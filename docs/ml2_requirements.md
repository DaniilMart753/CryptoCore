
## docs/ml2_requirements.md

```markdown
# Milestone 2 Requirements - CryptoCore

## Sprint Goal
Implement the core confidential modes of operation (CBC, CFB, OFB, CTR).

## Technical Requirements

### Project Structure
- All ML1 requirements must still be met
- Update README.md with new CLI options and interoperability tests
- New source code for modes integrated into logical structure

### Command-Line Interface
- `--mode` argument extended to accept: `cbc`, `cfb`, `ofb`, `ctr`
- Correct IV handling:
  - Encryption: generate secure random IV, `--iv` not accepted
  - Decryption: `--iv` must be accepted as hexadecimal string

### Core Cryptographic Implementation
- CBC, CFB, OFB, CTR modes implemented from scratch
- Mode-specific requirements:
  - CBC: chaining mechanism, requires PKCS#7 padding
  - CFB: stream cipher, full block size (128-bit), no padding
  - OFB: stream cipher, independent keystream, no padding
  - CTR: stream cipher, counter from IV, no padding
- Padding logic updated for stream modes

### Initialization Vector Handling
- Encryption: generate using CSPRNG (os.urandom for Python)
- Generated IV prepended to ciphertext output file
- Decryption: read IV from file or provided via `--iv`
- IV always 16 bytes for all modes

### File I/O
- Write 16-byte IV before ciphertext during encryption
- Read first 16 bytes as IV during decryption (if not provided)
- Handle short files with clear errors

### Testing & Verification
- Round-trip tests for all new modes
- Interoperability with OpenSSL CLI
- Test scripts for each mode

## Example Usage

```bash
# Encryption (IV generated automatically)
cryptocore --algorithm aes --mode cbc --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output ciphertext.bin

# Decryption (IV provided)
cryptocore --algorithm aes --mode cbc --decrypt --key 000102030405060708090a0b0c0d0e0f --iv aabbccddeeff00112233445566778899 --input ciphertext.bin --output decrypted.txt