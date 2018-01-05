import click
import tbs_client
from command_groups import (ThreeBladesBaseCommand, istbscommand)
from tbscli.decorators import instantiate_context, print_result
from tbscli.CONSTANTS import PERMISSIONS_ALIASES


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
        response = self.api_client.projects_create(namespace=kwargs['namespace'], project_data=project_data)
        return response


class ProjectsDeleteCommand(ThreeBladesBaseCommand):
    def __init__(self):
        options = [
            click.Option(
                param_decls=["--namespace", "-n"],
                help="Namespace of project",
                type=str,
                prompt=True
            ),
            click.Option(
                param_decls=["--project", "-p"],
                help="Name of project to delete",
                type=str,
                prompt=True
            )
        ]
        self.context = {}
        super(ProjectsDeleteCommand, self).__init__(name="delete",
                                                    params=options,
                                                    help="Delete a project",
                                                    api_class=tbs_client.ProjectsApi)

    def _validate_params(self, *args, **kwargs):
            return args, kwargs

    def _cmd(self, *args, **kwargs):
        if click.confirm(text=f"Proceed deleting project {kwargs['project']}?", abort=True):
            response = self.api_client.projects_delete(namespace=kwargs['namespace'], project=kwargs['project'])
            return response


class ProjectsListCommand(ThreeBladesBaseCommand):
    def __init__(self):
        options = [
            click.Option(
                param_decls=["--namespace", "-n"],
                help="Namespace of project",
                type=str,
                prompt=True
            )
        ]
        self.context = {}
        super(ProjectsListCommand, self).__init__(name="list",
                                                  params=options,
                                                  help="List all projects in a namespace",
                                                  api_class=tbs_client.ProjectsApi)
    def _validate_params(self, *args, **kwargs):
        return args, kwargs

    def _cmd(self, *args, **kwargs):
        response = self.api_client.projects_list(namespace=kwargs['namespace'])
        return response


class ProjectsAddUserCommand(ThreeBladesBaseCommand):
    def __init__(self):
        options = [
            click.Option(
                param_decls=["--user", "-u"],
                help="Username to add as collaborator",
                type=str,
                prompt=True),
            click.Option(
                param_decls=["--permissions", "-p"],
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

#
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

class ProjectsCLI(click.Group):
    def __init__(self, *args, **kwargs):
        kwargs['help'] = "Manage projects in your account"
        super(ProjectsCLI, self).__init__(*args, **kwargs)
        self.commands = {value().name: value for key, value in globals().items() if istbscommand(value)}

    def list_commands(self, ctx):
        return list(self.commands.keys())

    def get_command(self, ctx, cmd_name):
        return self.commands.get(cmd_name)()
