import argparse
import sys
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description='CryptoCore - Cryptographic Tool')
    
    # Crypto operations
    parser.add_argument('--algorithm', required=True, choices=['aes'], help='Cryptographic algorithm')
    parser.add_argument('--mode', required=True, choices=['ecb', 'cbc', 'cfb', 'ofb', 'ctr'], help='Mode of operation')
    parser.add_argument('--encrypt', action='store_true', help='Encrypt mode')
    parser.add_argument('--decrypt', action='store_true', help='Decrypt mode')
    parser.add_argument('--key', help='Encryption key as hexadecimal string (optional for encryption)')
    parser.add_argument('--input', required=True, help='Input file path')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--iv', help='Initialization vector as hexadecimal string')
    
    args = parser.parse_args()
    
    # Validate operation mode
    if not (args.encrypt or args.decrypt) or (args.encrypt and args.decrypt):
        parser.error("Exactly one of --encrypt or --decrypt must be specified")
    
    # Validate input file exists
    if not os.path.exists(args.input):
        parser.error(f"Input file does not exist: {args.input}")
    
    # ML3: Key validation - optional for encryption, required for decryption
    if args.decrypt and not args.key:
        parser.error("--key is mandatory for decryption")
    
    if args.encrypt and not args.key:
        print("[INFO] No key provided. Generating secure random key...")
    
    # Set default output file if not provided
    if not args.output:
        if args.encrypt:
            args.output = args.input + '.enc'
        else:
            args.output = args.input + '.dec'
        print(f"[INFO] Using default output file: {args.output}")
    
    return args

def main():
    try:
        args = parse_arguments()
        
        # Import here to avoid circular imports
        from crypto import encrypt_file, decrypt_file
        
        if args.encrypt:
            result = encrypt_file(
                algorithm=args.algorithm,
                mode=args.mode,
                key_hex=args.key,
                input_file=args.input,
                output_file=args.output,
                iv_hex=args.iv
            )
            if isinstance(result, tuple) and len(result) == 2:
                used_key, used_iv = result
                print(f"[SUCCESS] Encryption completed")
                if not args.key:
                    print(f"[IMPORTANT] Generated key: {used_key}")
            else:
                print(f"[SUCCESS] Encryption completed")
                
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
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()