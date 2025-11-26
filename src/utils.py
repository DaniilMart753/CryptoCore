# utils.py
def pkcs7_pad(data, block_size=16):
    """Pad data using PKCS#7 standard"""
    padding_length = block_size - (len(data) % block_size)
    padding = bytes([padding_length] * padding_length)
    return data + padding

def pkcs7_unpad(data):
    """Remove PKCS#7 padding"""
    padding_length = data[-1]
    # Validate padding
    if padding_length == 0 or padding_length > len(data):
        raise ValueError("Invalid padding")
    if data[-padding_length:] != bytes([padding_length] * padding_length):
        raise ValueError("Invalid padding")
    return data[:-padding_length]