
## docs/ml3_requirements.md

```markdown
# Milestone 3 Requirements - CryptoCore

## Sprint Goal
Implement a secure source of randomness for keys and IVs.

## Technical Requirements

### Project Structure
- All previous requirements must still be met
- New dedicated CSPRNG module file
- Update README.md with new key generation behavior
- Documentation for NIST statistical test suite

### Command-Line Interface
- `--key` argument becomes optional for encryption operations
- If `--key` provided: use it as before
- If `--key` not provided during encryption:
  - Generate secure random 16-byte key
  - Print generated key to stdout as hexadecimal string
  - Proceed with encryption using generated key
- For decryption: `--key` remains mandatory
- Optional: warn about weak user-provided keys

### CSPRNG Implementation
- Dedicated CSPRNG module with `generate_random_bytes()` function
- Use cryptographically secure randomness source:
  - Python: `os.urandom()`
  - C: `/dev/urandom` or `RAND_bytes()`
- Do not use standard library random functions
- Integrate CSPRNG for:
  - Encryption key generation (when not provided)
  - All IV generation for encryption operations
- Handle potential errors gracefully

### Key and IV Management
- Generated keys must be 16 bytes for AES-128
- Print generated key to stdout exactly once
- Do not write generated key to output file
- IV generation uses new CSPRNG function
- IV handling from ML2 remains unchanged

### Testing & Verification
- Key generation test: encrypt without key, decrypt with printed key
- Uniqueness test: generate 1000 keys, verify all unique
- NIST Statistical Test Suite on CSPRNG output
- Basic distribution tests (Hamming weight)
- Maintain interoperability tests from ML2

## Example Usage

```bash
# Encryption with automatic key generation
cryptocore --algorithm aes --mode ctr --encrypt --input plaintext.txt --output ciphertext.bin
# Output: Generated random key: 1a2b3c4d5e6f7890fedcba9876543210

# Decryption (key must be provided)
cryptocore --algorithm aes --mode ctr --decrypt --key 1a2b3c4d5e6f7890fedcba9876543210 --input ciphertext.bin --output decrypted.txt