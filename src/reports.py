import pandas as pd
import json
import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Optional

# Установка конфигурации для логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def report_decorator(filename: Optional[str] = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            if filename is None:
                filename_1 = f'report_{func.__name__}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            else:
                filename_1 = filename
                # Приведение Period к строке для сериализации в JSON
            if not result.empty:
                result['Дата операции'] = result['Дата операции'].astype(str)

            with open(filename_1, 'w') as f:
                json.dump(result.to_dict(orient='records'), f, indent=4)
                logging.info(f'Report saved to {filename}')

            return result
        return wrapper
    return decorator


@report_decorator()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    date = datetime.strptime(date, '%Y-%m-%d') if isinstance(date, str) else date
    three_months_ago = date - timedelta(days=90)

    filtered_transactions = transactions[
        (transactions['Категория'] == category) &
        (pd.to_datetime(transactions['Дата операции']) >= three_months_ago) &
        (pd.to_datetime(transactions['Дата операции']) <= date)
    ]

    total_spending = filtered_transactions.groupby(pd.to_datetime(filtered_transactions["Дата операции"]).dt.to_period("M"))["Сумма операции"].sum().reset_index()

    return total_spending


# Пример использования
if __name__ == '__main__':
    transactions_df = pd.read_excel("../data/operations.xlsx")

    # Вызов функции с отчетом
    print(spending_by_category(transactions_df, category='Супермаркеты', date="2021-12-31"))
