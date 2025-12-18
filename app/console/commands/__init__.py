"""
Console Commands
Laravel-like command structure for FastAPI Boilerplate
"""
import click
from app.console.commands.serve import serve
from app.console.commands.key_generate import key_generate
from app.console.commands.migration import (
    make_migration, migrate, migrate_status, migrate_rollback,
    migrate_reset, migrate_refresh
)
from app.console.commands.make import (
    make_model, make_controller, make_service, make_schema,
    make_middleware, make_exception, make_validator, make_repository, make_seeder
)
from app.console.commands.test import test
from app.console.commands.cache import clear_cache
from app.console.commands.logs import view_logs, clear_logs
from app.console.commands.schedule import schedule_run, schedule_list
from app.console.commands.seeder import db_seed, db_refresh
from app.console.commands.docs import generate_docs
from app.console.commands.database import db_create, db_drop
from app.console.commands.database import db_create, db_drop

@click.group()
def app():
    """FastAPI Boilerplate CLI"""
    pass

# Register all commands
app.add_command(serve)
app.add_command(key_generate)
app.add_command(make_migration)
app.add_command(migrate)
app.add_command(migrate_status)
app.add_command(migrate_rollback)
app.add_command(migrate_reset)
app.add_command(migrate_refresh)
app.add_command(make_model)
app.add_command(make_controller)
app.add_command(make_service)
app.add_command(make_schema)
app.add_command(test)
app.add_command(clear_cache)
app.add_command(view_logs)
app.add_command(clear_logs)
app.add_command(make_middleware)
app.add_command(make_exception)
app.add_command(make_validator)
app.add_command(make_repository)
app.add_command(generate_docs)
app.add_command(make_seeder)
app.add_command(db_seed)
app.add_command(db_refresh)
app.add_command(db_create)
app.add_command(db_drop)
app.add_command(schedule_run)
app.add_command(schedule_list)

__all__ = ['app']

