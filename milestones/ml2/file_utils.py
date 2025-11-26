import os

def read_file(filename):
    """
    Read entire file content as bytes
    
    Args:
        filename (str): Path to file
        
    Returns:
        bytes: File content
        
    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If file cannot be read
    """
    try:
        with open(filename, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filename}")
    except Exception as e:
        raise IOError(f"Error reading file {filename}: {str(e)}")

def write_file(filename, data):
    """
    Write data to file
    
    Args:
        filename (str): Path to file
        data (bytes): Data to write
        
    Raises:
        IOError: If file cannot be written
    """
    try:
        # Create directory if it doesn't exist (only if path contains directories)
        dir_name = os.path.dirname(filename)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
        
        with open(filename, 'wb') as f:
            f.write(data)
    except Exception as e:
        raise IOError(f"Error writing file {filename}: {str(e)}")

def read_file_chunks(filename, chunk_size=4096):
    """
    Read file in chunks (generator)
    
    Args:
        filename (str): Path to file
        chunk_size (int): Size of each chunk
        
    Yields:
        bytes: File chunks
    """
    try:
        with open(filename, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filename}")
    except Exception as e:
        raise IOError(f"Error reading file {filename}: {str(e)}")

def file_exists(filename):
    """Check if file exists"""
    return os.path.exists(filename)

def get_file_size(filename):
    """Get file size in bytes"""
    return os.path.getsize(filename)

# Test function
def test_file_utils():
    """Test file utility functions"""
    test_filename = "test_file_utils.txt"
    test_data = b"Hello, CryptoCore! This is a test."
    
    try:
        # Test write and read
        write_file(test_filename, test_data)
        print(f"✓ File written: {test_filename}")
        
        # Test read
        read_back = read_file(test_filename)
        print(f"✓ File read: {len(read_back)} bytes")
        
        # Test chunk reading
        chunks = list(read_file_chunks(test_filename, chunk_size=10))
        print(f"✓ Chunk reading: {len(chunks)} chunks")
        
        # Test file exists
        if file_exists(test_filename):
            print(f"✓ File exists check")
        
        # Test file size
        size = get_file_size(test_filename)
        print(f"✓ File size: {size} bytes")
        
        # Cleanup
        os.remove(test_filename)
        print("✓ Test cleanup completed")
        
    except Exception as e:
        print(f"✗ Test failed: {e}")

if __name__ == "__main__":
    test_file_utils()