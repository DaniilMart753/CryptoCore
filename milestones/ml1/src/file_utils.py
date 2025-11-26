import os

def read_file_binary(file_path):
    """
    Читает файл в бинарном режиме
    
    Args:
        file_path (str): Путь к файлу
        
    Returns:
        bytes: Содержимое файла в виде байтов
        
    Raises:
        FileNotFoundError: Если файл не существует
        IOError: Если ошибка чтения файла
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")
    
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except IOError as e:
        raise IOError(f"Ошибка чтения файла {file_path}: {e}")

def write_file_binary(file_path, data):
    """
    Записывает данные в файл в бинарном режиме
    
    Args:
        file_path (str): Путь к файлу
        data (bytes): Данные для записи
        
    Raises:
        IOError: Если ошибка записи файла
    """
    try:
        # Создаем папки если их нет (только если путь содержит папки)
        directory = os.path.dirname(file_path)
        if directory:  # Если есть папки в пути
            os.makedirs(directory, exist_ok=True)
        
        with open(file_path, 'wb') as file:
            file.write(data)
    except IOError as e:
        raise IOError(f"Ошибка записи файла {file_path}: {e}")

def generate_output_filename(input_file, operation, output_file=None):
    """
    Генерирует имя выходного файла если не указано
    
    Args:
        input_file (str): Входной файл
        operation (str): 'encrypt' или 'decrypt'
        output_file (str): Явно указанный выходной файл (если есть)
        
    Returns:
        str: Имя выходного файла
    """
    if output_file:
        return output_file
    
    # Генерируем имя на основе операции
    base_name = os.path.splitext(input_file)[0]
    
    if operation == 'encrypt':
        return f"{base_name}.encrypted"
    else:  # decrypt
        if input_file.endswith('.encrypted'):
            return f"{base_name}.decrypted"
        else:
            return f"{base_name}.decrypted"

# Тестирование файловых операций
if __name__ == "__main__":
    # Тест создания тестового файла
    test_data = b"Hello, this is test data for file operations!"
    
    try:
        # Используем простое имя файла без путей
        test_filename = "test_file.bin"
        
        write_file_binary(test_filename, test_data)
        print("Тестовый файл создан")
        
        read_data = read_file_binary(test_filename)
        print("Файл прочитан")
        
        if test_data == read_data:
            print("Данные совпадают - файловые операции работают!")
        else:
            print("Ошибка: данные не совпадают")
            
        # Убираем тестовый файл
        if os.path.exists(test_filename):
            os.remove(test_filename)
            print("Тестовый файл удален")
        
    except Exception as e:
        print(f"Ошибка при тесте файловых операций: {e}")