# CryptoCore - Cryptographic Toolkit

A command-line cryptographic tool implementing various encryption algorithms and modes.

## Milestones

- [Milestone 1](milestones/ml1/) - Basic AES-128 ECB mode
- [Milestone 2](milestones/ml2/) - Confidential modes (CBC, CFB, OFB, CTR) 
- [Milestone 3](milestones/ml3/) - Cryptographically Secure Random Number Generation

## Quick Start

```bash
# Using current development version
cd src
python main.py --algorithm aes --mode cbc --encrypt --input file.txt --output encrypted.bin

# Or use specific milestone
cd milestones/ml3
python src/main.py --algorithm aes --mode cbc --encrypt --input file.txt --output encrypted.bin