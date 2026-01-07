import pytest
import json
from src.services import simple_search

@pytest.fixture
def sample_transactions():
    """Возвращает список тестовых транзакций."""
    return [
        {
            "Описание": "Покупка в магазине",
            "Категория": "Еда",
            "Сумма операции": 100.0
        },
        {
            "Описание": "Оплата коммунальных услуг",
            "Категория": "Коммунальные платежи",
            "Сумма операции": 200.0
        },
        {
            "Описание": "Перевод Валерий А.",
            "Категория": "Переводы",
            "Сумма операции": 300.0
        },
    ]


def test_simple_search_by_description(sample_transactions):
    """Тест для функции simple_search по описанию."""
    query = "Покупка"
    result = simple_search(query, sample_transactions)
    expected = [
        {
            "Описание": "Покупка в магазине",
            "Категория": "Еда",
            "Сумма операции": 100.0
        },
    ]
    assert json.loads(result) == expected


def test_simple_search_by_category(sample_transactions):
    """Тест для функции simple_search по категории."""
    query = "переводы"
    result = simple_search(query, sample_transactions)
    expected = [
        {
            "Описание": "Перевод Валерий А.",
            "Категория": "Переводы",
            "Сумма операции": 300.0
        },
    ]
    assert json.loads(result) == expected


def test_simple_search_no_results(sample_transactions):
    """Тест для функции simple_search с отсутствующими результатами."""
    query = "Неттранзакции"
    result = simple_search(query, sample_transactions)
    expected = []
    assert json.loads(result) == expected
