"""Documentation commands"""
import click
from pathlib import Path
import os

@click.command(name="docs:generate")
def generate_docs():
    """Generate API documentation"""
    # Create docs directory if it doesn't exist
    docs_path = Path("docs")
    docs_path.mkdir(exist_ok=True)
    
    # Generate OpenAPI schema
    os.system("python3 -c 'from main import app; import json; open(\"docs/openapi.json\", \"w\").write(json.dumps(app.openapi()))'")
    
    # Generate ReDoc HTML
    with open("docs/index.html", "w") as f:
        f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>API Documentation</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    <style>
        body { margin: 0; padding: 0; }
    </style>
</head>
<body>
    <redoc spec-url="openapi.json"></redoc>
    <script src="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"></script>
</body>
</html>
        ''')
    
    click.echo("API documentation generated successfully!")
    click.echo(f"OpenAPI schema: file://{docs_path.absolute()}/openapi.json")
    click.echo(f"HTML documentation: file://{docs_path.absolute()}/index.html")

