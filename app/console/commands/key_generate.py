"""Key Generate command"""
import click
import secrets

@click.command(name="key:generate")
def key_generate():
    """Generate a new application key"""
    key = secrets.token_hex(32)
    click.echo(f"Application key: {key}")

