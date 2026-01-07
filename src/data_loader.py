import pandas as pd


def load_operations(file_path):
    """Загружает данные о транзакциях из Excel файла.

    Args:
        file_path (str): Путь к Excel файлу с данными о транзакциях.

    Returns:
        DataFrame: Возвращает DataFrame с загруженными данными о транзакциях.
    """
    data = pd.read_excel(file_path)
    data.columns = data.columns.str.strip()  # Убираем пробелы в названиях столбцов
    return data
