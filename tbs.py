import click


@click.group()
def cli():
    pass


@click.command()
@click.option("--username", prompt="Username")
@click.option("--password", prompt="Password")
def login(username, password):
    click.echo(f"Hello {username}")


cli.add_command(login)


if __name__ == "__main__":
    cli()
