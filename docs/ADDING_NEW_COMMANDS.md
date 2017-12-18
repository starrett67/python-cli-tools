# Adding New Commands
## Top Level Commands
To add a new top level command, create a `.py` file in the `command_groups` package. The module name should be the name 
you would like the command to have. For example, if I want to add a command called `servers`, I would create a file at 
`command_groups/servers.py`

Inside that file, you need to create a sub class of `click.Group`. The class name must:

- match the name of the module
- be title cased
- end with "CLI"

Using our servers example, the class will look like this:
```python
import click
from command_groups import istbscommand


class ServersCLI(click.Group):
    def __init__(self, *args, **kwargs):
        kwargs['help'] = "Manage Project Servers"
        super(ServersCLI, self).__init__(*args, **kwargs)
        self.commands = {value().name: value for key, value in globals().items() if istbscommand(value)}

    def list_commands(self, ctx):
        return list(self.commands.keys())

    def get_command(self, ctx, cmd_name):
        return self.commands.get(cmd_name)()
```

Unfortunately, this class must be fully defined like this for each top level command instead of sub classing some parent command. 
This is due to the way python imports and `globals` works. This implementation may be changed in order to support inheritance
 at some point in the future. Note that this class definition **must** be at the **bottom** of the module. Again, this is due
 to the way `globals()` works in python.
 
 ## Sub Commands
 Sub Commands are defined by subclassing `ThreeBladesBaseCommand` (this, among other things, is what `istbscommand` checks for).
 There are no requirements on how these command classes must be named, but so far I've followed the convention `ModuleSubcommandCommand`.
 Your sub command class should define three methods:
 - `__init__`
 - `validate_params`
 - `_cmd`
 
 ### `__init__(self)`
 The `__init__` method is used to a.) define options/flags for the sub command, b.) the name of the sub command,
 c.) help information for the sub command, and d.) which API class from the SDK to use in order to communicate with the API.
 
 ##### Example:
 ```python
import click
import tbs_client
from command_groups import ThreeBladesBaseCommand


class ServersDetailsCommand(ThreeBladesBaseCommand):
    def __init__(self):
        params = [click.Option("--namespace"),
                  click.Option("--project", help="Name or UUID of the project that this server is associated with.")]
        super(ServersDetailsCommand, self).__init__(name="details",
                                                           params=params,
                                                           help="Create and deploy a model as a RESTful endpoint",
                                                           api_class=tbs_client.DeploymentsApi)
```
 
 This, combined with the `ServersCLI` class from above allows the following from the command line: `tbs servers read`.
 
 
 ### _validate_params(self, *args, **kwargs) -> tuple
 Strictly speaking, it is not _required_ that `_validate_params` be implemented, but it is rare that you wouldn't need to.
 `args` and `kwargs` come from whatever was passed to `params` at runtime. `args` corresponds to any required positional arguments
 for the subcommand (instances of `click.Argument`); `kwargs` are any optional flags (instances of `click.Option`) sudh as `--namespace`
 from our example. The purpose of this method is to check if the argument/option was provided by the user, make sure the value is 
 coherent, and perhaps prompt the user for input if need be. It must return a tuple containing the validated `args` and `kwargs`.
 
`tbs servers details --namespace foo --project bar` would result in `_validate_params` being called with `args=[]` and 
`kwargs = {'namespace': "foo", 'project': "Bar"}`.

#### Example
```python
def _validate_params(self, *args, **kwargs):
    namespace = kwargs.get('namespace') or self.context.get('namespace')
    if namespace is None:
        namespace = click.prompt("Namespace", type=str)
    kwargs['namespace'] = namespace

    project_name = kwargs.get("project")
    if project_name is None:
        project_name = click.prompt("Project", type=str)
    kwargs['project'] = project_name
    return args, kwargs
```

This example simply checks to see if a value was provided via a flag, and if not prompts the user to input the value.

### _cmd(self, *args, **kwargs)
This is the business logic of your command, and is typically pretty simple.

#### Example
```python
def _cmd(self, *args, **kwargs):
    # This example is going to assume that you've
    # collected all the necessary data to create a server
    server_data = tbs_client.DeploymentData(**server_data)
    response = self.api_client.deployments_create(namespace=kwargs.get('namespace'),
                                                  project=kwargs.get('project'),
                                                  deployment_data=server_data)
    click.echo(response)
```

## General Notes

- It's generally preferable to use `click.echo` instead of `print`