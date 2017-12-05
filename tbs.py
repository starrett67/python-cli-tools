import os
import json
import click
import swagger_client
from pathlib import Path


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


# TODO: This always prompts for username and password, even if a token exists already.
# Make that conditional
@click.command()
@click.option("--username", prompt="Username")
# TODO: Make this a hidden field
@click.option("--password", prompt="Password", hide_input=True)
@click.pass_context
def login(ctx, username, password):
    home_dir = os.getenv("HOME")
    token_file = Path(home_dir, ".threeblades.token")
    if token_file.exists():
        with token_file.open() as tok_file:
            line = tok_file.read()
            token_json = json.loads(line)
            ctx.obj['token'] = token_json['token']
    else:
        auth_api = swagger_client.AuthApi()
        jwt_data = swagger_client.JWTData(username=username,
                                          password=password)
        response = auth_api.auth_jwt_token_auth(jwt_data=jwt_data)
        ctx.obj['token'] = response.token
        with open(token_file, "w") as tok_file:
            tok_file.write(json.dumps({'token': response.token}))
    click.echo(f"Hello {username}.")
    click.echo(ctx.obj['token'])


@click.command()
# TODO: Make namespace optional, defaulting to that of the user that is currently logged in.
# TODO: Add the various parameters?
@click.option("--namespace", prompt="Namespace")
@click.pass_context
def project_list(ctx, namespace):
    if "token" not in ctx.obj:
        click.echo("Make sure you've logged in first!")

    swagger_client.configuration.api_key['Authorization'] = ctx.obj['token']
    swagger_client.configuration.api_key_prefix['Authorization'] = 'Bearer'
    projects_api = swagger_client.ProjectsApi()
    response = projects_api.projects_list(namespace=namespace)
    print(response)


cli.add_command(login)
cli.add_command(project_list)


def main():
    return cli(obj={})
