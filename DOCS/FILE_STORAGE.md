# File Storage Guide

This guide explains how to use the Laravel-like file storage system in this FastAPI boilerplate.

## Table of Contents

1. [Introduction](#introduction)
2. [Configuration](#configuration)
3. [Basic Usage](#basic-usage)
4. [Storage Drivers](#storage-drivers)
5. [API Reference](#api-reference)
6. [Examples](#examples)

## Introduction

The boilerplate provides a powerful filesystem abstraction similar to Laravel's Storage facade. It uses PyFilesystem2 under the hood, allowing you to work with local filesystems, Amazon S3, FTP, SFTP, and more using the same simple API.

### Key Features

- **Unified API**: Same methods work with all storage drivers
- **Easy Switching**: Change storage driver via configuration
- **Laravel-like**: Familiar API for Laravel developers
- **Multiple Drivers**: Local, S3, FTP, SFTP support

## Configuration

### Environment Variables

Configure file storage in your `.env` file:

```env
# Default storage driver
FILESYSTEM_DISK=local  # Options: local, s3, ftp, sftp
FILESYSTEM_ROOT=storage/app  # Local storage root directory
FILESYSTEM_URL=  # Public URL for local storage (optional)
```

### Local Storage

Default driver for local file storage:

```env
FILESYSTEM_DISK=local
FILESYSTEM_ROOT=storage/app
FILESYSTEM_URL=http://localhost:8000/storage
```

### Amazon S3

For cloud storage with Amazon S3:

```env
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=your-bucket-name
AWS_ENDPOINT=  # Optional: for S3-compatible services
```

### FTP

For FTP server storage:

```env
FILESYSTEM_DISK=ftp
FTP_HOST=ftp.example.com
FTP_PORT=21
FTP_USERNAME=your-username
FTP_PASSWORD=your-password
```

### SFTP

For SFTP server storage:

```env
FILESYSTEM_DISK=sftp
SFTP_HOST=sftp.example.com
SFTP_PORT=22
SFTP_USERNAME=your-username
SFTP_PASSWORD=your-password
SFTP_KEY=/path/to/private/key  # Optional: SSH key path
```

## Basic Usage

### Import Storage

```python
from app.core.storage import storage
```

### Store Files

```python
# Store string content
storage().put('file.txt', 'Hello, World!')

# Store bytes
storage().put('file.bin', b'Binary content')

# Store from file-like object
with open('local_file.txt', 'rb') as f:
    storage().put('remote_file.txt', f.read())
```

### Retrieve Files

```python
# Get file content as bytes
content = storage().get('file.txt')

# Convert to string
text = content.decode('utf-8') if content else None
```

### Check File Existence

```python
if storage().exists('file.txt'):
    print("File exists")
```

### Delete Files

```python
storage().delete('file.txt')
```

### Get File URL

```python
url = storage().url('file.txt')
# Returns: http://localhost:8000/storage/file.txt (for local)
# Returns: https://bucket.s3.region.amazonaws.com/file.txt (for S3)
```

## Storage Drivers

### Switching Drivers

You can use different storage drivers in the same application:

```python
# Use default disk (from FILESYSTEM_DISK)
storage().put('file.txt', 'content')

# Use specific disk
storage('s3').put('file.txt', 'content')
storage('local').put('file.txt', 'content')
```

### Local Storage

Best for development and small applications:

```python
# Files stored in storage/app directory
storage('local').put('uploads/file.txt', 'content')
```

### Amazon S3

Best for production and scalable applications:

```python
# Files stored in S3 bucket
storage('s3').put('uploads/file.txt', 'content')
```

**Benefits:**
- Scalable storage
- CDN integration
- High availability
- Pay-as-you-go pricing

### FTP

For legacy systems or specific requirements:

```python
# Files stored on FTP server
storage('ftp').put('uploads/file.txt', 'content')
```

### SFTP

For secure file transfers:

```python
# Files stored on SFTP server
storage('sftp').put('uploads/file.txt', 'content')
```

## API Reference

### put(path, content, overwrite=True)

Store file content at given path.

**Parameters:**
- `path` (str): File path
- `content` (str|bytes|BinaryIO): File content
- `overwrite` (bool): Whether to overwrite existing file

**Returns:** `bool` - True if successful

**Example:**
```python
storage().put('file.txt', 'content')
storage().put('file.txt', 'content', overwrite=False)
```

### get(path)

Get file content.

**Parameters:**
- `path` (str): File path

**Returns:** `bytes|None` - File content or None if not found

**Example:**
```python
content = storage().get('file.txt')
```

### exists(path)

Check if file exists.

**Parameters:**
- `path` (str): File path

**Returns:** `bool` - True if file exists

**Example:**
```python
if storage().exists('file.txt'):
    print("Exists")
```

### delete(path)

Delete file.

**Parameters:**
- `path` (str): File path

**Returns:** `bool` - True if deleted successfully

**Example:**
```python
storage().delete('file.txt')
```

### copy(from_path, to_path)

Copy file from one location to another.

**Parameters:**
- `from_path` (str): Source path
- `to_path` (str): Destination path

**Returns:** `bool` - True if copied successfully

**Example:**
```python
storage().copy('old/file.txt', 'new/file.txt')
```

### move(from_path, to_path)

Move file from one location to another.

**Parameters:**
- `from_path` (str): Source path
- `to_path` (str): Destination path

**Returns:** `bool` - True if moved successfully

**Example:**
```python
storage().move('old/file.txt', 'new/file.txt')
```

### size(path)

Get file size in bytes.

**Parameters:**
- `path` (str): File path

**Returns:** `int|None` - File size or None if not found

**Example:**
```python
size = storage().size('file.txt')
```

### mime_type(path)

Get file MIME type.

**Parameters:**
- `path` (str): File path

**Returns:** `str|None` - MIME type or None if not found

**Example:**
```python
mime = storage().mime_type('file.txt')
# Returns: 'text/plain'
```

### last_modified(path)

Get file last modified timestamp.

**Parameters:**
- `path` (str): File path

**Returns:** `float|None` - Unix timestamp or None if not found

**Example:**
```python
timestamp = storage().last_modified('file.txt')
```

### files(directory='')

Get list of files in directory.

**Parameters:**
- `directory` (str): Directory path

**Returns:** `List[str]` - List of file paths

**Example:**
```python
files = storage().files('uploads/')
```

### directories(directory='')

Get list of directories.

**Parameters:**
- `directory` (str): Directory path

**Returns:** `List[str]` - List of directory paths

**Example:**
```python
dirs = storage().directories('uploads/')
```

### make_directory(path)

Create directory.

**Parameters:**
- `path` (str): Directory path

**Returns:** `bool` - True if created successfully

**Example:**
```python
storage().make_directory('uploads/2024/')
```

### delete_directory(path)

Delete directory and all contents.

**Parameters:**
- `path` (str): Directory path

**Returns:** `bool` - True if deleted successfully

**Example:**
```python
storage().delete_directory('uploads/old/')
```

### url(path)

Get public URL for file.

**Parameters:**
- `path` (str): File path

**Returns:** `str|None` - File URL or None if not available

**Example:**
```python
url = storage().url('file.txt')
```

## Examples

### Example 1: File Upload

```python
from fastapi import UploadFile
from app.core.storage import storage

async def upload_file(file: UploadFile):
    # Read file content
    content = await file.read()
    
    # Generate unique filename
    import uuid
    filename = f"{uuid.uuid4()}_{file.filename}"
    path = f"uploads/{filename}"
    
    # Store file
    storage().put(path, content)
    
    return {
        "path": path,
        "url": storage().url(path),
        "size": storage().size(path),
    }
```

### Example 2: File Download

```python
from fastapi.responses import StreamingResponse
from app.core.storage import storage
import io

def download_file(path: str):
    if not storage().exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    
    content = storage().get(path)
    filename = path.split('/')[-1]
    
    return StreamingResponse(
        io.BytesIO(content),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
```

### Example 3: Image Processing

```python
from app.core.storage import storage
from PIL import Image
import io

def process_image(path: str):
    # Get image from storage
    content = storage().get(path)
    if not content:
        return None
    
    # Process image
    image = Image.open(io.BytesIO(content))
    image.thumbnail((800, 800))
    
    # Save processed image
    output = io.BytesIO()
    image.save(output, format='JPEG')
    output.seek(0)
    
    # Store processed image
    processed_path = f"processed/{path}"
    storage().put(processed_path, output.read())
    
    return processed_path
```

### Example 4: Backup to S3

```python
from app.core.storage import storage

def backup_to_s3(local_path: str, s3_path: str):
    # Get file from local storage
    content = storage('local').get(local_path)
    if not content:
        return False
    
    # Store in S3
    return storage('s3').put(s3_path, content)
```

### Example 5: File Cleanup

```python
from app.core.storage import storage
from datetime import datetime, timedelta

def cleanup_old_files(directory: str, days: int = 30):
    """Delete files older than specified days."""
    cutoff = datetime.now() - timedelta(days=days)
    
    files = storage().files(directory)
    deleted = 0
    
    for file_path in files:
        last_modified = storage().last_modified(file_path)
        if last_modified:
            file_time = datetime.fromtimestamp(last_modified)
            if file_time < cutoff:
                storage().delete(file_path)
                deleted += 1
    
    return deleted
```

### Example 6: Directory Operations

```python
from app.core.storage import storage

# Create directory structure
storage().make_directory('uploads/2024/01/')
storage().make_directory('uploads/2024/02/')

# List all files
all_files = storage().files('uploads/')

# List directories
directories = storage().directories('uploads/')

# Delete entire directory
storage().delete_directory('uploads/old/')
```

## Best Practices

1. **Use Unique Filenames**: Generate unique filenames to avoid conflicts
   ```python
   import uuid
   filename = f"{uuid.uuid4()}_{original_filename}"
   ```

2. **Organize by Structure**: Use directory structure for organization
   ```python
   path = f"uploads/{user_id}/{year}/{month}/{filename}"
   ```

3. **Validate File Types**: Always validate file types before storing
   ```python
   ALLOWED_EXTENSIONS = {'jpg', 'png', 'pdf'}
   if file.filename.split('.')[-1] not in ALLOWED_EXTENSIONS:
       raise ValueError("File type not allowed")
   ```

4. **Handle Errors**: Always check return values
   ```python
   if not storage().put(path, content):
       raise Exception("Failed to store file")
   ```

5. **Use Appropriate Driver**: 
   - Local for development
   - S3 for production
   - FTP/SFTP for specific requirements

6. **Clean Up**: Regularly clean up old files
   ```python
   # Delete files older than 30 days
   cleanup_old_files('uploads/', days=30)
   ```

## Troubleshooting

### File Not Found

```python
if not storage().exists(path):
    raise HTTPException(status_code=404, detail="File not found")
```

### Permission Errors

Ensure storage directory has proper permissions:
```bash
chmod -R 755 storage/
```

### S3 Connection Issues

- Verify AWS credentials
- Check bucket permissions
- Verify region settings

### Large Files

For large files, consider streaming:
```python
# For very large files, use chunked upload
with open('large_file.bin', 'rb') as f:
    storage().put('large_file.bin', f.read())
```

## Additional Resources

- [PyFilesystem2 Documentation](https://docs.pyfilesystem.org/)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [FastAPI File Uploads](https://fastapi.tiangolo.com/tutorial/request-files/)

