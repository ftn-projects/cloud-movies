from aws_cdk import (
    aws_lambda as _lambda,
    BundlingOptions,
    Duration
)


RUNTIME = _lambda.Runtime.PYTHON_3_10
MEMORY_SIZE = 128
TIMEOUT_SECONDS = 10


# Function Definitions
def create_lambda(scope, id, handler, include_dir, layers, lambda_role):
    function = _lambda.Function(
        scope, id,
        runtime=RUNTIME,
        layers=layers,
        handler=handler,
        code=_lambda.Code.from_asset(include_dir,
            bundling=BundlingOptions(
                image=RUNTIME.bundling_image,
                command=[
                    "bash", "-c",
                    "pip install --no-cache -r requirements.txt -t /asset-output && cp -r . /asset-output"
                ],
            ),),
        memory_size=MEMORY_SIZE,
        timeout=Duration.seconds(TIMEOUT_SECONDS),
        role=lambda_role
    )
    fn_url = function.add_function_url(
        auth_type=_lambda.FunctionUrlAuthType.NONE,
        cors=_lambda.FunctionUrlCorsOptions(
            allowed_origins=["*"]
        )
    )
    
    return function
