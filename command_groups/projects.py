import click
import tbs_client
from command_groups import (ThreeBladesBaseCommand, istbscommand)
from tbscli.decorators import instantiate_context, print_result
from tbscli.CONSTANTS import API_KEY_PREFIX, CLICK_CONTEXT_SETTINGS, PERMISSIONS_ALIASES


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
                         type=click.Choice(PERMISSIONS_ALIASES),
                         prompt=True)
        ]
        self.context = {}
        super(ProjectsAddUserCommand, self).__init__(name="adduser",
                                                     params=options,
                                                     help="Add a user as project collaborator",
                                                     api_class=tbs_client.ProjectsApi)

    def _validate_params(self, *args, **kwargs):
        kwargs['permissions'] = PERMISSIONS_ALIASES[kwargs.get('permissions')]
        return args, kwargs

    def _cmd(self, *args, **kwargs):
        if click.confirm(text=f"Proceed adding user {kwargs['user']}?", abort=True):
            # response = self.api_client.projects
            # print(response)
            click.echo(message=kwargs)
            click.echo(kwargs['permissions'])


class ProjectsRemoveUserCommand(ThreeBladesBaseCommand):
    def __init__(self):
        options = [
            click.Option(
                param_decls=["--user", "-u"],
                help="Username to remove from project",
                type=str,
                prompt=True
            )
        ]
        self.context = {}
        super(ProjectsRemoveUserCommand, self).__init__(name="rmuser",
                                                        params=options,
                                                        help="Remove a user from a project",
                                                        api_class=tbs_client.ProjectsApi)

    def _validate_params(self, *args, **kwargs):
        return args, kwargs

    def _cmd(self, *args, **kwargs):
        if click.confirm(text=f"Proceed removing user {kwargs['user']} from project?", abort=True):
            # response = self.api_client.projects...
            # print(response)
            pass


class ProjectsCreateCommand(ThreeBladesBaseCommand):
    def __init__(self):
        options = [
            click.Option(
                param_decls=["--namespace", "-n"],
                help="Namespace of new project",
                type=str,
                prompt=True
            ),
            click.Option(
                param_decls=["--project", "-p"],
                help="Name of new project",
                type=str,
                prompt=True
            ),
            click.Option(
                param_decls=["--description", "-d"],
                help="Description for the new project",
                type=str,
                prompt=True,
                # 'default' param here *should* allow --description to be empty
                default=""
            ),
            click.Option(
                param_decls=["--private", "-p"],
                help="Boolean value for public/private project setting",
                type=bool,
                prompt="Make new project private?"
            )
        ]
        self.context = {}
        super(ProjectsCreateCommand, self).__init__(name="create",
                                                    params=options,
                                                    help="Create a project",
                                                    api_class=tbs_client.ProjectsApi)

    def _validate_params(self, *args, **kwargs):
        return args, kwargs

    def _cmd(self, *args, **kwargs):
        project_data = tbs_client.ProjectData({
            'name': kwargs['project'],
            'description': kwargs['description'],
            'private': kwargs['private']
        })

        tbs_client.configuration.api_key['Authorization'] = self.obj['token']
        tbs_client.configuration.api_key_prefix['Authorization'] = API_KEY_PREFIX

        project_api = tbs_client.ProjectsApi()
        response = project_api.projects_create(namespace=kwargs['namespace'], project_data=project_data)
        return response

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


class ProjectsUpdateCommand(ThreeBladesBaseCommand):
    def __init__(self):
        options = [
            click.Option(
                param_decls=["--namespace", "-n"],
                help="Namespace of project",
                type=str,
                prompt=True
            ),
            click.Option(

            )
        ]
@click.command(help="Update a project", context_settings=CLICK_CONTEXT_SETTINGS)
@click.option("--namespace", "-n", help="Namespace hosting target project")
@instantiate_context
@print_result
def update(ctx, *args, **kwargs):
    namespace = kwargs['namespace']
    tbs_client.configuration.api_key['Authorization'] = ctx.obj['token']
    tbs_client.configuration.api_key_prefix['Authorization'] = 'Bearer'
    project_api = tbs_client.ProjectsApi()
    project_name = click.prompt("Name of project to delete", type=str)
    click.confirm(f"Are you SURE you want to delete the project {project_name}", abort=True)
    response = project_api.projects_delete(namespace, project=project_name)
    return response
    click.echo(namespace)



class ProjectsCLI(click.Group):
    def __init__(self, *args, **kwargs):
        kwargs['help'] = "Manage projects in your account"
        super(ProjectsCLI, self).__init__(*args, **kwargs)
        self.commands = {value().name: value for key, value in globals().items() if istbscommand(value)}

    def list_commands(self, ctx):
        return list(self.commands.keys())

    def get_command(self, ctx, cmd_name):
        return self.commands.get(cmd_name)()
