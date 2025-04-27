import click
from pathlib import Path
import os
import secrets
from typing import List
import subprocess
import sys
from fastapi import Depends
from app.cli.templates.service import SERVICE_TEMPLATE, SERVICE_WITH_INTERFACE_TEMPLATE
from app.cli.templates.controller import BASIC_CONTROLLER_TEMPLATE, RESOURCE_CONTROLLER_TEMPLATE, API_CONTROLLER_TEMPLATE
from app.cli.templates.model import MODEL_TEMPLATE
from app.cli.templates.seeder import SEEDER_TEMPLATE

@click.group()
def app():
    """FastAPI Boilerplate CLI"""
    pass

@app.command(name="serve")
@click.option('--reload', is_flag=True, help='Enable auto-reload')
def serve(reload: bool):
    """Start the development server"""
    reload_flag = "--reload" if reload else ""
    os.system(f"uvicorn main:app {reload_flag}")

@app.command(name="key:generate")
def key_generate():
    """Generate a new application key"""
    key = secrets.token_hex(32)
    click.echo(f"Application key: {key}")

@app.command(name="make:migration")
@click.argument('message', required=False)
def make_migration(message: str = None):
    """Create a new database migration"""
    if not message:
        message = click.prompt("Enter migration message")
    os.system(f'alembic revision --autogenerate -m "{message}"')

@app.command(name="migrate")
def migrate():
    """Run database migrations"""
    os.system("alembic upgrade head")

@app.command(name="migrate:status")
def migrate_status():
    """Show the status of database migrations"""
    os.system("alembic current")

@app.command(name="migrate:rollback")
def rollback():
    """Rollback the last database migration"""
    os.system("alembic downgrade -1")

@app.command(name="migrate:reset")
def migrate_reset():
    """Reset database (rollback all migrations)"""
    os.system("alembic downgrade base")
    click.echo("Database reset successfully!")

@app.command(name="migrate:refresh")
def migrate_refresh():
    """Refresh database (rollback + migrate)"""
    os.system("alembic downgrade base")
    os.system("alembic upgrade head")
    click.echo("Database refreshed successfully!")

@app.command(name="make:model")
@click.argument('name')
@click.option('--migration', is_flag=True, help='Create a migration for the model')
@click.option('--controller', is_flag=True, help='Create a controller for the model')
@click.option('--all', is_flag=True, help='Create all components (model, migration, controller, service, schema)')
def make_model(name: str, migration: bool, controller: bool, all: bool):
    """Create a new model file"""
    model_name = name.lower()
    model_class = name.capitalize()
    
    # Create models directory if it doesn't exist
    model_path = Path("app/models") / f"{model_name}.py"
    if model_path.exists():
        click.echo(f"Model {name} already exists!")
        return

    model_path.parent.mkdir(parents=True, exist_ok=True)

    # Create model file
    model_content = MODEL_TEMPLATE.format(
        model_name=model_name,
        model_class=model_class
    )
    model_path.write_text(model_content)
    click.echo(f"Model {name} created successfully!")
    click.echo(f"Model: file://{model_path.absolute()}")

    # Create migration if requested
    if migration or all:
        os.system(f'alembic revision --autogenerate -m "create {model_name} model"')
        migration_path = Path("alembic/versions")
        latest_migration = sorted(migration_path.glob("*.py"))[-1] if migration_path.exists() else None
        if latest_migration:
            click.echo(f"Migration: file://{latest_migration.absolute()}")

    # Create controller if requested
    if controller or all:
        os.system(f'./artisan make:controller {model_class}Controller --resource')

    # Create all components if requested
    if all:
        # Create service
        os.system(f'./artisan make:service {model_class}Service --interface')
        
        # Create schema
        os.system(f'./artisan make:schema {model_class}')

@app.command(name="make:controller")
@click.argument('name')
@click.option('--resource', is_flag=True, help='Create a resource controller')
@click.option('--api', is_flag=True, help='Create an API controller')
def make_controller(name: str, resource: bool, api: bool):
    """Create a new controller file"""
    # Remove 'Controller' suffix if present
    model_name = name.lower().replace('controller', '')
    model_class = name.replace('Controller', '')
    controller_class = name

    controller_path = Path("app/controllers") / f"{name.lower()}.py"
    if controller_path.exists():
        click.echo(f"Controller {name} already exists!")
        return

    # Create controllers directory if it doesn't exist
    controller_path.parent.mkdir(parents=True, exist_ok=True)

    # Choose template based on flags
    if api:
        template = API_CONTROLLER_TEMPLATE
    elif resource:
        template = RESOURCE_CONTROLLER_TEMPLATE
    else:
        template = BASIC_CONTROLLER_TEMPLATE
    
    # Format template with variables
    controller_content = template.format(
        model_name=model_name,
        model_class=model_class,
        controller_class=controller_class
    )

    controller_path.write_text(controller_content)
    click.echo(f"Controller {name} created successfully!")
    click.echo(f"Controller: file://{controller_path.absolute()}")

