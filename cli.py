import argparse

def parse_arguments():
    """
    Разбирает аргументы командной строки
    """
    parser = argparse.ArgumentParser(
        description='CryptoCore - Простая криптографическая утилита',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Примеры использования:
  Шифрование (ECB):
    python main.py --algorithm aes --mode ecb --encrypt --key 00112233445566778899aabbccddeeff --input text.txt --output encrypted.bin
  
  Шифрование (CBC):
    python main.py --algorithm aes --mode cbc --encrypt --key 00112233445566778899aabbccddeeff --input text.txt --output encrypted.bin

  Дешифрование:
    python main.py --algorithm aes --mode ecb --decrypt --key 00112233445566778899aabbccddeeff --input encrypted.bin --output decrypted.txt
        '''
    )
    
    # Обязательные аргументы
    parser.add_argument('--algorithm', required=True, choices=['aes'], 
                       help='Алгоритм шифрования (пока только aes)')
    
    parser.add_argument('--mode', required=True, choices=['ecb', 'cbc', 'cfb', 'ofb', 'ctr'], 
                       help='Режим работы')
    
    # Режим работы (шифрование или дешифрование)
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('--encrypt', action='store_true', 
                           help='Режим шифрования')
    mode_group.add_argument('--decrypt', action='store_true', 
                           help='Режим дешифрования')
    
    # Ключ и файлы
    parser.add_argument('--key', required=True, 
                       help='Ключ в HEX формате (16 байт для AES-128)')
    
    parser.add_argument('--input', required=True, 
                       help='Путь к входному файлу')
    
    parser.add_argument('--output', 
                       help='Путь к выходному файлу (если не указан, будет сгенерирован автоматически)')
    
    return parser.parse_args()

def validate_args(args):
    """
    Проверяет корректность аргументов
    """
    # Проверяем что указан ровно один режим
    if args.encrypt == args.decrypt:
        raise ValueError("Должен быть указан ровно один из флагов --encrypt или --decrypt")
    
    # Проверяем ключ
    if not args.key.startswith('--'):
        # Убираем префикс если есть
        key_clean = args.key[2:] if args.key.startswith('--') else args.key
        
        if len(key_clean) != 32:  # 32 hex символа = 16 байт
            raise ValueError(f"Ключ должен быть 16 байт (32 hex символа). Получено: {len(key_clean)} символов")
        
        try:
            bytes.fromhex(key_clean)
        except ValueError:
            raise ValueError("Ключ должен быть в корректном HEX формате")
    
    return args

def get_arguments():
    """
    Основная функция для получения и проверки аргументов
    """
    args = parse_arguments()
    return validate_args(args)

# Временная проверка
if __name__ == "__main__":
    try:
        args = get_arguments()
        print("Аргументы корректны:")
        print(f"  Алгоритм: {args.algorithm}")
        print(f"  Режим: {args.mode}")
        print(f"  Действие: {'Шифрование' if args.encrypt else 'Дешифрование'}")
        print(f"  Ключ: {args.key}")
        print(f"  Входной файл: {args.input}")
        print(f"  Выходной файл: {args.output}")
    except Exception as e:
        print(f"Ошибка: {e}")