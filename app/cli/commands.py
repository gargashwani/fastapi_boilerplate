import click
from pathlib import Path
import os
import secrets
from typing import List
import subprocess
import sys
from fastapi import Depends

@click.group()
def app():
    """FastAPI Boilerplate CLI"""
    pass

@app.command(name="serve")
def serve():
    """Start the development server"""
    os.system("uvicorn main:app --reload")

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

@app.command(name="make:model")
@click.argument('name')
@click.option('--migration', is_flag=True, help='Create a migration for the model')
def make_model(name: str, migration: bool):
    """Create a new model file"""
    model_path = Path("app/models") / f"{name.lower()}.py"
    if model_path.exists():
        click.echo(f"Model {name} already exists!")
        return

    # Create models directory if it doesn't exist
    model_path.parent.mkdir(parents=True, exist_ok=True)

    model_content = f'''from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.core.database import Base
from datetime import datetime

class {name.capitalize()}(Base):
    __tablename__ = "{name.lower()}s"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
'''
    model_path.write_text(model_content)
    
    # Print clickable file paths
    click.echo("\nCreated files:")
    click.echo(f"Model: file://{model_path.absolute()}")
    
    if migration:
        # Create migrations directory if it doesn't exist
        migration_path = Path("alembic/versions")
        migration_path.mkdir(parents=True, exist_ok=True)
        
        # Generate migration
        os.system(f'alembic revision --autogenerate -m "create {name.lower()} model"')
        
        # Get the latest migration file
        latest_migration = sorted(migration_path.glob("*.py"))[-1] if migration_path.exists() else None
        if latest_migration:
            click.echo(f"Migration: file://{latest_migration.absolute()}")
    
    click.echo(f"\nModel {name} created successfully!")

@app.command(name="make:controller")
@click.argument('name')
def make_controller(name: str):
    """Create a new controller file"""
    controller_path = Path("app/controllers") / f"{name.lower()}.py"
    if controller_path.exists():
        click.echo(f"Controller {name} already exists!")
        return

    controller_content = f'''from fastapi import APIRouter, Depends
from typing import List
from app.schemas.{name.lower()} import {name.capitalize()}Create, {name.capitalize()}Response
from app.services.{name.lower()} import {name.capitalize()}Service

router = APIRouter(prefix="/{name.lower()}s", tags=["{name.lower()}s"])

@router.get("/", response_model=List[{name.capitalize()}Response])
async def get_{name.lower()}s(service: {name.capitalize()}Service = Depends()):
    return await service.get_all()

@router.post("/", response_model={name.capitalize()}Response)
async def create_{name.lower()}({name.lower()}: {name.capitalize()}Create, service: {name.capitalize()}Service = Depends()):
    return await service.create({name.lower()})
'''
    controller_path.write_text(controller_content)
    click.echo(f"Controller {name} created successfully!")

@app.command(name="make:service")
@click.argument('name')
def make_service(name: str):
    """Create a new service file"""
    service_path = Path("app/services") / f"{name.lower()}.py"
    if service_path.exists():
        click.echo(f"Service {name} already exists!")
        return

    service_content = f'''from typing import List
from fastapi import Depends
from app.models.{name.lower()} import {name.capitalize()}
from app.schemas.{name.lower()} import {name.capitalize()}Create, {name.capitalize()}Response
from app.core.database import get_db
from sqlalchemy.orm import Session

class {name.capitalize()}Service:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    async def get_all(self) -> List[{name.capitalize()}Response]:
        {name.lower()}s = self.db.query({name.capitalize()}).all()
        return {name.lower()}s

    async def create(self, {name.lower()}: {name.capitalize()}Create) -> {name.capitalize()}Response:
        db_{name.lower()} = {name.capitalize()}(**{name.lower()}.dict())
        self.db.add(db_{name.lower()})
        self.db.commit()
        self.db.refresh(db_{name.lower()})
        return db_{name.lower()}
'''
    service_path.write_text(service_content)
    click.echo(f"Service {name} created successfully!")

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
def test():
    """Run tests"""
    os.system("pytest")

@app.command(name="seed")
def seed():
    """Seed the database with initial data"""
    # Add your seeding logic here
    click.echo("Database seeded successfully!")

@app.command(name="clear:cache")
def clear_cache():
    """Clear the application cache"""
    # Add your cache clearing logic here
    click.echo("Cache cleared successfully!")

if __name__ == '__main__':
    app() 