# Task Scheduling Guide

This guide explains how to use the Laravel-like task scheduling system in this FastAPI boilerplate.

## Table of Contents

1. [Introduction](#introduction)
2. [Defining Schedules](#defining-schedules)
3. [Schedule Frequency Options](#schedule-frequency-options)
4. [Task Types](#task-types)
5. [Task Modifiers](#task-modifiers)
6. [Running the Scheduler](#running-the-scheduler)
7. [Examples](#examples)

## Introduction

The boilerplate provides a powerful task scheduling system similar to Laravel's scheduler. Tasks are defined in `app/console/kernel.py` and can be scheduled to run at specific intervals.

### Key Features

- **Laravel-like API**: Familiar scheduling syntax
- **Multiple Frequency Options**: Every minute, hourly, daily, weekly, etc.
- **Task Types**: Commands, jobs, and shell commands
- **Timezone Support**: Schedule tasks in specific timezones
- **Overlap Prevention**: Prevent tasks from overlapping
- **Conditional Execution**: Run tasks based on conditions
- **Task Hooks**: Before and after callbacks

## Defining Schedules

All scheduled tasks are defined in `app/console/kernel.py` in the `schedule_tasks()` function:

```python
from app.core.scheduler import schedule

def schedule_tasks():
    """Define all scheduled tasks here."""
    
    # Schedule a task to run every minute
    schedule().job(example_task).every_minute()
    
    # Schedule a task to run daily
    schedule().job(cleanup_old_files).daily()
    
    # Schedule a task to run hourly
    schedule().job(process_queue).hourly()
```

## Schedule Frequency Options

### Minute-based Frequencies

```python
schedule().job(task).every_minute()
schedule().job(task).every_two_minutes()
schedule().job(task).every_five_minutes()
schedule().job(task).every_ten_minutes()
schedule().job(task).every_fifteen_minutes()
schedule().job(task).every_thirty_minutes()
```

### Hourly Frequencies

```python
schedule().job(task).hourly()
schedule().job(task).hourly_at(30)  # At :30 past the hour
```

### Daily Frequencies

```python
schedule().job(task).daily()
schedule().job(task).daily_at('09:00')
schedule().job(task).daily_at('14:30')
schedule().job(task).twice_daily(1, 13)  # At 1:00 and 13:00
```

### Weekly Frequencies

```python
schedule().job(task).weekly()
schedule().job(task).weekly_on('monday', '09:00')
schedule().job(task).weekly_on('friday', '17:00')
```

### Monthly Frequencies

```python
schedule().job(task).monthly()
schedule().job(task).monthly_on(15, '09:00')  # 15th of month at 9 AM
```

### Other Frequencies

```python
schedule().job(task).quarterly()  # Every 3 months
schedule().job(task).yearly()     # January 1st
schedule().job(task).every(30)    # Every 30 seconds
```

### Custom Cron Expression

```python
schedule().job(task).cron('0 0 * * *')  # Daily at midnight
schedule().job(task).cron('0 */6 * * *')  # Every 6 hours
schedule().job(task).cron('0 9 * * 1-5')  # 9 AM on weekdays
```

## Task Types

### Scheduling Jobs (Functions)

```python
def send_daily_report():
    """Send daily report."""
    # Your logic here
    pass

schedule().job(send_daily_report).daily_at('09:00')
```

### Scheduling Commands

```python
# Schedule an Artisan command
schedule().command('cache:clear').daily()
schedule().command('backup:run').daily_at('02:00')
```

### Scheduling Shell Commands

```python
# Schedule a shell command
schedule().exec('python manage.py cleanup').daily()
schedule().exec('php artisan backup:run').hourly()
```

## Task Modifiers

### Timezone

```python
schedule().job(task).daily_at('09:00').timezone('America/New_York')
schedule().job(task).hourly().timezone('Europe/London')
```

### Without Overlapping

Prevent task from overlapping with previous execution:

```python
schedule().job(long_running_task).hourly().without_overlapping()
schedule().job(task).daily().without_overlapping(expiration=120)  # 2 hours expiration
```

### On One Server

Run task on only one server (for multi-server deployments):

```python
schedule().job(task).daily().on_one_server()
```

### Run in Background

```python
schedule().job(task).daily().run_in_background()
```

### Conditional Execution

```python
# Run only when condition is true
schedule().job(task).daily().when(lambda: some_condition())

# Skip when condition is true
schedule().job(task).daily().skip(lambda: maintenance_mode())
```

### Task Hooks

```python
def before_task():
    print("Task is about to run")

def after_task():
    print("Task completed")

schedule().job(task).daily().before(before_task).after(after_task)
```

### Output Management

```python
# Append output to file
schedule().job(task).daily().append_output_to('logs/task.log')

# Send output to file (overwrite)
schedule().job(task).daily().send_output_to('logs/task.log')

# Email output
schedule().job(task).daily().email_output_to('admin@example.com')
```

## Running the Scheduler

### Development

Run the scheduler manually:

```bash
python artisan schedule:run
```

Or use the CLI:

```bash
./artisan schedule:run
```

### Production

For production, you should run the scheduler as a background service. The scheduler needs to run continuously.

**Option 1: Using systemd (Linux)**

Create `/etc/systemd/system/scheduler.service`:

```ini
[Unit]
Description=FastAPI Task Scheduler
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/your/app
ExecStart=/path/to/venv/bin/python artisan schedule:run
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable scheduler
sudo systemctl start scheduler
```

**Option 2: Using Supervisor**

Create `/etc/supervisor/conf.d/scheduler.conf`:

```ini
[program:scheduler]
command=/path/to/venv/bin/python artisan schedule:run
directory=/path/to/your/app
autostart=true
autorestart=true
user=www-data
```

**Option 3: Using Docker**

```dockerfile
# In your Dockerfile or docker-compose.yml
CMD ["python", "artisan", "schedule:run"]
```

### List Scheduled Tasks

View all scheduled tasks:

```bash
python artisan schedule:list
```

## Examples

### Example 1: Daily Cleanup

```python
def cleanup_old_files():
    """Clean up old files daily."""
    from app.core.storage import storage
    from datetime import datetime, timedelta
    
    cutoff = datetime.now() - timedelta(days=30)
    files = storage().files('uploads/')
    
    for file_path in files:
        last_modified = storage().last_modified(file_path)
        if last_modified and datetime.fromtimestamp(last_modified) < cutoff:
            storage().delete(file_path)

schedule().job(cleanup_old_files).daily_at('02:00')
```

### Example 2: Hourly Queue Processing

```python
def process_queue():
    """Process queued items hourly."""
    from app.workers.tasks import process_pending_tasks
    process_pending_tasks()

schedule().job(process_queue).hourly()
```

### Example 3: Weekly Backup

```python
def weekly_backup():
    """Run weekly backup."""
    import subprocess
    subprocess.run(['python', 'backup.py'])

schedule().job(weekly_backup).weekly_on('sunday', '02:00')
```

### Example 4: Cache Clearing

```python
def clear_cache():
    """Clear cache every 5 minutes."""
    from app.core.cache import cache
    cache().flush()

schedule().job(clear_cache).every_five_minutes()
```

### Example 5: Conditional Task

```python
def send_notification():
    """Send notification only during business hours."""
    # Your notification logic
    pass

def is_business_hours():
    from datetime import datetime
    hour = datetime.now().hour
    return 9 <= hour <= 17

schedule().job(send_notification).every_minute().when(is_business_hours)
```

### Example 6: Task with Hooks

```python
def before_backup():
    logger.info("Starting backup...")

def after_backup():
    logger.info("Backup completed!")

def run_backup():
    # Backup logic
    pass

schedule().job(run_backup).daily().before(before_backup).after(after_backup)
```

### Example 7: Multiple Tasks

```python
def schedule_tasks():
    # Cleanup tasks
    schedule().job(cleanup_old_files).daily_at('02:00')
    schedule().job(cleanup_logs).weekly()
    
    # Processing tasks
    schedule().job(process_queue).every_five_minutes()
    schedule().job(process_payments).hourly()
    
    # Reporting tasks
    schedule().job(send_daily_report).daily_at('09:00')
    schedule().job(send_weekly_report).weekly_on('monday', '09:00')
    
    # Maintenance tasks
    schedule().job(clear_cache).every_fifteen_minutes()
    schedule().job(optimize_database).monthly()
```

## Best Practices

1. **Keep Tasks Lightweight**: Schedule tasks should complete quickly
2. **Use Background Jobs**: For long-running tasks, queue them instead
3. **Handle Errors**: Always include error handling in scheduled tasks
4. **Log Everything**: Log task execution for debugging
5. **Use Without Overlapping**: For tasks that might take longer than the interval
6. **Test Locally**: Test scheduled tasks before deploying
7. **Monitor Execution**: Set up monitoring for scheduled tasks

## Troubleshooting

### Task Not Running

1. Check if scheduler is running: `python artisan schedule:list`
2. Check logs for errors
3. Verify task is defined in `kernel.py`
4. Check timezone settings

### Task Overlapping

Use `without_overlapping()`:

```python
schedule().job(task).hourly().without_overlapping()
```

### Task Running on Multiple Servers

Use `on_one_server()`:

```python
schedule().job(task).daily().on_one_server()
```

## Additional Resources

- [APScheduler Documentation](https://apscheduler.readthedocs.io/)
- [Laravel Task Scheduling](https://laravel.com/docs/scheduling)

