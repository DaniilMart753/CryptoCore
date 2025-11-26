from Crypto.Cipher import AES
from Crypto.Util import Counter
import os
from crypto import pkcs7_pad, pkcs7_unpad

class EncryptionModes:
    """
    Класс для реализации различных режимов шифрования
    """
    
    @staticmethod
    def ecb_encrypt(plaintext, key):
        """Режим ECB - шифрование"""
        padded_data = pkcs7_pad(plaintext)
        cipher = AES.new(key, AES.MODE_ECB)
        return cipher.encrypt(padded_data)
    
    @staticmethod
    def ecb_decrypt(ciphertext, key):
        """Режим ECB - дешифрование"""
        cipher = AES.new(key, AES.MODE_ECB)
        padded_plaintext = cipher.decrypt(ciphertext)
        return pkcs7_unpad(padded_plaintext)
    
    @staticmethod
    def cbc_encrypt(plaintext, key, iv):
        """Режим CBC - шифрование"""
        padded_data = pkcs7_pad(plaintext)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return cipher.encrypt(padded_data)
    
    @staticmethod
    def cbc_decrypt(ciphertext, key, iv):
        """Режим CBC - дешифрование"""
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_plaintext = cipher.decrypt(ciphertext)
        return pkcs7_unpad(padded_plaintext)
    
    @staticmethod
    def cfb_encrypt(plaintext, key, iv):
        """Режим CFB - шифрование"""
        cipher = AES.new(key, AES.MODE_CFB, iv, segment_size=128)
        return cipher.encrypt(plaintext)
    
    @staticmethod
    def cfb_decrypt(ciphertext, key, iv):
        """Режим CFB - дешифрование"""
        cipher = AES.new(key, AES.MODE_CFB, iv, segment_size=128)
        return cipher.decrypt(ciphertext)
    
    @staticmethod
    def ofb_encrypt(plaintext, key, iv):
        """Режим OFB - шифрование"""
        cipher = AES.new(key, AES.MODE_OFB, iv)
        return cipher.encrypt(plaintext)
    
    @staticmethod
    def ofb_decrypt(ciphertext, key, iv):
        """Режим OFB - дешифрование"""
        cipher = AES.new(key, AES.MODE_OFB, iv)
        return cipher.decrypt(ciphertext)
    
    @staticmethod
    def ctr_encrypt(plaintext, key, iv):
        """Режим CTR - шифрование"""
        ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))
        cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
        return cipher.encrypt(plaintext)
    
    @staticmethod
    def ctr_decrypt(ciphertext, key, iv):
        """Режим CTR - дешифрование"""
        ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))
        cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
        return cipher.decrypt(ciphertext)

def generate_iv():
    """
    Генерирует случайный вектор инициализации (16 байт)
    """
    return os.urandom(16)

def encrypt_with_mode(plaintext, key, mode, iv=None):
    """
    Универсальная функция шифрования для всех режимов
    """
    if iv is None:
        iv = generate_iv()
    
    modes_class = EncryptionModes()
    
    if mode == 'ecb':
        return iv, modes_class.ecb_encrypt(plaintext, key)
    elif mode == 'cbc':
        return iv, modes_class.cbc_encrypt(plaintext, key, iv)
    elif mode == 'cfb':
        return iv, modes_class.cfb_encrypt(plaintext, key, iv)
    elif mode == 'ofb':
        return iv, modes_class.ofb_encrypt(plaintext, key, iv)
    elif mode == 'ctr':
        return iv, modes_class.ctr_encrypt(plaintext, key, iv)
    else:
        raise ValueError(f"Неизвестный режим: {mode}")

def decrypt_with_mode(ciphertext, key, mode, iv):
    """
    Универсальная функция дешифрования для всех режимов
    """
    modes_class = EncryptionModes()
    
    if mode == 'ecb':
        return modes_class.ecb_decrypt(ciphertext, key)
    elif mode == 'cbc':
        return modes_class.cbc_decrypt(ciphertext, key, iv)
    elif mode == 'cfb':
        return modes_class.cfb_decrypt(ciphertext, key, iv)
    elif mode == 'ofb':
        return modes_class.ofb_decrypt(ciphertext, key, iv)
    elif mode == 'ctr':
        return modes_class.ctr_decrypt(ciphertext, key, iv)
    else:
        raise ValueError(f"Неизвестный режим: {mode}")

# Тестирование режимов
if __name__ == "__main__":
    test_key = b'0123456789abcdef'
    test_plaintext = b"Testing different encryption modes"
    
    print("Тестирование режимов шифрования...")
    
    for mode in ['ecb', 'cbc', 'cfb', 'ofb', 'ctr']:
        try:
            iv, encrypted = encrypt_with_mode(test_plaintext, test_key, mode)
            decrypted = decrypt_with_mode(encrypted, test_key, mode, iv)
            
            if test_plaintext == decrypted:
                print(f"{mode.upper()} режим работает")
            else:
                print(f"{mode.upper()} режим не работает")
                
        except Exception as e:
            print(f"{mode.upper()} ошибка: {e}")