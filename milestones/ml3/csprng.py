import os

def generate_random_bytes(num_bytes):
    """
    Generates cryptographically secure random bytes using os.urandom()
    
    Args:
        num_bytes (int): Number of bytes to generate
        
    Returns:
        bytes: Random byte string
        
    Raises:
        ValueError: If num_bytes <= 0
        RuntimeError: If random generation fails
    """
    if num_bytes <= 0:
        raise ValueError("Number of bytes must be positive")
    
    try:
        return os.urandom(num_bytes)
    except Exception as e:
        raise RuntimeError(f"Failed to generate random bytes: {str(e)}")

def bytes_to_hex(byte_string):
    """Convert bytes to hexadecimal string"""
    return byte_string.hex()

def hex_to_bytes(hex_string):
    """Convert hexadecimal string to bytes"""
    return bytes.fromhex(hex_string)

# Test function for demonstration
def test_csprng():
    """Test the CSPRNG functions"""
    print("Testing CSPRNG...")
    
    # Test basic generation
    random_bytes = generate_random_bytes(16)
    print(f"Generated 16 bytes: {len(random_bytes)}")
    
    # Test conversion
    hex_string = bytes_to_hex(random_bytes)
    print(f"Hex representation: {hex_string}")
    
    # Test back conversion
    back_to_bytes = hex_to_bytes(hex_string)
    print(f"Back to bytes matches: {random_bytes == back_to_bytes}")
    
    # Test uniqueness
    unique_test = set()
    for i in range(10):
        unique_test.add(generate_random_bytes(16))
    print(f"Generated {len(unique_test)} unique random sequences")

if __name__ == "__main__":
    test_csprng()