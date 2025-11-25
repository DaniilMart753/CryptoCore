#!/usr/bin/env python3
"""
CryptoCore - Главный файл программы
Связывает все модули вместе для шифрования/дешифрования
"""

import sys
import os
from cli import get_arguments
from file_utils import read_file_binary, write_file_binary, generate_output_filename
from crypto import aes_ecb_encrypt, aes_ecb_decrypt, hex_to_bytes

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
        
        # 3. Генерируем имя выходного файла если не указано
        output_file = generate_output_filename(args.input, operation, args.output)
        print(f"Входной файл: {args.input}")
        print(f"Выходной файл: {output_file}")
        
        # 4. Читаем входной файл
        print("Чтение файла...")
        input_data = read_file_binary(args.input)
        print(f"Прочитано {len(input_data)} байт")
        
        # 5. Конвертируем ключ из HEX в байты
        print("Обработка ключа...")
        key_bytes = hex_to_bytes(args.key)
        print(f"Ключ: {args.key} -> {key_bytes.hex()}")
        
        # 6. Выполняем операцию (шифрование/дешифрование)
        print(f"Выполнение {operation}...")
        if operation == 'encrypt':
            result_data = aes_ecb_encrypt(input_data, key_bytes)
            print("Шифрование завершено")
        else:
            result_data = aes_ecb_decrypt(input_data, key_bytes)
            print("Дешифрование завершено")
        
        # 7. Записываем результат
        print("Запись результата...")
        write_file_binary(output_file, result_data)
        print(f"Записано {len(result_data)} байт")
        
        # 8. Успех!
        print(f"УСПЕХ! {operation.upper()} завершено!")
        print(f"Результат сохранен в: {output_file}")
        
        if operation == 'encrypt':
            print(f"Размер исходного файла: {len(input_data)} байт")
            print(f"Размер зашифрованного файла: {len(result_data)} байт")
        else:
            print(f"Файл успешно расшифрован!")
            
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