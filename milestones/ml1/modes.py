from Crypto.Cipher import AES
from utils import pkcs7_pad, pkcs7_unpad

# ECB Mode
def ecb_encrypt(plaintext, key):
    """ECB mode encryption"""
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plaintext = pkcs7_pad(plaintext)
    ciphertext = b''
    
    for i in range(0, len(padded_plaintext), 16):
        block = padded_plaintext[i:i+16]
        encrypted_block = cipher.encrypt(block)
        ciphertext += encrypted_block
    
    return ciphertext

def ecb_decrypt(ciphertext, key):
    """ECB mode decryption"""
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = b''
    
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i+16]
        decrypted_block = cipher.decrypt(block)
        plaintext += decrypted_block
    
    return pkcs7_unpad(plaintext)

# CBC Mode
def cbc_encrypt(plaintext, key, iv):
    """CBC mode encryption"""
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plaintext = pkcs7_pad(plaintext)
    ciphertext = b''
    prev_block = iv
    
    for i in range(0, len(padded_plaintext), 16):
        block = padded_plaintext[i:i+16]
        # XOR with previous ciphertext block (or IV for first block)
        xor_block = bytes(a ^ b for a, b in zip(block, prev_block))
        encrypted_block = cipher.encrypt(xor_block)
        ciphertext += encrypted_block
        prev_block = encrypted_block
    
    return ciphertext

def cbc_decrypt(ciphertext, key, iv):
    """CBC mode decryption"""
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = b''
    prev_block = iv
    
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i+16]
        decrypted_block = cipher.decrypt(block)
        # XOR with previous ciphertext block (or IV for first block)
        plain_block = bytes(a ^ b for a, b in zip(decrypted_block, prev_block))
        plaintext += plain_block
        prev_block = block
    
    return pkcs7_unpad(plaintext)

# CFB Mode
def cfb_encrypt(plaintext, key, iv):
    """CFB mode encryption (stream cipher)"""
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = b''
    feedback = iv
    
    for i in range(0, len(plaintext), 16):
        block = plaintext[i:i+16]
        # Encrypt the feedback register
        encrypted_feedback = cipher.encrypt(feedback)
        # XOR with plaintext to produce ciphertext
        cipher_block = bytes(a ^ b for a, b in zip(block, encrypted_feedback))
        ciphertext += cipher_block
        # Update feedback register with ciphertext
        feedback = cipher_block
    
    return ciphertext

def cfb_decrypt(ciphertext, key, iv):
    """CFB mode decryption (stream cipher)"""
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = b''
    feedback = iv
    
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i+16]
        # Encrypt the feedback register
        encrypted_feedback = cipher.encrypt(feedback)
        # XOR with ciphertext to produce plaintext
        plain_block = bytes(a ^ b for a, b in zip(block, encrypted_feedback))
        plaintext += plain_block
        # Update feedback register with ciphertext
        feedback = block
    
    return plaintext

# OFB Mode
def ofb_encrypt(plaintext, key, iv):
    """OFB mode encryption (stream cipher)"""
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = b''
    feedback = iv
    
    for i in range(0, len(plaintext), 16):
        block = plaintext[i:i+16]
        # Encrypt the feedback register to generate keystream
        keystream = cipher.encrypt(feedback)
        # XOR with plaintext to produce ciphertext
        cipher_block = bytes(a ^ b for a, b in zip(block, keystream))
        ciphertext += cipher_block
        # Update feedback register with keystream
        feedback = keystream
    
    return ciphertext

def ofb_decrypt(ciphertext, key, iv):
    """OFB mode decryption (stream cipher)"""
    # OFB decryption is identical to encryption
    return ofb_encrypt(ciphertext, key, iv)

# CTR Mode
def ctr_encrypt(plaintext, key, iv):
    """CTR mode encryption (stream cipher)"""
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = b''
    
    for i in range(0, len(plaintext), 16):
        block = plaintext[i:i+16]
        # Encrypt the counter (IV + block counter)
        counter = int.from_bytes(iv, 'big') + (i // 16)
        counter_bytes = counter.to_bytes(16, 'big')
        keystream = cipher.encrypt(counter_bytes)
        # XOR with plaintext to produce ciphertext
        cipher_block = bytes(a ^ b for a, b in zip(block, keystream))
        ciphertext += cipher_block
    
    return ciphertext

def ctr_decrypt(ciphertext, key, iv):
    """CTR mode decryption (stream cipher)"""
    # CTR decryption is identical to encryption
    return ctr_encrypt(ciphertext, key, iv)

# Test function
def test_modes():
    """Test all encryption modes"""
    key = b'\x00' * 16  # Test key
    iv = b'\x00' * 16   # Test IV
    test_data = b"Hello, CryptoCore! This is a test message."
    
    print("Testing encryption modes...")
    
    # Test each mode
    modes = [
        ('ECB', ecb_encrypt, ecb_decrypt),
        ('CBC', cbc_encrypt, cbc_decrypt),
        ('CFB', cfb_encrypt, cfb_decrypt),
        ('OFB', ofb_encrypt, ofb_decrypt),
        ('CTR', ctr_encrypt, ctr_decrypt)
    ]
    
    for mode_name, encrypt_func, decrypt_func in modes:
        try:
            if mode_name == 'ECB':
                encrypted = encrypt_func(test_data, key)
                decrypted = decrypt_func(encrypted, key)
            else:
                encrypted = encrypt_func(test_data, key, iv)
                decrypted = decrypt_func(encrypted, key, iv)
            
            if decrypted == test_data:
                print(f"✓ {mode_name} mode: PASS")
            else:
                print(f"✗ {mode_name} mode: FAIL")
                
        except Exception as e:
            print(f"✗ {mode_name} mode: ERROR - {e}")

if __name__ == "__main__":
    test_modes()