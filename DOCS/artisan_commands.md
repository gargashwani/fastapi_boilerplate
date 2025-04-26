# Start the development server
./artisan.py serve

# Generate a new application key
./artisan.py key_generate

# Create a new model
./artisan.py make_model User

# Create a new controller
./artisan.py make_controller User

# Create a new service
./artisan.py make_service User

# Create a new schema
./artisan.py make_schema User

# Create and run migrations
./artisan.py make_migration "create users table"
./artisan.py migrate

# Run tests
./artisan.py test