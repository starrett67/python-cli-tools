import click
import tbs_client
from command_groups import (ThreeBladesBaseCommand, istbscommand)
from tbscli.decorators import instantiate_context, print_result
from tbscli.CONSTANTS import CLICK_CONTEXT_SETTINGS, PERMISSIONS_CHOICES_DISPLAYED


# # TODO: Consider combining all these decorators into one. Would be a lot less verbose
# @click.command(help="Get details about a file in a project", context_settings=CLICK_CONTEXT_SETTINGS)
# @click.option("--namespace", "-n", help="Namespace hosting target project")
# @instantiate_context
# @print_result
# def detail(ctx, *args, **kwargs):
#     namespace = kwargs.get('namespace') or ctx.obj['namespace']
#     tbs_client.configuration.api_key['Authorization'] = ctx.obj['token']
#     tbs_client.configuration.api_key_prefix['Authorization'] = 'Bearer'
#     project_name = click.prompt("Enter a project name", type=str)
#     projects_api = tbs_client.ProjectsApi()
#     response = projects_api.projects_read(namespace, project_name)
#     return response
#
#
# @click.command(help="List all files in a project", context_settings=CLICK_CONTEXT_SETTINGS)
# @click.option("--namespace", "-n", help="Namespace hosting target project")
# @instantiate_context
# @print_result
# def list(ctx, *args, **kwargs):
#     namespace = kwargs.get('namespace') or ctx.obj['namespace']
#     tbs_client.configuration.api_key['Authorization'] = ctx.obj['token']
#     tbs_client.configuration.api_key_prefix['Authorization'] = 'Bearer'
#     projects_api = tbs_client.ProjectsApi()
#     response = projects_api.projects_list(namespace=namespace)
#     return response
#
#
# @click.command(help="Create a project", context_settings=CLICK_CONTEXT_SETTINGS)
# @click.option("--namespace", "-n", help="Namespace hosting target project")
# @instantiate_context
# @print_result
# def create(ctx, *args, **kwargs):
#     namespace = kwargs['namespace']
#     project_name = click.prompt("Enter a project name", type=str)
#     description = click.prompt("Enter a project description", type=str)
#     private = click.prompt("Is this a private project?", type=bool)
#     proj_data = {'name': project_name,
#                  'description': description,
#                  'private': private}
#     project_data = tbs_client.ProjectData(**proj_data)
#
#     tbs_client.configuration.api_key['Authorization'] = ctx.obj['token']
#     tbs_client.configuration.api_key_prefix['Authorization'] = 'Bearer'
#
#     project_api = tbs_client.ProjectsApi()
#     response = project_api.projects_create(namespace, project_data=project_data)
#     return response
#
#
# @click.command(help="Delete a project", context_settings=CLICK_CONTEXT_SETTINGS)
# @click.option("--namespace", "-n", help="Namespace hosting target project")
# @instantiate_context
# @print_result
# def delete(ctx, *args, **kwargs):
#     namespace = kwargs['namespace']
#     tbs_client.configuration.api_key['Authorization'] = ctx.obj['token']
#     tbs_client.configuration.api_key_prefix['Authorization'] = 'Bearer'
#     project_api = tbs_client.ProjectsApi()
#     project_name = click.prompt("Name of project to delete", type=str)
#     click.confirm(f"Are you SURE you want to delete the project {project_name}", abort=True)
#     response = project_api.projects_delete(namespace, project=project_name)
#     return response

class ProjectsAddUserCommand(ThreeBladesBaseCommand):
    def __init__(self):
        options = [
            click.Option(param_decls=["--user", "-u"],
                         help="Username to add as collaborator",
                         type=str,
                         prompt=True),
            click.Option(param_decls=["--permissions", "-p"],
                         help="Appropriate permissions level",
                         type=click.Choice(PERMISSIONS_CHOICES_DISPLAYED),
                         prompt=True)
        ]
        self.context = {}
        super(ProjectsAddUserCommand, self).__init__(name="adduser",
                                                     params=options,
                                                     help="Add a user as project collaborator",
                                                     api_class=tbs_client.ProjectsApi)

    def _validate_params(self, *args, **kwargs):
        return args, kwargs

    def _cmd(self, *args, **kwargs):
        # response = self.api_client.projects
        # print(response)
        click.echo(message=kwargs)

# @click.command(help="Update a project", context_settings=CLICK_CONTEXT_SETTINGS)
# @click.option("--namespace", "-n", help="Namespace hosting target project")
# @instantiate_context
# @print_result
# def update(ctx, *args, **kwargs):
#     namespace = kwargs['namespace']
#     # tbs_client.configuration.api_key['Authorization'] = ctx.obj['token']
#     # tbs_client.configuration.api_key_prefix['Authorization'] = 'Bearer'
#     # project_api = tbs_client.ProjectsApi()
#     # project_name = click.prompt("Name of project to delete", type=str)
#     # click.confirm(f"Are you SURE you want to delete the project {project_name}", abort=True)
#     # response = project_api.projects_delete(namespace, project=project_name)
#     # return response
#     click.echo(namespace)
#
#
# @click.command(help="Add a user as project collaborator", context_settings=CLICK_CONTEXT_SETTINGS)
# @click.option("--user", "-u", help="Username or email of user to add")
# @click.option("--permissions", "-p", help="Designated permissions level/role for added user")
# @instantiate_context
# @print_result
# def adduser(ctx, *args, **kwargs):
#     user = kwargs['user']
#     permissions = kwargs['permissions']
#     click.echo(user, permissions)
#     teams views from app-backend repo for add project collaborator
# --user should be either username or email
# --permissions should be [role]
#
#
# @click.command(help="Remove a user as project collaborator", context_settings=CLICK_CONTEXT_SETTINGS)
# @click.option("--user", "-u", help="Username or email of user to remove")
# @instantiate_context
# @print_result
# def rmuser(ctx, *args, **kwargs):
#     user = kwargs['user']
#     click.echo(user)

class ProjectsCLI(click.Group):
    def __init__(self, *args, **kwargs):
        kwargs['help'] = "Manage projects in your account"
        super(ProjectsCLI, self).__init__(*args, **kwargs)
        self.commands = {value().name: value for key, value in globals().items() if istbscommand(value)}

    def list_commands(self, ctx):
        return list(self.commands.keys())

    def get_command(self, ctx, cmd_name):
        return self.commands.get(cmd_name)()
