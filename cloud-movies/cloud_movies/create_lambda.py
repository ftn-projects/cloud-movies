from os import path
from aws_cdk import (
    aws_lambda as _lambda,
    Duration
)


LAMBDAS_HOME = 'lambdas'
RUNTIME = _lambda.Runtime.PYTHON_3_10
TIMEOUT_DURATION = Duration.seconds(10)


def create_lambda(scope, id, include_dir, handler, layers=[]):
    function = _lambda.Function(
        scope, id,
        code=_lambda.Code.from_asset(path.join(LAMBDAS_HOME, include_dir)),
        handler=handler,
        runtime=RUNTIME,
        layers=layers,
        timeout=TIMEOUT_DURATION
    )

    function.add_function_url(
        auth_type=_lambda.FunctionUrlAuthType.NONE,
        cors=_lambda.FunctionUrlCorsOptions(
            allowed_origins=['*']
        )
    )
    
    return function


def create_lambda_with_code(scope, id, code, layers=[]):
    return _lambda.Function(
        scope, id,
        code=_lambda.InlineCode(code),
        handler='index.handler',
        runtime=RUNTIME,
        layers=layers,
        timeout=TIMEOUT_DURATION
    )
