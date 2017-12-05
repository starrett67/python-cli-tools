import os
import json
import click
import swagger_client
from pathlib import Path


@click.group()
def cli():
    pass


@click.command()
@click.option("--username", prompt="Username")
# TODO: Make this a hidden field
@click.option("--password", prompt="Password")
def login(username, password):
    home_dir = os.getenv("HOME")
    token_file = Path(home_dir, ".threeblades.token")
    if token_file.exists():
        with token_file.open() as tok_file:
            line = tok_file.read()
            token_json = json.loads(line)
            click.echo(f"Token JSON: {token_json}")
    else:
        auth_api = swagger_client.AuthApi()
        jwt_data = swagger_client.JWTData(username=username,
                                          password=password)
        response = auth_api.auth_jwt_token_auth(jwt_data=jwt_data)
        click.echo(response)
        with open(token_file, "w") as tok_file:
            tok_file.write(json.dumps({'token': response.token}))
    click.echo(f"Hello {username}.")


cli.add_command(login)


if __name__ == "__main__":
    cli()
