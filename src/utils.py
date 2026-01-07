import pandas as pd
import os


def load_operations(file_path):
    """Загружает данные о транзакциях из Excel."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    data = pd.read_excel(file_path)
    data.columns = data.columns.str.strip()  # Убираем пробелы в названиях столбцов

    # Преобразование 'Дата операции' в тип datetime
    data['Дата операции'] = pd.to_datetime(data['Дата операции'], format='%d.%m.%Y %H:%M:%S', errors='coerce')

    # Проверяем типы данных
    print(data.dtypes)  # Это поможет увидеть, какие типы данных есть в DataFrame

    return data