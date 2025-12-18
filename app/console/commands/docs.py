"""Documentation commands"""

import os
from pathlib import Path

import click


@click.command(name="docs:generate")
def generate_docs():
    """Generate API documentation using MkDocs"""
    click.echo("📚 Generating documentation with MkDocs...")
    
    # Run mkdocs build
    result = os.system("uv run mkdocs build")
    
    if result == 0:
        click.echo("✅ Documentation generated successfully in the 'site/' directory!")
    else:
        click.echo("❌ Error generating documentation. Make sure mkdocs is installed.")
