from constructs import Construct
from .create_lambda import (
    create_lambda, 
    create_lambda_layer, 
    create_python_lambda_layer, 
    create_lambda_integration
)
from aws_cdk import (
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_stepfunctions_tasks as sfn_tasks,
    aws_stepfunctions as sfn,
    aws_lambda_event_sources as lambda_event_sources,
    aws_sns_subscriptions as subscriptions,
    aws_sns as sns,
    aws_cognito as cognito,
    aws_iam as iam,
    RemovalPolicy,
    CfnOutput,
    Stack
)


# Constants

VIDEOS_TABLE = 'videosTable'
REVIEWS_TABLE = 'reviewsTable'
SUBSCRIPTIONS_TABLE = 'subscriptionsTable'
FEEDS_TABLE = 'feedsTable'
RATINGS_TABLE = 'ratingTable'

SOURCE_BUCKET = 'sourceBucket'
PUBLISH_BUCKET = 'publishBucket'
DESTINATION_BUCKET = 'destinationBucket'

API_GATEWAY = 'moviesApi'

USER_POOL = 'moviesUserPool'
CLIENT_NAME = 'movies-client'
DOMAIN_NAME = 'movies-app-123456789'

USER_ROLE = 'UserRole'
ADMIN_ROLE = 'AdminRole'

USER_GROUP = 'UserGroup'
ADMIN_GROUP = 'AdminGroup'


VIDEOS_TABLE_GSI = ['videoType', 'title', 'description', 'actors', 'directors', 'genres']
VIDEO_EXTENSIONS = ['mp4', 'mov', 'm4v']
VIDEO_RESOLUTIONS = ['360', '480', '720']

ADMIN_EMAIL = 'dimitrije.gasic.02@gmail.com'


class CloudMoviesStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # DynamoDB Tables
        self.videos_table = dynamodb.Table(
            self, VIDEOS_TABLE,
            partition_key=dynamodb.Attribute(name='videoId', type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name='videoType', type=dynamodb.AttributeType.STRING),
            removal_policy=RemovalPolicy.DESTROY
        )
        for index in VIDEOS_TABLE_GSI:
            self.videos_table.add_global_secondary_index(
                index_name=f'{index}Index',
                partition_key=dynamodb.Attribute(name=index, type=dynamodb.AttributeType.STRING)
            )

        self.subscriptions_table = dynamodb.Table(
            self, SUBSCRIPTIONS_TABLE,
            partition_key=dynamodb.Attribute(name='userId', type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name='subscriptionType',type=dynamodb.AttributeType.STRING),
            removal_policy=RemovalPolicy.DESTROY
        )
        
        self.ratings_table = dynamodb.Table(
            self, RATINGS_TABLE,
            partition_key=dynamodb.Attribute(name='userId', type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name='contentId', type=dynamodb.AttributeType.STRING),
            removal_policy=RemovalPolicy.DESTROY 
        )

        # S3 Buckets
        cors_allow_all = s3.CorsRule(
            allowed_methods=[
                s3.HttpMethods.GET,
                s3.HttpMethods.PUT,
                s3.HttpMethods.POST,
                s3.HttpMethods.DELETE,
                s3.HttpMethods.HEAD,
            ],
            allowed_origins=['*'],
            allowed_headers=['*']
        )
        self.source_bucket = s3.Bucket(
            self, SOURCE_BUCKET, 
            cors=[cors_allow_all], 
            auto_delete_objects=True,
            removal_policy=RemovalPolicy.DESTROY
        )
        self.publish_bucket = s3.Bucket(
            self, PUBLISH_BUCKET, 
            cors=[cors_allow_all],
            auto_delete_objects=True,
            removal_policy=RemovalPolicy.DESTROY
        )
        
        # SNS Topics
        self.source_upload_processing_topic = sns.Topic(self, 'sourceUploadProcessingTopic')
        self.source_upload_processing_topic.add_subscription(subscriptions.EmailSubscription(ADMIN_EMAIL))

        # Utils layer
        self.utils_layer = create_python_lambda_layer(self, 'utils', 'layer/utils')

        self.__create_source_upload_processing_workflow()
        self.__create_source_upload_processing_cleanup()

        self.__create_api_gateway()
        self.__create_user_pool()


    def __create_source_upload_processing_workflow(self) -> None:
        unzip_lambda = create_lambda(self, 'unzipVideoLambda', 'unzip_video', 'unzip_video.handler')
        unzip_lambda.add_environment('VIDEOS_TABLE', self.videos_table.table_name)
        unzip_lambda.add_environment('EXTENSIONS', ','.join(VIDEO_EXTENSIONS))
        unzip_lambda.add_environment('FAILED_TOPIC_ARN', self.source_upload_processing_topic.topic_arn)
        self.videos_table.grant_write_data(unzip_lambda)
        self.source_bucket.grant_read_write(unzip_lambda)
        self.source_upload_processing_topic.grant_publish(unzip_lambda)

        unzip_lambda.add_event_source(lambda_event_sources.S3EventSource(
            bucket=self.source_bucket,
            events=[s3.EventType.OBJECT_CREATED],
            filters=[{'suffix': '.zip'}]
        ))

        ffmpeg_layer = create_lambda_layer(self, 'ffmpegLayer', 'layer/ffmpeg')
        transcode_lambda = create_lambda(self, 'transcodeVideoLambda', 'transcode_video', 'transcode_video.handler', 900, 1024, [ffmpeg_layer])
        transcode_lambda.add_environment('SOURCE_BUCKET', self.source_bucket.bucket_name)
        transcode_lambda.add_environment('PUBLISH_BUCKET', self.publish_bucket.bucket_name)
        self.source_bucket.grant_read(transcode_lambda)
        self.publish_bucket.grant_write(transcode_lambda)
        self.source_upload_processing_topic.grant_publish(transcode_lambda)

        parallel = sfn.Parallel(self, 'parallelTranscoding')
        for resolution in VIDEO_RESOLUTIONS:
            parallel.branch(sfn_tasks.LambdaInvoke(
                self, f'transcoding{resolution}',
                lambda_function=transcode_lambda,
                payload=sfn.TaskInput.from_object({
                    'resolution': resolution,
                    'objectKey.$': '$.objectKey',
                    'timestamp.$': '$.timestamp'
                }),
            ).add_retry(
                max_attempts=3,
                backoff_rate=2
            ))

        success_publish = sfn_tasks.SnsPublish(
            self, 'publishSuccessfulTranscoding',
            topic=self.source_upload_processing_topic,
            message=sfn.TaskInput.from_object({
                'success': True,
                'state': 'transcoding',
                'objectKey.$': '$.[0].Payload.objectKey'
            })
        )
        failed_publish = sfn_tasks.SnsPublish(
            self, 'publishFailedTranscoding',
            topic=self.source_upload_processing_topic,
            message=sfn.TaskInput.from_object({
                'success': False,
                'state': 'transcoding',
                'error.$': '$.errorInfo.Cause'
            })
        )
        parallel.add_catch(failed_publish, errors=["States.ALL"], result_path="$.errorInfo")

        state_machine = sfn.StateMachine(
            self, 'transcodingStateMachine', 
            definition_body=sfn.DefinitionBody.from_chainable(parallel.next(success_publish)),
            removal_policy=RemovalPolicy.DESTROY
        )

        start_transcoding_lambda = create_lambda(self, 'startTranscodingLambda', 'start_transcoding', 'start_transcoding.handler')
        start_transcoding_lambda.add_environment('TRANSCODING_STATE_MACHINE', state_machine.state_machine_arn)
        state_machine.grant_start_execution(start_transcoding_lambda)

        for extension in VIDEO_EXTENSIONS:
            start_transcoding_lambda.add_event_source(lambda_event_sources.S3EventSource(
                bucket=self.source_bucket,
                events=[s3.EventType.OBJECT_CREATED],
                filters=[{'suffix': extension}]
            ))


    def __create_source_upload_processing_cleanup(self) -> None:
        cleanup_lambda = create_lambda(self, 'handle_processing_result')
        cleanup_lambda.add_environment('SOURCE_BUCKET', self.source_bucket.bucket_name)
        cleanup_lambda.add_environment('PUBLISH_BUCKET', self.publish_bucket.bucket_name)
        cleanup_lambda.add_environment('VIDEOS_TABLE', self.videos_table.table_name)
        cleanup_lambda.add_environment('RESOLUTIONS', ','.join(VIDEO_RESOLUTIONS))
        self.publish_bucket.grant_read(cleanup_lambda)
        self.publish_bucket.grant_delete(cleanup_lambda)
        self.videos_table.grant_read_write_data(cleanup_lambda)
        self.source_bucket.grant_delete(cleanup_lambda)
        self.source_upload_processing_topic.add_subscription(subscriptions.LambdaSubscription(cleanup_lambda))


    def __create_api_gateway(self) -> apigateway.RestApi:
        upload_lambda = create_lambda(self, 'uploadVideoLambda', 'upload_video', 'upload_video.handler')
        upload_lambda.add_environment('SOURCE_BUCKET', self.source_bucket.bucket_name)
        self.source_bucket.grant_put(upload_lambda)

        list_videos_lambda = create_lambda(self, 'listVideosLambda', 'list_videos', 'list_videos.handler', layers=[self.utils_layer])
        list_videos_lambda.add_environment('VIDEOS_TABLE', self.videos_table.table_name)
        self.videos_table.grant_read_data(list_videos_lambda)

        find_video_lambda = create_lambda(self, 'findVideoLambda', 'get_details', 'get_details.handler', layers=[self.utils_layer])
        find_video_lambda.add_environment('VIDEOS_TABLE', self.videos_table.table_name)
        self.videos_table.grant_read_data(find_video_lambda)

        query_videos_lambda = create_lambda(self, 'queryVideosLambda', 'query_videos', 'query_videos.handler')
        query_videos_lambda.add_environment('VIDEOS_TABLE', self.videos_table.table_name)
        self.videos_table.grant_read_data(query_videos_lambda)

        list_subscriptions_lambda = create_lambda(self, 'listSubscriptionsLambda', 'list_subscriptions', 'list_subscriptions.handler', layers=[self.utils_layer])
        list_subscriptions_lambda.add_environment('SUBSCRIPTIONS_TABLE', self.subscriptions_table.table_name)
        self.subscriptions_table.grant_read_data(list_subscriptions_lambda)

        stream_lambda = create_lambda(self, 'streamLambda', 'stream_video', 'stream_video.handler', layers=[self.utils_layer])
        stream_lambda.add_environment('PUBLISH_BUCKET', self.publish_bucket.bucket_name)
        stream_lambda.add_environment('VIDEOS_TABLE', self.videos_table.table_name)
        self.publish_bucket.grant_read(stream_lambda)
        self.videos_table.grant_read_data(stream_lambda)
        
        stream_lambda.add_to_role_policy(iam.PolicyStatement(
            actions=['s3:*'],
            resources=[f"{self.publish_bucket.bucket_arn}/*"]
        ))

        subscribe_lambda = create_lambda(self, 'subscribeLambda', 'subscribe', 'subscribe.handler', layers=[self.utils_layer])
        subscribe_lambda.add_environment('SUBSCRIPTIONS_TABLE', self.subscriptions_table.table_name)
        self.subscriptions_table.grant_read_write_data(subscribe_lambda)

        unsubscribe_lambda = create_lambda(self, 'unsubcribeLambda', 'unsubscribe', 'unsubscribe.handler', layers=[self.utils_layer])
        unsubscribe_lambda.add_environment('SUBSCRIPTIONS_TABLE', self.subscriptions_table.table_name)
        self.subscriptions_table.grant_read_write_data(unsubscribe_lambda)

        rate_content_lambda = create_lambda(self, 'rateContentLambda', 'rate_content', 'rate_content.handler', layers=[self.utils_layer])
        rate_content_lambda.add_environment('RATINGS_TABLE', self.ratings_table.table_name)
        self.ratings_table.grant_read_write_data(rate_content_lambda)


        # Create API Gateway
        api = apigateway.RestApi(self, API_GATEWAY)

        # Resources
        content_resource = api.root.add_resource('content')
        videos_resource = api.root.add_resource('video')
        movies_resource = api.root.add_resource('movie')

        show_resource = api.root.add_resource('show')
        show_id_resource = show_resource.add_resource('{showId}')
        season_id_resource = show_id_resource.add_resource('{season}')
        episode_id_resource = season_id_resource.add_resource('{episode}')

        subscriptions_resource = api.root.add_resource('subscription')
        rating_resource = api.root.add_resource('ratings')
        sub_user_id_resource = subscriptions_resource.add_resource(
            '{userId}', default_cors_preflight_options=apigateway.CorsOptions(
                allow_methods=apigateway.Cors.ALL_METHODS,
                allow_origins=apigateway.Cors.ALL_ORIGINS
            ))

        # GET /upload
        upload_video_integration = apigateway.LambdaIntegration(upload_lambda)
        api.root.add_resource('upload').add_method('GET', upload_video_integration)

        # GET /content - admin
        list_videos_integration = apigateway.LambdaIntegration(list_videos_lambda)
        content_resource.add_method('GET', list_videos_integration)

        # GET /content/{videoId} - anyone
        find_video_integration = apigateway.LambdaIntegration(find_video_lambda)
        content_id_res = content_resource.add_resource('{videoId}')
        content_id_res.add_method('GET', find_video_integration)

        # GET /content/query
        query_videos_integration = apigateway.LambdaIntegration(query_videos_lambda)
        videos_resource.add_resource('query').add_method('GET', query_videos_integration)

        # GET /subscription/{userId (orEmail)}
        list_subscriptions_integration = apigateway.LambdaIntegration(list_subscriptions_lambda)
        sub_user_id_resource.add_method('GET', list_subscriptions_integration)

        # POST /subscription/{userId}
        subscribe_integration = apigateway.LambdaIntegration(subscribe_lambda)
        sub_user_id_resource.add_method('POST', subscribe_integration)

        # DELETE /subscription/{userId}
        unsubscribe_integration = apigateway.LambdaIntegration(unsubscribe_lambda)
        sub_user_id_resource.add_resource('{type}').add_resource('{name}').add_method('DELETE', unsubscribe_integration)

        # GET /video/{videoId}/{resolution}?season=1&episode=2 - stream/download video
        stream_integration = apigateway.LambdaIntegration(stream_lambda)
        video_id_resource = videos_resource.add_resource('{videoId}')
        video_id_resource.add_resource('{resolution}').add_method('GET', stream_integration)

        rating_integration = apigateway.LambdaIntegration(rate_content_lambda)
        rating_user_id_resource = rating_resource.add_resource('{user_id}', 
                                                                    default_cors_preflight_options=apigateway.CorsOptions(
                                                                    allow_methods=apigateway.Cors.ALL_METHODS,
                                                                    allow_origins=apigateway.Cors.ALL_ORIGINS
                                                                    ))
        rating_user_id_resource.add_method('POST', rating_integration)

        # GET /show/{showId}/seasonDetails - seasons with episodes
        show_id_resource.add_resource('seasonDetails').add_method('GET', create_lambda_integration(
            self, 'get_season_details', 
            env_vars=[('VIDEOS_TABLE', self.videos_table.table_name)],
            permissions=[self.videos_table.grant_read_data]
        ))

        # GET /show/{showId}/{season}/{episode} - episode details
        episode_id_resource.add_method('GET', create_lambda_integration(
            self, 'get_episode_details',
            env_vars=[('VIDEOS_TABLE', self.videos_table.table_name)],
            permissions=[self.videos_table.grant_read_data]
        ))

        # POST /show - create show
        show_resource.add_method('POST', create_lambda_integration(
            self, 'create_show',
            env_vars=[('VIDEOS_TABLE', self.videos_table.table_name)],
            permissions=[self.videos_table.grant_read_write_data]
        ))

        # POST /show/{showId} - create season
        show_id_resource.add_method('POST', create_lambda_integration(
            self, 'create_season',
            env_vars=[('VIDEOS_TABLE', self.videos_table.table_name)],
            permissions=[self.videos_table.grant_read_write_data]
        ))

        # PUT /content/{videoId} - update show/movie details
        content_resource.add_resource('{videoId}').add_method('PUT', create_lambda_integration(
            self, 'edit_details',
            env_vars=[('VIDEOS_TABLE', self.videos_table.table_name)],
            permissions=[self.videos_table.grant_read_write_data]
        ))
    
        # PUT /show/{showId}/{season}/{episode} - update episode
        season_id_resource.add_method('PUT', create_lambda_integration(
            self, 'edit_episode',
            env_vars=[('VIDEOS_TABLE', self.videos_table.table_name)],
            permissions=[self.videos_table.grant_read_write_data]
        ))

        # DELETE /show/{showId}
        show_id_resource.add_method('DELETE', create_lambda_integration(
            self, 'delete_show',
            env_vars=[
                ('VIDEOS_TABLE', self.videos_table.table_name), 
                ('PUBLISH_BUCKET', self.publish_bucket.bucket_name)],
            permissions=[
                self.videos_table.grant_read_write_data, 
                self.publish_bucket.grant_delete]
        ))

        # DELETE /show/{showId}/{season}
        season_id_resource.add_method('DELETE', create_lambda_integration(
            self, 'delete_season',
            env_vars=[
                ('VIDEOS_TABLE', self.videos_table.table_name),
                ('PUBLISH_BUCKET', self.publish_bucket.bucket_name)],
            permissions=[
                self.videos_table.grant_read_write_data,
                self.publish_bucket.grant_delete]
        ))

        # DELETE /show/{showId}/{season}/{episode}
        episode_id_resource.add_method('DELETE', create_lambda_integration(
            self, 'delete_episode',
            env_vars=[
                ('VIDEOS_TABLE', self.videos_table.table_name),
                ('PUBLISH_BUCKET', self.publish_bucket.bucket_name)],
            permissions=[
                self.videos_table.grant_read_write_data,
                self.publish_bucket.grant_delete]
        ))

        # DELETE /movie/{movieId}
        movies_resource.add_resource('{movieId}').add_method('DELETE', create_lambda_integration(
            self, 'delete_movie',
            env_vars=[
                ('VIDEOS_TABLE', self.videos_table.table_name),
                ('PUBLISH_BUCKET', self.publish_bucket.bucket_name)],
            permissions=[
                self.videos_table.grant_read_write_data,
                self.publish_bucket.grant_delete]
        ))

        return api


    def __create_user_pool(self) -> cognito.UserPool:
        attach_role_lambda = create_lambda(self, 'attachUserRole', 'attach_role', 'user_role.handler')
        
        pool = cognito.UserPool(
            self, USER_POOL,
            sign_in_case_sensitive=False,
            self_sign_up_enabled=True,
            user_verification=cognito.UserVerificationConfig(
                email_subject='Verify Your Email Address for movies-app',
                email_body="""
                Thank you for registering with Movies-app. To complete your registration, please verify your email address by clicking {##here##}. \n\n
                If you did not register for Movies-app, please ignore this email.\n\n
                Thank you,\n
                Movies-app Team\n""",
                email_style=cognito.VerificationEmailStyle.LINK
            ),
            sign_in_aliases=cognito.SignInAliases(
                username=True,
                email=True
                ),
            auto_verify=cognito.AutoVerifiedAttrs(
                email=True
                ),
            standard_attributes=cognito.StandardAttributes(
                birthdate=cognito.StandardAttribute(
                    required=True,
                    mutable=False
                ),
                given_name=cognito.StandardAttribute(
                    required=True,
                    mutable=False
                ),
                family_name=cognito.StandardAttribute(
                    required=True,
                    mutable=False
                ),
                email=cognito.StandardAttribute(
                    required=True,
                    mutable=False
                )
            ),
            lambda_triggers=cognito.UserPoolTriggers(
                post_confirmation=attach_role_lambda
            ), 
            removal_policy=RemovalPolicy.DESTROY
        )

        pool_domain = pool.add_domain(
            'CognitoDomain', 
            cognito_domain=cognito.CognitoDomainOptions(
             domain_prefix=DOMAIN_NAME
            )   
        )

        # Creates a client for User Pool
        client = pool.add_client(
            CLIENT_NAME,
            generate_secret=False,
            auth_flows=cognito.AuthFlow(
                user_password=True,
                custom=True,
                user_srp=True,
                admin_user_password=True 
            ),
            o_auth=cognito.OAuthSettings(
                flows=cognito.OAuthFlows(
                    authorization_code_grant=True
                ),
                scopes=[cognito.OAuthScope.OPENID],
            ),
        )

        user_role = iam.Role(
            self, USER_ROLE,
            assumed_by=iam.ServicePrincipal('cognito-idp.amazonaws.com'),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name('ReadOnlyAccess')
            ]
        )

        admin_role = iam.Role(
            self, ADMIN_ROLE,
            assumed_by=iam.ServicePrincipal('cognito-idp.amazonaws.com'),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name('AdministratorAccess')
            ]
        )

        user_group = cognito.CfnUserPoolGroup(
            self, USER_GROUP,
            group_name='User',
            user_pool_id=pool.user_pool_id,
        )

        admin_group = cognito.CfnUserPoolGroup(
            self, ADMIN_GROUP,
            group_name='Admin',
            user_pool_id=pool.user_pool_id,
        )        

        admin_group.role_arn = admin_role.role_arn
        user_group.role_arn = user_role.role_arn

        
        attach_role_lambda.role.attach_inline_policy(
            iam.Policy(self, 'userpool-policy',
                           statements=[iam.PolicyStatement(
                               actions=['cognito-idp:AdminAddUserToGroup'],
                               resources=[pool.user_pool_arn]
                            )]))
        
        CfnOutput(self, 'UserPoolId', value=pool.user_pool_id)
        CfnOutput(self, 'UserPoolClientId', value=client.user_pool_client_id)
        CfnOutput(self, 'UserPoolDomain', value=pool_domain.domain_name)

        return pool
