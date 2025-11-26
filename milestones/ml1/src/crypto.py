from Crypto.Cipher import AES
import os

def pkcs7_pad(data, block_size=16):
    """
    Добавляет PKCS7 padding к данным
    
    Args:
        data (bytes): Данные для паддинга
        block_size (int): Размер блока (по умолчанию 16 для AES)
        
    Returns:
        bytes: Данные с паддингом
    """
    padding_length = block_size - (len(data) % block_size)
    padding = bytes([padding_length]) * padding_length
    return data + padding

def pkcs7_unpad(data, block_size=16):
    """
    Убирает PKCS7 padding с данных
    
    Args:
        data (bytes): Данные с паддингом
        block_size (int): Размер блока
        
    Returns:
        bytes: Данные без паддинга
        
    Raises:
        ValueError: Если паддинг некорректен
    """
    if len(data) % block_size != 0:
        raise ValueError("Данные не выровнены по размеру блока")
    
    padding_length = data[-1]
    
    # Проверяем корректность паддинга
    if padding_length < 1 or padding_length > block_size:
        raise ValueError("Некорректная длина паддинга")
    
    if data[-padding_length:] != bytes([padding_length]) * padding_length:
        raise ValueError("Некорректный паддинг")
    
    return data[:-padding_length]

def aes_ecb_encrypt(plaintext, key):
    """
    Шифрует данные в режиме ECB
    
    Args:
        plaintext (bytes): Открытый текст
        key (bytes): Ключ шифрования (16 байт)
        
    Returns:
        bytes: Зашифрованный текст
    """
    # Добавляем паддинг
    padded_data = pkcs7_pad(plaintext)
    
    # Создаем объект шифрования
    cipher = AES.new(key, AES.MODE_ECB)
    
    # Шифруем
    ciphertext = cipher.encrypt(padded_data)
    
    return ciphertext

def aes_ecb_decrypt(ciphertext, key):
    """
    Дешифрует данные в режиме ECB
    
    Args:
        ciphertext (bytes): Зашифрованный текст  
        key (bytes): Ключ шифрования (16 байт)
        
    Returns:
        bytes: Расшифрованный текст
    """
    # Создаем объект дешифрования
    cipher = AES.new(key, AES.MODE_ECB)
    
    # Дешифруем
    padded_plaintext = cipher.decrypt(ciphertext)
    
    # Убираем паддинг
    plaintext = pkcs7_unpad(padded_plaintext)
    
    return plaintext

def hex_to_bytes(hex_string):
    """
    Конвертирует HEX строку в байты
    
    Args:
        hex_string (str): HEX строка (может быть с префиксом -- или без)
        
    Returns:
        bytes: Байтовое представление
    """
    # Убираем префикс если есть
    if hex_string.startswith('--'):
        hex_string = hex_string[2:]
    
    return bytes.fromhex(hex_string)

# Тестирование криптографических функций
if __name__ == "__main__":
    # Тестовые данные
    test_key = b'0123456789abcdef'  # 16 байт
    test_plaintext = b"Hello, AES ECB mode! This is a test."
    
    print("Тестирование криптографических функций...")
    
    try:
        # Шифрование
        ciphertext = aes_ecb_encrypt(test_plaintext, test_key)
        print("Шифрование выполнено")
        
        # Дешифрование  
        decrypted = aes_ecb_decrypt(ciphertext, test_key)
        print("Дешифрование выполнено")
        
        # Проверка
        if test_plaintext == decrypted:
            print("Все работает! Исходный и расшифрованный текст совпадают")
        else:
            print("Ошибка: тексты не совпадают")
            
    except Exception as e:
        print(f"Ошибка: {e}")