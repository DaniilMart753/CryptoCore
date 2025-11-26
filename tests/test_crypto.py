import sys
import os
import tempfile

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from crypto import encrypt_file, decrypt_file
from file_utils import write_file, read_file

def test_encrypt_decrypt_roundtrip():
    test_content = b"Hello, CryptoCore! This is a test message for encryption."
    
    with tempfile.NamedTemporaryFile(delete=False, mode='wb', suffix='.txt') as f:
        input_file = f.name
        f.write(test_content)
    
    try:
        encrypted_file = input_file + '.enc'
        decrypted_file = input_file + '.dec'
        
        test_key = "00112233445566778899aabbccddeeff"
        
        used_key, used_iv = encrypt_file(
            algorithm='aes',
            mode='cbc',
            key_hex=test_key,
            input_file=input_file,
            output_file=encrypted_file
        )
        
        assert used_key == test_key
        assert used_iv is not None
        
        encrypted_data = read_file(encrypted_file)
        assert len(encrypted_data) >= 16
        
        decrypt_file(
            algorithm='aes',
            mode='cbc', 
            key_hex=test_key,
            input_file=encrypted_file,
            output_file=decrypted_file
        )
        
        decrypted_data = read_file(decrypted_file)
        assert decrypted_data == test_content
        
        print("Encrypt/decrypt roundtrip test passed")
        
    finally:
        for file_path in [input_file, encrypted_file, decrypted_file]:
            if os.path.exists(file_path):
                os.unlink(file_path)

def test_auto_key_generation():
    test_content = b"Test for auto key generation"
    
    with tempfile.NamedTemporaryFile(delete=False, mode='wb', suffix='.txt') as f:
        input_file = f.name
        f.write(test_content)
    
    try:
        encrypted_file = input_file + '.enc'
        decrypted_file = input_file + '.dec'
        
        used_key, used_iv = encrypt_file(
            algorithm='aes',
            mode='ctr',
            key_hex=None,
            input_file=input_file,
            output_file=encrypted_file
        )
        
        assert used_key is not None
        assert len(used_key) == 32
        assert used_iv is not None
        
        print(f"Generated key: {used_key}")
        
        decrypt_file(
            algorithm='aes',
            mode='ctr',
            key_hex=used_key,
            input_file=encrypted_file,
            output_file=decrypted_file
        )
        
        decrypted_data = read_file(decrypted_file)
        assert decrypted_data == test_content
        
        print("Auto key generation test passed")
        
    finally:
        for file_path in [input_file, encrypted_file, decrypted_file]:
            if os.path.exists(file_path):
                os.unlink(file_path)

def test_different_modes():
    test_content = b"Testing different modes"
    test_key = "0123456789abcdef0123456789abcdef"
    
    modes_to_test = ['ecb', 'cbc', 'cfb', 'ofb', 'ctr']
    
    with tempfile.NamedTemporaryFile(delete=False, mode='wb', suffix='.txt') as f:
        input_file = f.name
        f.write(test_content)
    
    try:
        for mode in modes_to_test:
            encrypted_file = f"{input_file}.{mode}.enc"
            decrypted_file = f"{input_file}.{mode}.dec"
            
            encrypt_file(
                algorithm='aes',
                mode=mode,
                key_hex=test_key,
                input_file=input_file,
                output_file=encrypted_file
            )
            
            decrypt_file(
                algorithm='aes',
                mode=mode,
                key_hex=test_key, 
                input_file=encrypted_file,
                output_file=decrypted_file
            )
            
            decrypted_data = read_file(decrypted_file)
            assert decrypted_data == test_content
            
            print(f"{mode.upper()} mode test passed")
            
    finally:
        for file_path in [input_file]:
            if os.path.exists(file_path):
                os.unlink(file_path)
        for mode in modes_to_test:
            for ext in ['.enc', '.dec']:
                file_path = f"{input_file}.{mode}{ext}"
                if os.path.exists(file_path):
                    os.unlink(file_path)

def run_all_tests():
    print("Starting crypto tests")
    
    test_encrypt_decrypt_roundtrip()
    test_auto_key_generation() 
    test_different_modes()
    
    print("All crypto tests passed successfully")

if __name__ == "__main__":
    run_all_tests()