@app.command(name="make:service")
@click.argument('name')
@click.option('--interface', is_flag=True, help='Create service with interface')
def make_service(name: str, interface: bool):
    """Create a new service file"""
    # Remove 'Service' suffix if present
    model_name = name.lower().replace('service', '')
    model_class = name.replace('Service', '')
    service_class = name

    service_path = Path("app/services") / f"{name.lower()}.py"
    if service_path.exists():
        click.echo(f"Service {name} already exists!")
        return

    # Create services directory if it doesn't exist
    service_path.parent.mkdir(parents=True, exist_ok=True)

    # Choose template based on interface flag
    template = SERVICE_WITH_INTERFACE_TEMPLATE if interface else SERVICE_TEMPLATE
    
    # Format template with variables
    service_content = template.format(
        model_name=model_name,
        model_class=model_class,
        service_class=service_class
    )

    service_path.write_text(service_content)
    click.echo(f"Service {name} created successfully!")
    click.echo(f"Service: file://{service_path.absolute()}")

@app.command(name="make:schema")
@click.argument('name')
def make_schema(name: str):
    """Create a new schema file"""
    schema_path = Path("app/schemas") / f"{name.lower()}.py"
    if schema_path.exists():
        click.echo(f"Schema {name} already exists!")
        return

    schema_content = f'''from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class {name.capitalize()}Base(BaseModel):
    pass

class {name.capitalize()}Create({name.capitalize()}Base):
    pass

class {name.capitalize()}Response({name.capitalize()}Base):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
'''
    schema_path.write_text(schema_content)
    click.echo(f"Schema {name} created successfully!")

@app.command(name="test")
@click.argument('test_path', required=False)
def test(test_path: str = None):
    """Run tests"""
    if test_path:
        os.system(f"pytest {test_path}")
    else:
        os.system("pytest")

@app.command(name="seed")
def seed():
    """Seed the database with initial data"""
    # Add your seeding logic here
    click.echo("Database seeded successfully!")

@app.command(name="cache:clear")
def clear_cache():
    """Clear the application cache"""
    cache_path = Path("app/cache")
    if cache_path.exists():
        for file in cache_path.glob("*"):
            file.unlink()
    click.echo("Cache cleared successfully!")

@app.command(name="logs:view")
def view_logs():
    """View application logs"""
    log_path = Path("logs/app.log")
    if not log_path.exists():
        click.echo("No logs found!")
        return
    
    with open(log_path, 'r') as f:
        click.echo(f.read())

@app.command(name="logs:clear")
def clear_logs():
    """Clear application logs"""
    log_path = Path("logs/app.log")
    if log_path.exists():
        log_path.write_text("")
        click.echo("Logs cleared successfully!")
    else:
        click.echo("No logs found!")

@app.command(name="make:middleware")
@click.argument('name')
def make_middleware(name: str):
    """Create a new middleware file"""
    middleware_path = Path("app/middleware") / f"{name.lower()}.py"
    if middleware_path.exists():
        click.echo(f"Middleware {name} already exists!")
        return

    middleware_content = f'''from fastapi import Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware

class {name.capitalize()}Middleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Process request
        response = await call_next(request)
        # Process response
        return response
'''
    middleware_path.write_text(middleware_content)
    click.echo(f"Middleware {name} created successfully!")

@app.command(name="make:exception")
@click.argument('name')
def make_exception(name: str):
    """Create a new exception file"""
    exception_path = Path("app/exceptions") / f"{name.lower()}.py"
    if exception_path.exists():
        click.echo(f"Exception {name} already exists!")
        return

    exception_content = f'''from fastapi import HTTPException, status

class {name.capitalize()}Exception(HTTPException):
    def __init__(self, detail: str = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail or "An error occurred"
        )
'''
    exception_path.write_text(exception_content)
    click.echo(f"Exception {name} created successfully!")

