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

MOVIES_TABLE = 'videosTable'
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
        movies_table = dynamodb.Table(
            self, MOVIES_TABLE,
            partition_key=dynamodb.Attribute(
                name='id', type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name='title', type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY,
        )
        movies_table.add_global_secondary_index(
            index_name='titleIndex',
            partition_key=dynamodb.Attribute(
                name='title', type=dynamodb.AttributeType.STRING
            )
        )
        movies_table.add_global_secondary_index(
            index_name='descriptionIndex',
            partition_key=dynamodb.Attribute(
                name='description', type=dynamodb.AttributeType.STRING
            )
        )
        movies_table.add_global_secondary_index(
            index_name='actorsIndex',
            partition_key=dynamodb.Attribute(
                name='actors', type=dynamodb.AttributeType.STRING
            )
        )
        movies_table.add_global_secondary_index(
            index_name='directorsIndex',
            partition_key=dynamodb.Attribute(
                name='directors', type=dynamodb.AttributeType.STRING
            )
        )
        movies_table.add_global_secondary_index(
            index_name='genresIndex',
            partition_key=dynamodb.Attribute(
                name='genres', type=dynamodb.AttributeType.STRING
            )
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
        source_bucket.grant_read(download_lambda)


        # Create API Gateway
        api = apigateway.RestApi(self, API_GATEWAY)
        

        # GET /uploadurl
        upload_integration = apigateway.LambdaIntegration(upload_lambda)
        upload = api.root.add_resource('uploadurl')
        upload.add_method('GET', upload_integration)


        # GET /download/{video_file}
        # TODO communicate with DynamoDB where video_file should be associated with video uuid
        download_integration = apigateway.LambdaIntegration(download_lambda)
        download = api.root.add_resource('download').add_resource('{video_file}')
        download.add_method('GET', download_integration)
