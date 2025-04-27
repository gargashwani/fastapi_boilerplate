# Artisan Commands

## Development Server
```bash
# Start the development server
./artisan serve

# Start with auto-reload enabled
./artisan serve --reload
```

## Testing
```bash
# Run all tests
./artisan test

# Run specific test file
./artisan test tests/test_users.py
```

## Documentation
```bash
# Generate API documentation
./artisan docs:generate
```

## Database
```bash
# Create a new model (with optional migration)
./artisan make:model User --migration

# Create and run migrations
./artisan make:migration "create users table"
./artisan migrate
./artisan migrate:status
./artisan migrate:rollback

# Reset and refresh database
./artisan migrate:reset    # Rollback all migrations
./artisan migrate:refresh  # Rollback all and run all migrations
```

## Database Seeding

### Create a new seeder
```bash
python3 artisan make:seeder UsersSeeder
```
This will create a new seeder file in `app/seeders/usersseeder.py` with sample data.

### Run all seeders
```bash
python3 artisan db:seed
```
This will run all seeders in the `app/seeders` directory.

### Run specific seeder
```bash
python3 artisan db:seed --seeder=UsersSeeder
```
This will run only the specified seeder.

### Refresh database and seed
```bash
python3 artisan db:refresh
```
This will:
1. Rollback all migrations
2. Run all migrations
3. Run all seeders

## Code Generation
```bash
# Create a new service
./artisan make:service UserService

# Create service with interface
./artisan make:service UserService --interface

# Create a new controller
./artisan make:controller User

# Create a new schema
./artisan make:schema User

# Create a new middleware
./artisan make:middleware Auth

# Create a new exception
./artisan make:exception NotFound

# Create a new validator
./artisan make:validator User

# Create a new repository
./artisan make:repository User
```

## Maintenance
```bash
# Generate a new application key
./artisan key:generate

# Clear application cache
./artisan cache:clear

# View application logs
./artisan logs:view

# Clear application logs
./artisan logs:clear

# Seed the database
./artisan seed