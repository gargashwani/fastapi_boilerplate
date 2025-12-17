"""Test command"""
import click
import os

@click.command(name="test")
@click.argument('test_path', required=False)
def test(test_path: str = None):
    """Run tests"""
    if test_path:
        os.system(f"pytest {test_path}")
    else:
        os.system("pytest")

