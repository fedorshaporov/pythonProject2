import pandas as pd

def load_operations(file_path):
    """Загружает данные о транзакциях из Excel."""
    data = pd.read_excel(file_path)
    data.columns = data.columns.str.strip()  # Убираем пробелы в названиях столбцов
    return data