@app.command(name="make:validator")
@click.argument('name')
def make_validator(name: str):
    """Create a new validator file"""
    validator_path = Path("app/validators") / f"{name.lower()}.py"
    if validator_path.exists():
        click.echo(f"Validator {name} already exists!")
        return

    validator_content = f'''from pydantic import BaseModel, validator

class {name.capitalize()}Validator(BaseModel):
    @validator('*')
    def validate_fields(cls, v):
        # Add your validation logic here
        return v
'''
    validator_path.write_text(validator_content)
    click.echo(f"Validator {name} created successfully!")

@app.command(name="make:repository")
@click.argument('name')
def make_repository(name: str):
    """Create a new repository file"""
    repository_path = Path("app/repositories") / f"{name.lower()}.py"
    if repository_path.exists():
        click.echo(f"Repository {name} already exists!")
        return

    repository_content = f'''from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.{name.lower()} import {name.capitalize()}
from app.schemas.{name.lower()} import {name.capitalize()}Create, {name.capitalize()}Update

class {name.capitalize()}Repository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[{name.capitalize()}]:
        return self.db.query({name.capitalize()}).all()

    def get_by_id(self, id: int) -> Optional[{name.capitalize()}]:
        return self.db.query({name.capitalize()}).filter({name.capitalize()}.id == id).first()

    def create(self, obj_in: {name.capitalize()}Create) -> {name.capitalize()}:
        db_obj = {name.capitalize()}(**obj_in.dict())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: {name.capitalize()}, obj_in: {name.capitalize()}Update) -> {name.capitalize()}:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, db_obj: {name.capitalize()}) -> None:
        self.db.delete(db_obj)
        self.db.commit()
'''
    repository_path.write_text(repository_content)
    click.echo(f"Repository {name} created successfully!")

@app.command(name="docs:generate")
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

@app.command(name="make:seeder")
@click.argument('name')
def make_seeder(name: str):
    """Create a new seeder file"""
    # Remove 'Seeder' suffix if present
    model_name = name.lower().replace('seeder', '')
    model_class = name.replace('Seeder', '')
    seeder_class = name

    seeder_path = Path("app/seeders") / f"{name.lower()}.py"
    if seeder_path.exists():
        click.echo(f"Seeder {name} already exists!")
        return

    # Create seeders directory if it doesn't exist
    seeder_path.parent.mkdir(parents=True, exist_ok=True)

    # Create seeder file
    seeder_content = SEEDER_TEMPLATE.format(
        model_name=model_name,
        model_class=model_class,
        seeder_class=seeder_class
    )
    seeder_path.write_text(seeder_content)
    click.echo(f"Seeder {name} created successfully!")
    click.echo(f"Seeder: file://{seeder_path.absolute()}")

@app.command(name="db:seed")
@click.option('--seeder', help='Run specific seeder')
def db_seed(seeder: str = None):
    """Run database seeders"""
    seeders_path = Path("app/seeders")
    if not seeders_path.exists():
        click.echo("No seeders found!")
        return

    if seeder:
        # Run specific seeder
        seeder_file = seeders_path / f"{seeder.lower()}.py"
        if not seeder_file.exists():
            click.echo(f"Seeder {seeder} not found!")
            return
        
        # Import and run the seeder
        seeder_module = f"app.seeders.{seeder.lower()}"
        seeder_class = seeder
        try:
            module = __import__(seeder_module, fromlist=[seeder_class])
            seeder_instance = getattr(module, seeder_class)()
            count = seeder_instance.run()
            click.echo(f"Seeder {seeder} ran successfully! Created {count} records.")
        except Exception as e:
            click.echo(f"Error running seeder {seeder}: {str(e)}")
    else:
        # Run all seeders
        for seeder_file in seeders_path.glob("*.py"):
            if seeder_file.name == "__init__.py":
                continue
            
            seeder_name = seeder_file.stem.capitalize()
            seeder_module = f"app.seeders.{seeder_file.stem}"
            try:
                module = __import__(seeder_module, fromlist=[seeder_name])
                seeder_instance = getattr(module, seeder_name)()
                count = seeder_instance.run()
                click.echo(f"Seeder {seeder_name} ran successfully! Created {count} records.")
            except Exception as e:
                click.echo(f"Error running seeder {seeder_name}: {str(e)}")

@app.command(name="db:refresh")
def db_refresh():
    """Refresh database (migrate:fresh + seed)"""
    # Run fresh migrations
    os.system("alembic downgrade base")
    os.system("alembic upgrade head")
    
    # Run seeders
    os.system("./artisan db:seed")
    
    click.echo("Database refreshed successfully!")

if __name__ == '__main__':
    app() 