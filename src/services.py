import json
import logging
from typing import List, Dict


def simple_search(query: str, transactions: List[Dict[str, str]]) -> str:
    """Функция для поиска транзакций по строке.

    :param query: Строка запроса для поиска.
    :param transactions: Список транзакций в формате словарей.
    :return: JSON-ответ с найденными транзакциями.
    """
    logging.info(f"Searching for transactions with query: {query}")
    query = query.lower()

    matched_transactions = [
        transaction for transaction in transactions
        if query in transaction['Описание'].lower() or query in transaction['Категория'].lower()
    ]

    return json.dumps(matched_transactions)
