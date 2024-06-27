from constructs import Construct
from .create_lambda import create_lambda
from aws_cdk import (
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    RemovalPolicy,
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


class CloudMoviesStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


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
