from constructs import Construct
from .create_lambda import create_lambda
from aws_cdk import (
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    RemovalPolicy,
    aws_cognito,
    aws_iam,
    CfnOutput,
    Stack
)


# ID-s

VIDEOS_TABLE = 'videosTable'
REVIEWS_TABLE = 'reviewsTable'
SUBSCRIPTIONS_TABLE = 'subscriptionsTable'
FEEDS_TABLE = 'feedsTable'

SOURCE_BUCKET = 'sourceBucket'
DESTINATION_BUCKET = 'destinationBucket'

API_GATEWAY = 'moviesApi'

USER_POOL = 'moviesUserPool'
CLIENT_NAME = 'movies-client'
DOMAIN_NAME = 'movies-app-123456789'

USER_ROLE = 'UserRole'
ADMIN_ROLE = 'AdminRole'

USER_GROUP = 'UserGroup'
ADMIN_GROUP = 'AdminGroup'

class CloudMoviesStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        attach_role_lambda = create_lambda(self, 'attachUserRole', 'attach_role', 'user_role.handler')
        
        # Creates User Pool
        pool = aws_cognito.UserPool(
            self, USER_POOL,
            sign_in_case_sensitive=False,
            self_sign_up_enabled=True,
            user_verification=aws_cognito.UserVerificationConfig(
                email_subject="Verify Your Email Address for movies-app",
                email_body="""
                Thank you for registering with Movies-app. To complete your registration, please verify your email address by clicking {##here##}. \n\n
                If you did not register for Movies-app, please ignore this email.\n\n
                Thank you,\n
                Movies-app Team\n""",
                email_style=aws_cognito.VerificationEmailStyle.LINK
            ),
            sign_in_aliases=aws_cognito.SignInAliases(
                username=True,
                email=True
                ),
            auto_verify=aws_cognito.AutoVerifiedAttrs(
                email=True
                ),
            standard_attributes=aws_cognito.StandardAttributes(
                birthdate=aws_cognito.StandardAttribute(
                    required=True,
                    mutable=False
                ),
                given_name=aws_cognito.StandardAttribute(
                    required=True,
                    mutable=False
                ),
                family_name=aws_cognito.StandardAttribute(
                    required=True,
                    mutable=False
                ),
                email=aws_cognito.StandardAttribute(
                    required=True,
                    mutable=False
                )
            ),
            lambda_triggers=aws_cognito.UserPoolTriggers(
                post_confirmation=attach_role_lambda
            ) 
        )

        pool_domain = pool.add_domain(
            "CognitoDomain", 
            cognito_domain=aws_cognito.CognitoDomainOptions(
             domain_prefix=DOMAIN_NAME
            )   
        )

        # Creates a client for User Pool
        client = pool.add_client(
            CLIENT_NAME,
            generate_secret=False,
            auth_flows=aws_cognito.AuthFlow(
                user_password=True,
                custom=True,
                user_srp=True,
                admin_user_password=True 
            ),
            o_auth=aws_cognito.OAuthSettings(
                flows=aws_cognito.OAuthFlows(
                    authorization_code_grant=True
                ),
                scopes=[aws_cognito.OAuthScope.OPENID],
            ),
        )

        user_role = aws_iam.Role(
            self, USER_ROLE,
            assumed_by=aws_iam.ServicePrincipal('cognito-idp.amazonaws.com'),
            managed_policies=[
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('ReadOnlyAccess')
            ]
        )

        admin_role = aws_iam.Role(
            self, ADMIN_ROLE,
            assumed_by=aws_iam.ServicePrincipal('cognito-idp.amazonaws.com'),
            managed_policies=[
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('AdministratorAccess')
            ]
        )

        user_group = aws_cognito.CfnUserPoolGroup(
            self, USER_GROUP,
            group_name='User',
            user_pool_id=pool.user_pool_id,
        )

        admin_group = aws_cognito.CfnUserPoolGroup(
            self, ADMIN_GROUP,
            group_name='Admin',
            user_pool_id=pool.user_pool_id,
        )        

        admin_group.role_arn = admin_role.role_arn
        user_group.role_arn = user_role.role_arn

        
        attach_role_lambda.role.attach_inline_policy(
            aws_iam.Policy(self, 'userpool-policy',
                           statements=[aws_iam.PolicyStatement(
                               actions=['cognito-idp:AdminAddUserToGroup'],
                               resources=[pool.user_pool_arn]
                            )]))

        # attach_role_lambda.add_to_role_policy(
        #     aws_iam.PolicyStatement(
        #         actions=['cognito-idp:AdminAddUserToGroup'],
        #         resources=[pool.user_pool_arn]
        #     )
        # )

        # pool.add_trigger(
        #     aws_cognito.UserPoolOperation.POST_CONFIRMATION,
        #     attach_role_lambda
        # )
        
        CfnOutput(self, "UserPoolId", value=pool.user_pool_id)
        CfnOutput(self, "UserPoolClientId", value=client.user_pool_client_id)
        CfnOutput(self, "UserPoolDomain", value=pool_domain.domain_name)


        # Create DynamoDB Table
        videos_table = dynamodb.Table(
            self, VIDEOS_TABLE,
            partition_key=dynamodb.Attribute(
                name='id', type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY,
        )
        videos_table.add_global_secondary_index(
            index_name='titleIndex',
            partition_key=dynamodb.Attribute(
                name='title', type=dynamodb.AttributeType.STRING
            )
        )
        videos_table.add_global_secondary_index(
            index_name='descriptionIndex',
            partition_key=dynamodb.Attribute(
                name='description', type=dynamodb.AttributeType.STRING
            )
        )
        videos_table.add_global_secondary_index(
            index_name='actorsIndex',
            partition_key=dynamodb.Attribute(
                name='actors', type=dynamodb.AttributeType.STRING
            )
        )
        videos_table.add_global_secondary_index(
            index_name='directorsIndex',
            partition_key=dynamodb.Attribute(
                name='directors', type=dynamodb.AttributeType.STRING
            )
        )
        videos_table.add_global_secondary_index(
            index_name='genresIndex',
            partition_key=dynamodb.Attribute(
                name='genres', type=dynamodb.AttributeType.STRING
            )
        )

        subscriptions_table = dynamodb.Table(
            self, SUBSCRIPTIONS_TABLE,
            partition_key=dynamodb.Attribute(
                name='id', type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY,
        )

        # Create S3 source bucket
        source_bucket = s3.Bucket(
                    self, SOURCE_BUCKET,
                    cors=[s3.CorsRule(
                        allowed_methods=[
                            s3.HttpMethods.GET,
                            s3.HttpMethods.PUT,
                            s3.HttpMethods.POST,
                            s3.HttpMethods.DELETE
                        ],
                        allowed_origins=['*'],  # You can specify more specific origins here
                        allowed_headers=['*']  # You can specify more specific headers here
                    )],
                    
                )
        

        # Create Lambdas
        upload_lambda = create_lambda(self, 'uploadLambda', 'upload_video', 'upload_video.handler')
        upload_lambda.add_environment('BUCKET_NAME', source_bucket.bucket_name)
        source_bucket.grant_put(upload_lambda)

        download_lambda = create_lambda(self, 'downloadLambda', 'download_video', 'download_video.handler')
        download_lambda.add_environment('BUCKET_NAME', source_bucket.bucket_name)
        download_lambda.add_environment('TABLE_NAME', videos_table.table_name)
        source_bucket.grant_read(download_lambda)
        videos_table.grant_read_data(download_lambda)

        list_videos_lambda = create_lambda(self, 'listVideosLambda', 'list_videos', 'list_videos.handler')
        list_videos_lambda.add_environment('TABLE_NAME', videos_table.table_name)
        videos_table.grant_read_data(list_videos_lambda)

        find_video_lambda = create_lambda(self, 'findVideoLambda', 'get_details', 'get_details.handler')
        find_video_lambda.add_environment('TABLE_NAME', videos_table.table_name)
        videos_table.grant_read_data(find_video_lambda)

        query_videos_lambda = create_lambda(self, 'queryVideosLambda', 'query_videos', 'query_videos.handler')
        query_videos_lambda.add_environment('TABLE_NAME', videos_table.table_name)
        videos_table.grant_read_data(query_videos_lambda)

        list_subscriptions_lambda = create_lambda(self, 'listSubscriptionsLambda', 'list_subscriptions', 'list_subscriptions.handler')
        list_subscriptions_lambda.add_environment('TABLE_NAME', subscriptions_table.table_name)
        subscriptions_table.grant_read_data(list_subscriptions_lambda)


        # Create API Gateway
        api = apigateway.RestApi(self, API_GATEWAY)
        

        # GET /uploadurl
        upload_integration = apigateway.LambdaIntegration(upload_lambda)
        api.root.add_resource('uploadurl').add_method('GET', upload_integration)


        # GET /download/{video_id}
        download_integration = apigateway.LambdaIntegration(download_lambda)
        download_resource = api.root.add_resource('download').add_resource('{video_id}').add_resource('{resolution}')
        download_resource.add_method('GET', download_integration)


        videos_resource = api.root.add_resource('videos')
        subscriptions_resource = api.root.add_resource('subscriptions')


        # GET /videos
        list_videos_integration = apigateway.LambdaIntegration(list_videos_lambda)
        videos_resource.add_method('GET', list_videos_integration)


        # GET /videos/{video_id}
        find_video_integration = apigateway.LambdaIntegration(find_video_lambda)
        videos_resource.add_resource('{video_id}').add_method('GET', find_video_integration)


        # GET /videos/query
        query_videos_integration = apigateway.LambdaIntegration(query_videos_lambda)
        videos_resource.add_resource('query').add_method('GET', query_videos_integration)


        # GET /subscriptions
        list_subscriptions_integration = apigateway.LambdaIntegration(list_subscriptions_lambda)
        subscriptions_resource.add_method('GET', list_subscriptions_integration)
