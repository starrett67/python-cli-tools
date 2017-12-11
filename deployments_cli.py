import click
import swagger_client


def deploy(ctx, *args, **kwargs):
    namespace = kwargs.get('namespace') or ctx.obj.get('namespace')
    if namespace is None:
        namespace = click.prompt("Namespace", type=str)

    swagger_client.configuration.api_key['Authorization'] = ctx.obj['token']
    swagger_client.configuration.api_key_prefix['Authorization'] = 'Bearer'

    project_name = kwargs.get("project")
    if project_name is None:
        project_name = click.prompt("Project", type=str)

    deployment_name = click.prompt("Name", type=str)
    handler = click.prompt("Handler Function", type=str)
    files = click.prompt("Files", type=str)
    runtime = click.prompt("Runtime", type=str)
    framework = click.prompt("Framework", type=str)

    config = swagger_client.DeploymentConfig(handler=handler,
                                             files=[f.strip() for f in files.split(",")])

    deployment_data = {'name': deployment_name,
                       'config': config,
                       'runtime': runtime,
                       'framework': framework}

    deploy_data = swagger_client.DeploymentData(**deployment_data)

    deployments_api = swagger_client.DeploymentsApi()
    initial_response = deployments_api.deployments_create(namespace=namespace,
                                                          project=project_name,
                                                          deployment_data=deploy_data)

    response = deployments_api.deployments_deploy(namespace=namespace,
                                                  project=project_name,
                                                  deployment=initial_response.name)
    return response
