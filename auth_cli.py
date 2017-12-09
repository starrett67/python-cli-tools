import os
import json
import click
import swagger_client
from pathlib import Path


def login(ctx, *args, **kwargs):
    username = kwargs.get('username')
    password = kwargs.get('password')
    home_dir = os.getenv("HOME")
    token_file = Path(home_dir, ".threeblades.token")
    if token_file.exists():
        click.echo(".threeblades.token file already exists in $HOME directory. "
                   "Using that to login.")
        with token_file.open() as tok_file:
            line = tok_file.read()
            token_json = json.loads(line)
            ctx.obj['token'] = token_json['token']
    else:
        if not (username and password):
            username = click.prompt("Username", type=str)
            password = click.prompt("Password", type=str, hide_input=True)
        auth_api = swagger_client.AuthApi()
        jwt_data = swagger_client.JWTData(username=username,
                                          password=password)
        response = auth_api.auth_jwt_token_auth(jwt_data=jwt_data)
        ctx.obj['token'] = response.token
        with open(token_file, "w") as tok_file:
            tok_file.write(json.dumps({'token': response.token}))

        click.echo(f"Welcome {username}")

    click.echo("Login successful")
