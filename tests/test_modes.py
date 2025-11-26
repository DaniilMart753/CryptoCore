import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from modes import *

def test_ecb_mode():
    key = b'\x00' * 16
    test_data = b"Hello, ECB Mode! Testing 123"
    
    encrypted = ecb_encrypt(test_data, key)
    assert len(encrypted) % 16 == 0
    
    decrypted = ecb_decrypt(encrypted, key)
    assert decrypted == test_data
    
    print("ECB mode test passed")

def test_cbc_mode():
    key = b'\x01' * 16
    iv = b'\xff' * 16
    test_data = b"Hello, CBC Mode! Testing 456"
    
    encrypted = cbc_encrypt(test_data, key, iv)
    decrypted = cbc_decrypt(encrypted, key, iv)
    
    assert decrypted == test_data
    print("CBC mode test passed")

def test_cfb_mode():
    key = b'\x02' * 16
    iv = b'\xfe' * 16
    test_data = b"Hello, CFB! Short"
    
    encrypted = cfb_encrypt(test_data, key, iv)
    decrypted = cfb_decrypt(encrypted, key, iv)
    
    assert decrypted == test_data
    assert len(encrypted) == len(test_data)
    print("CFB mode test passed")

def test_ofb_mode():
    key = b'\x03' * 16
    iv = b'\xfd' * 16
    test_data = b"Hello, OFB! Test message"
    
    encrypted = ofb_encrypt(test_data, key, iv)
    decrypted = ofb_decrypt(encrypted, key, iv)
    
    assert decrypted == test_data
    assert len(encrypted) == len(test_data)
    print("OFB mode test passed")

def test_ctr_mode():
    key = b'\x04' * 16
    iv = b'\xfc' * 16
    test_data = b"Hello, CTR! Counter mode"
    
    encrypted = ctr_encrypt(test_data, key, iv)
    decrypted = ctr_decrypt(encrypted, key, iv)
    
    assert decrypted == test_data
    assert len(encrypted) == len(test_data)
    print("CTR mode test passed")

def test_modes_with_different_lengths():
    key = b'\x05' * 16
    iv = b'\xfb' * 16
    
    test_cases = [
        b"",
        b"A",
        b"Short",
        b"Exactly16Bytes!!",
        b"More than 16 bytes for testing padding",
    ]
    
    modes = [
        ('ECB', ecb_encrypt, ecb_decrypt, False),
        ('CBC', cbc_encrypt, cbc_decrypt, True),
        ('CFB', cfb_encrypt, cfb_decrypt, False),
        ('OFB', ofb_encrypt, ofb_decrypt, False),
        ('CTR', ctr_encrypt, ctr_decrypt, False),
    ]
    
    for mode_name, encrypt_func, decrypt_func, uses_iv in modes:
        for test_data in test_cases:
            if uses_iv:
                encrypted = encrypt_func(test_data, key, iv)
                decrypted = decrypt_func(encrypted, key, iv)
            else:
                encrypted = encrypt_func(test_data, key)
                decrypted = decrypt_func(encrypted, key)
            
            assert decrypted == test_data

    print("All modes work with different input lengths")

def run_all_tests():
    print("Starting mode tests")
    
    test_ecb_mode()
    test_cbc_mode()
    test_cfb_mode()
    test_ofb_mode()
    test_ctr_mode()
    test_modes_with_different_lengths()
    
    print("All mode tests passed successfully")

if __name__ == "__main__":
    run_all_tests()