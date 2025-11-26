import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.csprng import generate_random_bytes, bytes_to_hex

def test_key_uniqueness():
    """Test that generated keys are unique"""
    key_set = set()
    num_keys = 1000
    
    for _ in range(num_keys):
        key = generate_random_bytes(16)
        key_hex = bytes_to_hex(key)
        
        # Check for uniqueness
        assert key_hex not in key_set, f"Duplicate key found: {key_hex}"
        key_set.add(key_hex)
    
    print(f"✓ Successfully generated {len(key_set)} unique keys")

def test_randomness_basic():
    """Basic randomness test - check bit distribution"""
    total_bits = 0
    total_ones = 0
    num_samples = 100
    
    for _ in range(num_samples):
        random_bytes = generate_random_bytes(16)
        # Count ones in binary representation
        for byte in random_bytes:
            binary = bin(byte)[2:].zfill(8)
            total_ones += binary.count('1')
            total_bits += 8
    
    ones_ratio = total_ones / total_bits
    print(f"✓ Bit distribution: {ones_ratio:.3f} (should be close to 0.5)")
    
    # Should be roughly 50% ones and zeros
    assert 0.45 < ones_ratio < 0.55, f"Poor bit distribution: {ones_ratio}"

def test_nist_preparation():
    """Generate large random file for NIST testing"""
    total_size = 10_000_000  # 10 MB
    output_file = "nist_test_data.bin"
    
    with open(output_file, 'wb') as f:
        bytes_written = 0
        while bytes_written < total_size:
            chunk_size = min(4096, total_size - bytes_written)
            random_chunk = generate_random_bytes(chunk_size)
            f.write(random_chunk)
            bytes_written += chunk_size
    
    print(f"✓ Generated {bytes_written} bytes for NIST testing in '{output_file}'")

if __name__ == "__main__":
    print("Testing CSPRNG...")
    test_key_uniqueness()
    test_randomness_basic()
    test_nist_preparation()
    print("All CSPRNG tests passed! ✓")