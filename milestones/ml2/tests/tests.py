import os
import sys
import subprocess

# Добавляем родительскую папку в путь для импорта
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from file_utils import read_file_binary, write_file_binary
from crypto import aes_ecb_encrypt, aes_ecb_decrypt, hex_to_bytes

def test_encryption_decryption_roundtrip():
    """Тест: шифрование -> дешифрование = исходный текст"""
    print("Тест 1: Проверка шифрования и дешифрования")
    
    # Тестовые данные
    test_key = b'0123456789abcdef'
    test_data = b"Test data for encryption and decryption"
    
    # Шифруем
    encrypted = aes_ecb_encrypt(test_data, test_key)
    
    # Дешифруем
    decrypted = aes_ecb_decrypt(encrypted, test_key)
    
    # Проверяем
    assert test_data == decrypted, "Исходные и дешифрованные данные не совпадают"
    print("Тест пройден: шифрование -> дешифрование работает корректно")

def test_file_operations():
    """Тест работы с файлами"""
    print("Тест 2: Проверка файловых операций")
    
    test_data = b"File operations test data"
    test_filename = "test_file_ops.bin"
    
    # Записываем файл
    write_file_binary(test_filename, test_data)
    
    # Читаем файл
    read_data = read_file_binary(test_filename)
    
    # Проверяем
    assert test_data == read_data, "Записанные и прочитанные данные не совпадают"
    
    # Убираем тестовый файл
    if os.path.exists(test_filename):
        os.remove(test_filename)
    
    print("Тест пройден: файловые операции работают корректно")

def test_cli_encryption():
    """Тест CLI команды шифрования"""
    print("Тест 3: Проверка CLI команды")
    
    # Создаем тестовый файл
    test_input = "cli_test_input.txt"
    test_encrypted = "cli_test_encrypted.bin"
    test_decrypted = "cli_test_decrypted.txt"
    
    with open(test_input, 'w') as f:
        f.write("CLI command test data")
    
    try:
        # Команда шифрования
        encrypt_cmd = [
            'python', 'main.py',
            '--algorithm', 'aes',
            '--mode', 'ecb',
            '--encrypt',
            '--key', '00112233445566778899aabbccddeeff',
            '--input', test_input,
            '--output', test_encrypted
        ]
        
        # Команда дешифрования
        decrypt_cmd = [
            'python', 'main.py',
            '--algorithm', 'aes',
            '--mode', 'ecb',
            '--decrypt',
            '--key', '00112233445566778899aabbccddeeff',
            '--input', test_encrypted,
            '--output', test_decrypted
        ]
        
        # Запускаем команды
        subprocess.run(encrypt_cmd, check=True, capture_output=True)
        subprocess.run(decrypt_cmd, check=True, capture_output=True)
        
        # Проверяем что файлы создались
        assert os.path.exists(test_encrypted), "Зашифрованный файл не создан"
        assert os.path.exists(test_decrypted), "Расшифрованный файл не создан"
        
        print("Тест пройден: CLI команды работают корректно")
        
    except subprocess.CalledProcessError as e:
        raise AssertionError(f"CLI команда завершилась с ошибкой: {e}")
    
    finally:
        # Убираем тестовые файлы
        for file in [test_input, test_encrypted, test_decrypted]:
            if os.path.exists(file):
                os.remove(file)

def run_all_tests():
    """Запуск всех тестов"""
    print("Запуск тестов CryptoCore...")
    print("=" * 50)
    
    try:
        test_file_operations()
        test_encryption_decryption_roundtrip()
        test_cli_encryption()
        
        print("=" * 50)
        print("Все тесты пройдены успешно!")
        
    except Exception as e:
        print("=" * 50)
        print(f"Тест не пройден: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_all_tests()