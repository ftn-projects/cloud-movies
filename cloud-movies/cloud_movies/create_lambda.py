from os import path
from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    Duration
)
from aws_cdk.aws_lambda_python_alpha import PythonLayerVersion

LAMBDAS_HOME = 'lambdas'
RUNTIME = _lambda.Runtime.PYTHON_3_9
TIMEOUT_DURATION = Duration.seconds(10)


def create_lambda_integration(scope, name, include_dir=None, handler=None, timeout=10, memory=128, layers=[], env_vars=[], permissions=[]):
    function = create_lambda(scope, name, include_dir, handler, timeout, memory, layers, env_vars, permissions)
    return apigateway.LambdaIntegration(function)


def create_lambda(scope, name, include_dir=None, handler=None, timeout=10, memory=128, layers=[], env_vars=[], permissions=[]):
    if include_dir is None:
        include_dir = name
    if handler is None:
        handler = name + '.handler'

    function = _lambda.Function(
        scope, __camel_case(name.split('_')) + 'Lambda',
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

    for var in env_vars:
        function.add_environment(*var)

    for permission in permissions:
        permission(function)
    
    return function


def __camel_case(words: list[str]) -> str:
    return words[0].lower() + ''.join(word.capitalize() for word in words[1:])


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
