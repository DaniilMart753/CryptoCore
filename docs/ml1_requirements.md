# Milestone 1 Requirements - CryptoCore

## Sprint Goal
Establish the codebase and implement core block cipher operations in ECB mode.

## Technical Requirements

### Project Structure & Repository Hygiene
- Project must be hosted in a Git repository
- README.md file with project description, build instructions, usage examples, and dependencies
- Build system or setup script (setup.py for Python, Makefile for C)
- Logical source code organization

### Command-Line Interface (CLI)
- Tool must be invokable as `cryptocore`
- Required arguments:
  - `--algorithm aes` (only AES supported)
  - `--mode ecb` (only ECB mode)
  - `--encrypt` or `--decrypt` (exactly one)
  - `--key KEY` (16-byte hexadecimal string)
  - `--input INPUT_FILE`
  - `--output OUTPUT_FILE`
- Key must be provided as hexadecimal string
- CLI must validate all arguments

### Core Cryptographic Implementation
- AES-128 implementation using library primitives (pycryptodome for Python, OpenSSL for C)
- ECB mode logic implemented from scratch
- PKCS#7 padding standard
- Handle both text and binary files correctly

### File I/O
- Read entire input file contents
- Write resulting data to output file
- Handle file errors gracefully

### Testing & Verification
- Encrypting and decrypting must produce identical file
- Provide test script in README.md
- Verify against OpenSSL implementation

## Example Usage

```bash
# Encryption
cryptocore --algorithm aes --mode ecb --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output ciphertext.bin

# Decryption
cryptocore --algorithm aes --mode ecb --decrypt --key 000102030405060708090a0b0c0d0e0f --input ciphertext.bin --output decrypted.txt