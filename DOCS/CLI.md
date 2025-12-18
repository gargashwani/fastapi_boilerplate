# CLI Commands

Command-line interface tools for the FastAPI Boilerplate.

## Installation

### Installing CLI Tools

```bash
# Install the package
pip install -e .

# Verify installation
python3 artisan --version
```

## Database Commands

### Migration Commands

```bash
# Create a new migration
python3 artisan make:migration "create users table"

# Run migrations
python3 artisan migrate

# Rollback last migration
python3 artisan migrate:rollback

# Show migration status
python3 artisan migrate:status

# Reset database
python3 artisan migrate:reset

# Refresh database
python3 artisan migrate:refresh
```

### Seed Commands

```bash
# Create a new seeder
python3 artisan make:seeder UsersSeeder

# Run seeders
python3 artisan db:seed

# Run specific seeder
python3 artisan db:seed --seeder=UsersSeeder

# Refresh and seed
python3 artisan db:refresh
```

## Model Commands

### Model Generation

```bash
# Create a new model
python3 artisan make:model User

# Create model with migration
python3 artisan make:model User --migration

# Create model with controller
python3 artisan make:model User --controller

# Create model with all components
python3 artisan make:model User --all
```

## Controller Commands

### Controller Generation

```bash
# Create a new controller
python3 artisan make:controller UserController

# Create resource controller
python3 artisan make:controller UserController --resource

# Create API controller
python3 artisan make:controller UserController --api
```

## Service Commands

### Service Generation

```bash
# Create a new service
python3 artisan make:service UserService

# Create service with interface
python3 artisan make:service UserService --interface
```

## Development Commands

### Development Tools

```bash
# Run development server
python3 artisan serve

# Run development server with reload
python3 artisan serve --reload

# Run tests
python3 artisan test

# Run specific test
python3 artisan test tests/test_users.py

# Generate API documentation
python3 artisan docs:generate

# Clear application cache
python3 artisan cache:clear

# View application logs
python3 artisan logs:view
```

## Custom Commands

### Creating Custom Commands

```python
from artisan import Command

class CustomCommand(Command):
    name = "custom:command"
    description = "Description of your custom command"

    def handle(self):
        # Command logic here
        self.info("Running custom command...")
        # Add your command implementation
        self.success("Command completed successfully")

# Register the command
Command.register(CustomCommand)
```
