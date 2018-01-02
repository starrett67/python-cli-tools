import tbs_client
import click
from tbscli.decorators import instantiate_context, print_result


# TODO: Consider combining all these decorators into one. Would be a lot less verbose
@click.command(help="Get details about a file in a project")
@click.option("--namespace", help="Namespace hosting target project")
@instantiate_context
@print_result
def detail(ctx, *args, **kwargs):
    namespace = kwargs.get('namespace') or ctx.obj['namespace']
    tbs_client.configuration.api_key['Authorization'] = ctx.obj['token']
    tbs_client.configuration.api_key_prefix['Authorization'] = 'Bearer'
    project_name = click.prompt("Enter a project name", type=str)
    projects_api = tbs_client.ProjectsApi()
    response = projects_api.projects_read(namespace, project_name)
    return response


@click.command(help="List all files in a project")
@click.option("--namespace", help="Namespace hosting target project")
@instantiate_context
@print_result
def list(ctx, *args, **kwargs):
    namespace = kwargs.get('namespace') or ctx.obj['namespace']
    tbs_client.configuration.api_key['Authorization'] = ctx.obj['token']
    tbs_client.configuration.api_key_prefix['Authorization'] = 'Bearer'
    projects_api = tbs_client.ProjectsApi()
    response = projects_api.projects_list(namespace=namespace)
    return response


@click.command(help="Create a project")
@click.option("--namespace", help="Namespace hosting target project")
@instantiate_context
@print_result
def create(ctx, *args, **kwargs):
    namespace = kwargs['namespace']
    project_name = click.prompt("Enter a project name", type=str)
    description = click.prompt("Enter a project description", type=str)
    private = click.prompt("Is this a private project?", type=bool)
    proj_data = {'name': project_name,
                 'description': description,
                 'private': private}
    project_data = tbs_client.ProjectData(**proj_data)

    tbs_client.configuration.api_key['Authorization'] = ctx.obj['token']
    tbs_client.configuration.api_key_prefix['Authorization'] = 'Bearer'

    project_api = tbs_client.ProjectsApi()
    response = project_api.projects_create(namespace, project_data=project_data)
    return response


@click.command(help="Delete a project")
@click.option("--namespace", help="Namespace hosting target project")
@instantiate_context
@print_result
def delete(ctx, *args, **kwargs):
    namespace = kwargs['namespace']
    tbs_client.configuration.api_key['Authorization'] = ctx.obj['token']
    tbs_client.configuration.api_key_prefix['Authorization'] = 'Bearer'
    project_api = tbs_client.ProjectsApi()
    project_name = click.prompt("Name of project to delete", type=str)
    click.confirm(f"Are you SURE you want to delete the project {project_name}", abort=True)
    response = project_api.projects_delete(namespace, project=project_name)
    return response


@click.command(help="Add a user as project collaborator")
@click.option("--user", help="Username or email of user to add")
@click.option("--permissions", help="Designated permissions level/role for added user")
@instantiate_context
@print_result
def adduser(ctx, *args, **kwargs):
    user = kwargs['user']
    permissions = kwargs['permissions']
    click.echo(user, permissions)
#     teams views from app-backend repo for add project collaborator
# --user should be either username or email
# --permissions should be [role]


class ProjectsCLI(click.Group):
    def __init__(self, *args, **kwargs):
        kwargs['help'] = "Manage projects in your account"
        super(ProjectsCLI, self).__init__(*args, **kwargs)

    def list_commands(self, ctx):
        commands = [key for key, value in globals().items() if isinstance(value, click.Command)]
        return commands

    def get_command(self, ctx, cmd_name):
        return globals().get(cmd_name)

