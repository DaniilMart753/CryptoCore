#!/usr/bin/env python3
"""
CryptoCore - Главный файл программы
Связывает все модули вместе для шифрования/дешифрования
"""

import sys
import os
from cli import get_arguments
from file_utils import read_file_binary, write_encrypted_file, read_encrypted_file, write_decrypted_file, generate_output_filename
from crypto import hex_to_bytes
from modes import encrypt_with_mode, decrypt_with_mode

def main():
    """
    Главная функция программы
    """
    try:
        # 1. Получаем аргументы командной строки
        print("Парсинг аргументов...")
        args = get_arguments()
        
        # 2. Определяем операцию
        operation = 'encrypt' if args.encrypt else 'decrypt'
        print(f"Операция: {operation}")
        print(f"Режим: {args.mode}")
        
        # 3. Генерируем имя выходного файла если не указано
        output_file = generate_output_filename(args.input, operation, args.output)
        print(f"Входной файл: {args.input}")
        print(f"Выходной файл: {output_file}")
        
        # 4. Конвертируем ключ из HEX в байты
        print("Обработка ключа...")
        key_bytes = hex_to_bytes(args.key)
        print(f"Ключ: {args.key} -> {key_bytes.hex()}")
        
        # 5. Выполняем операцию (шифрование/дешифрование)
        if operation == 'encrypt':
            # Читаем исходный файл
            print("Чтение файла для шифрования...")
            plaintext = read_file_binary(args.input)
            print(f"Прочитано {len(plaintext)} байт")
            
            # Шифруем
            print(f"Шифрование в режиме {args.mode}...")
            iv, encrypted_data = encrypt_with_mode(plaintext, key_bytes, args.mode)
            print(f"Сгенерирован IV: {iv.hex()}")
            
            # Записываем зашифрованные данные с IV
            print("Запись зашифрованного файла...")
            write_encrypted_file(output_file, iv, encrypted_data)
            print(f"Записано {len(encrypted_data) + 16} байт (данные + IV)")
            
            print(f"УСПЕХ! Шифрование завершено!")
            print(f"Результат сохранен в: {output_file}")
            print(f"IV (hex): {iv.hex()}")
            
        else:  # decrypt
            # Читаем зашифрованный файл и извлекаем IV
            print("Чтение зашифрованного файла...")
            iv, encrypted_data = read_encrypted_file(args.input)
            print(f"Прочитано {len(encrypted_data)} байт данных")
            print(f"Извлечен IV: {iv.hex()}")
            
            # Дешифруем
            print(f"Дешифрование в режиме {args.mode}...")
            decrypted_data = decrypt_with_mode(encrypted_data, key_bytes, args.mode, iv)
            
            # Записываем расшифрованные данные
            print("Запись расшифрованного файла...")
            write_decrypted_file(output_file, decrypted_data)
            print(f"Записано {len(decrypted_data)} байт")
            
            print(f"УСПЕХ! Дешифрование завершено!")
            print(f"Результат сохранен в: {output_file}")
            
    except FileNotFoundError as e:
        print(f"ОШИБКА: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"ОШИБКА: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"НЕИЗВЕСТНАЯ ОШИБКА: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()