import os
import json
import click
from pprint import pprint
from pathlib import Path

# TODO: Clean up how arguments/options are passed to subcommands.
# It's not great at the moment


def invoke_command(ctx, module_name, *args, **kwargs):
    sub_command = kwargs['sub_command']
    try:
        command_func = getattr(__import__(module_name), sub_command)
    except AttributeError:
        click.echo(f"Invalid sub-command: {sub_command}")
        raise
    response = command_func(ctx, *args, **kwargs)
    if response is not None:
        pprint(response)


@click.group()
@click.pass_context
def cli(ctx):
    home_dir = os.getenv("HOME")
    token_file = Path(home_dir, ".threeblades.token")
    if token_file.exists():
        with token_file.open() as tok_file:
            line = tok_file.read()
            token_json = json.loads(line)
            ctx.obj['token'] = token_json['token']


@click.command()
@click.argument("sub_command")
@click.option("--username")
@click.option("--password")
@click.pass_context
def auth(ctx, *args, **kwargs):
    invoke_command(ctx, "auth_cli", *args, **kwargs)


@click.command()
# TODO: Make namespace optional, defaulting to that of the user that is currently logged in.
# TODO: Add the various parameters?
@click.argument("sub_command")
@click.option("--namespace", prompt="Namespace")
@click.pass_context
def projects(ctx, *args, **kwargs):
    if "token" not in ctx.obj:
        click.echo("Make sure you've logged in first!")
    invoke_command(ctx, "projects_cli", *args, **kwargs)


@click.command()
@click.argument("sub_command")
@click.option("--namespace", prompt="Namespace")
@click.pass_context
# @click.option("--framework")
# @click.option("--files")
def deployments(ctx, *args, **kwargs):
    if "token" not in ctx.obj:
        click.echo("Make sure you've logged in first!")
    invoke_command(ctx, "deployments_cli", *args, **kwargs)


cli.add_command(auth)
cli.add_command(projects)
cli.add_command(deployments)


def main():
    return cli(obj={})
