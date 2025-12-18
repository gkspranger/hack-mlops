import click


@click.group()
def cli():
    pass


@cli.command()
@click.option("-c", "--count", default=1, help="Number of greetings.")
@click.argument("name")
def greet(count, name):
    """
    Simple program that greets NAME for a total of COUNT times.
    """
    for x in range(count):
        click.echo(f"Hello, {name}!")


cli.add_command(greet)


def main():
    cli()
