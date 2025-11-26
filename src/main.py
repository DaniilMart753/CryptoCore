import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(__file__))

from cli import parse_arguments
from crypto import encrypt_file, decrypt_file

def main():
    try:
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