from constructs import Construct
from create_lambda import create_lambda
from aws_cdk import (
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_iam as iam,
    Stack,
)


DYNAMO_MOVIES_TABLE = "movies"
S3_SOURCE_BUCKET = "source-bucket"


class CloudMoviesStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # Create DynamoDb Table
        movies_table = dynamodb.Table(
            self, DYNAMO_MOVIES_TABLE,
            partition_key=dynamodb.Attribute(
                name="id", type=dynamodb.AttributeType.STRING
            ),
            write_capacity=1,
            read_capacity=1
        )


        # Create S3 source bucket
        source_bucket = s3.Bucket(self, S3_SOURCE_BUCKET)
        

        # Define the API Gateway resource
        api = apigateway.LambdaRestApi(
            self,
            "moovis",
            proxy = False,
        )
        
        # '/upload' resource with a POST method
        upload_resource = api.root.add_resource("upload")
        # upload_integration = apigateway.LambdaIntegration(upload_handler)  # TODO upload handler
        upload_resource.add_method("POST")


        # '/download' resource with a GET method
        download_resource = api.root.add_resource("download")
        # download_integration = apigateway.LambdaIntegration(download_handler)  # TODO download handler
        download_resource.add_method("GET")
