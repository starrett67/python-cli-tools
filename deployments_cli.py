import click
import swagger_client


def create(ctx, *args, **kwargs):
    namespace = kwargs['namespace']
    swagger_client.configuration.api_key['Authorization'] = ctx.obj['token']
    swagger_client.configuration.api_key_prefix['Authorization'] = 'Bearer'
    project_name = click.prompt("Project", type=str)
    deployment_name = click.prompt("Name", type=str)
    handler = click.prompt("Handler Function", type=str)
    files = click.prompt("Files", type=str)
    runtime = click.prompt("Runtime", type=str)
    framework = click.prompt("Framework", type=str)

    config = swagger_client.DeploymentConfig(handler=handler,
                                             files=files.split(","))

    deployment_data = {'name': deployment_name,
                       'config': config,
                       'runtime': runtime,
                       'framework': framework}

    deploy_data = swagger_client.DeploymentData(**deployment_data)

    deployments_api = swagger_client.DeploymentsApi()
    response = deployments_api.deployments_create(namespace, project_name,
                                                  deployment_data=deploy_data)
    return response
