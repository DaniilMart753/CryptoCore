import os
from Crypto.Cipher import AES
from modes import ecb_encrypt, ecb_decrypt, cbc_encrypt, cbc_decrypt, cfb_encrypt, cfb_decrypt, ofb_encrypt, ofb_decrypt, ctr_encrypt, ctr_decrypt
from file_utils import read_file, write_file, read_file_chunks
from csprng import generate_random_bytes, bytes_to_hex
from utils import pkcs7_pad, pkcs7_unpad

def pkcs7_pad(data, block_size=16):
    """Pad data using PKCS#7 standard"""
    padding_length = block_size - (len(data) % block_size)
    if padding_length == 0:
        padding_length = block_size
    padding = bytes([padding_length] * padding_length)
    return data + padding

def pkcs7_unpad(data):
    """Remove PKCS#7 padding"""
    if len(data) == 0:
        return data
    padding_length = data[-1]
    # Validate padding
    if padding_length == 0 or padding_length > len(data):
        raise ValueError("Invalid padding")
    if data[-padding_length:] != bytes([padding_length] * padding_length):
        raise ValueError("Invalid padding")
    return data[:-padding_length]

def encrypt_file(algorithm, mode, key_hex, input_file, output_file, iv_hex=None):
    """Encrypt file with optional key generation"""
    
    # ML3: Generate key if not provided
    if not key_hex:
        key_bytes = generate_random_bytes(16)  # 128-bit key for AES
        key_hex = bytes_to_hex(key_bytes)
        print(f"[INFO] Generated random key: {key_hex}")
    else:
        key_bytes = bytes.fromhex(key_hex)
    
    # Read input data
    plaintext = read_file(input_file)
    
    # Generate IV if needed and not provided
    if mode in ['cbc', 'cfb', 'ofb', 'ctr']:
        if iv_hex:
            iv = bytes.fromhex(iv_hex)
        else:
            iv = generate_random_bytes(16)
            iv_hex = bytes_to_hex(iv)
    else:
        iv = None
        iv_hex = None
    
    # Select encryption mode
    if mode == 'ecb':
        ciphertext = ecb_encrypt(plaintext, key_bytes)
    elif mode == 'cbc':
        ciphertext = cbc_encrypt(plaintext, key_bytes, iv)
    elif mode == 'cfb':
        ciphertext = cfb_encrypt(plaintext, key_bytes, iv)
    elif mode == 'ofb':
        ciphertext = ofb_encrypt(plaintext, key_bytes, iv)
    elif mode == 'ctr':
        ciphertext = ctr_encrypt(plaintext, key_bytes, iv)
    else:
        raise ValueError(f"Unsupported mode: {mode}")
    
    # Prepare output data
    if mode in ['cbc', 'cfb', 'ofb', 'ctr']:
        output_data = iv + ciphertext
    else:
        output_data = ciphertext
    
    # Write output file
    write_file(output_file, output_data)
    
    return key_hex, iv_hex

def decrypt_file(algorithm, mode, key_hex, input_file, output_file, iv_hex=None):
    """Decrypt file (key is always required)"""
    
    key_bytes = bytes.fromhex(key_hex)
    ciphertext = read_file(input_file)
    
    # Extract IV if needed
    if mode in ['cbc', 'cfb', 'ofb', 'ctr']:
        if iv_hex:
            iv = bytes.fromhex(iv_hex)
            actual_ciphertext = ciphertext
        else:
            # IV is prepended to ciphertext
            if len(ciphertext) < 16:
                raise ValueError("Ciphertext too short to contain IV")
            iv = ciphertext[:16]
            actual_ciphertext = ciphertext[16:]
    else:
        iv = None
        actual_ciphertext = ciphertext
    
    # Select decryption mode
    if mode == 'ecb':
        plaintext = ecb_decrypt(actual_ciphertext, key_bytes)
    elif mode == 'cbc':
        plaintext = cbc_decrypt(actual_ciphertext, key_bytes, iv)
    elif mode == 'cfb':
        plaintext = cfb_decrypt(actual_ciphertext, key_bytes, iv)
    elif mode == 'ofb':
        plaintext = ofb_decrypt(actual_ciphertext, key_bytes, iv)
    elif mode == 'ctr':
        plaintext = ctr_decrypt(actual_ciphertext, key_bytes, iv)
    else:
        raise ValueError(f"Unsupported mode: {mode}")
    
    # Write output file
    write_file(output_file, plaintext)

def main():
    """Main function for direct execution"""
    try:
        from cli import parse_arguments
        args = parse_arguments()
        
        if args.encrypt:
            result = encrypt_file(
                algorithm=args.algorithm,
                mode=args.mode,
                key_hex=args.key,
                input_file=args.input,
                output_file=args.output,
                iv_hex=args.iv
            )
            if isinstance(result, tuple):
                used_key, used_iv = result
                print(f"[SUCCESS] Encryption completed")
                if not args.key:
                    print(f"[IMPORTANT] Save this key for decryption: {used_key}")
                    
        elif args.decrypt:
            decrypt_file(
                algorithm=args.algorithm,
                mode=args.mode,
                key_hex=args.key,
                input_file=args.input,
                output_file=args.output,
                iv_hex=args.iv
            )
            print(f"[SUCCESS] Decryption completed")
            
    except Exception as e:
        print(f"[ERROR] {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())