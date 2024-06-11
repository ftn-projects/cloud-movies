from constructs import Construct
from .create_lambda import create_lambda
from aws_cdk import (
    aws_lambda as _lambda,
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
        source_bucket = s3.Bucket(
                    self, 'Bucket',
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

        # IAM Role for Lambda Functions
        lambda_role = iam.Role(
            self, "LambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )
        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
        )
        lambda_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "dynamodb:DescribeTable",
                    "dynamodb:Query",
                    "dynamodb:Scan",
                    "dynamodb:GetItem",
                    "dynamodb:PutItem",
                    "dynamodb:UpdateItem",
                    "dynamodb:DeleteItem",
                    "s3:GetObject",
                    "s3:PutObject"
                ],
                resources=[movies_table.table_arn]
            )
        )

        upload_lambda = create_lambda(self, "uploadFile", "uploadFile.upload_file_handler", "lambdas", lambda_role)
        upload_lambda.add_environment("TABLE_NAME", movies_table.table_name)
        upload_lambda.add_environment("BUCKET_NAME", source_bucket.bucket_name)
        source_bucket.grant_put(upload_lambda)
        source_bucket.grant_put_acl(upload_lambda)


        handler = create_lambda(self, "handler", "handler.handler", "lambdas", lambda_role)

        # Define the API Gateway resource
        api = apigateway.LambdaRestApi(
            self,
            "moovis",
            handler = handler
        )
        
        # '/upload' resource with a POST method
        upload_resource = api.root.add_resource("upload")
        upload_integration = apigateway.LambdaIntegration(upload_lambda)
        upload_resource.add_method("POST", upload_integration)


        # '/download' resource with a GET method
        # download_resource = api.root.add_resource("download")
        # download_integration = apigateway.LambdaIntegration(download_handler)  # TODO download handler
        # download_resource.add_method("GET", upload_integration)
