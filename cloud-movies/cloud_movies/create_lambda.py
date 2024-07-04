from os import path
from aws_cdk import (
    aws_lambda as _lambda,
    Duration
)
from aws_cdk.aws_lambda_python_alpha import PythonLayerVersion

LAMBDAS_HOME = 'lambdas'
RUNTIME = _lambda.Runtime.PYTHON_3_10
TIMEOUT_DURATION = Duration.seconds(10)


def create_lambda(scope, id, include_dir, handler, timeout=10, memory=128, layers=[]):
    function = _lambda.Function(
        scope, id,
        code=_lambda.Code.from_asset(path.join(LAMBDAS_HOME, include_dir)),
        handler=handler,
        runtime=RUNTIME,
        layers=layers,
        timeout=Duration.seconds(timeout),
        memory_size=memory
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


def create_lambda_layer(scope, id, code):
    return _lambda.LayerVersion(
        scope, id,
        code=_lambda.Code.from_asset(code),
        compatible_runtimes=[RUNTIME],
    )

def create_python_lambda_layer(scope, id, entry):
    return PythonLayerVersion(
            scope, id,
            entry=entry,
            compatible_runtimes=[RUNTIME]
        )