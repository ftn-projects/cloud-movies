from constructs import Construct
from .create_lambda import create_lambda, create_lambda_with_code
from aws_cdk import (
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    Stack,
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
            write_capacity=1,
            read_capacity=1
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
            )]
        )
        

        # Create Lambdas
        upload_lambda = create_lambda(self, 'uploadLambda', 'upload_video', 'upload_video.handler')
        upload_lambda.add_environment('BUCKET_NAME', source_bucket.bucket_name)
        source_bucket.grant_put(upload_lambda)

        upload_lambda.add_environment('TABLE_NAME', movies_table.table_name)
        movies_table.grant_read_write_data(upload_lambda)


        download_lambda = create_lambda(self, 'downloadLambda', 'download_video', 'download_video.handler')
        download_lambda.add_environment('BUCKET_NAME', source_bucket.bucket_name)
        source_bucket.grant_read(download_lambda)


        download_lambda.add_environment('TABLE_NAME', movies_table.table_name)
        movies_table.grant_read_write_data(download_lambda)
    

        # Create API Gateway
        api = apigateway.RestApi(self, API_GATEWAY)
        

        # POST /upload
        upload_resource = api.root.add_resource('upload')
        upload_integration = apigateway.LambdaIntegration(upload_lambda)
        upload_resource.add_method('POST', upload_integration)


        # GET /download
        download_resource = api.root.add_resource('download')
        download_integration = apigateway.LambdaIntegration(download_lambda)
        download_resource.add_method('GET', download_integration)
