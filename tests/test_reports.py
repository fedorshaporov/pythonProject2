import pandas as pd
import pytest
from src.reports import spending_by_category  # Убедитесь, что путь импортирования правильный

@pytest.fixture
def sample_transactions():
    """Фикстура для создания образца данных транзакций."""
    # Пример данных о транзакциях
    data = {
        'Дата операции': [
            '2021-10-01', '2021-10-10', '2021-11-15',
            '2021-11-20', '2021-12-01', '2021-12-10'
        ],
        'Категория': [
            'Супермаркеты', 'Супермаркеты', 'Супермаркеты',
            'Еда', 'Супермаркеты', 'Еда'
        ],
        'Сумма операции': [1000, -9000, 1500, -300, -2500, 400]
    }
    return pd.DataFrame(data)

def test_spending_by_category(sample_transactions):
    """Тест для проверки функции spending_by_category."""
    result = spending_by_category(sample_transactions, category='Супермаркеты', date='2021-12-31')

    expected_data = {
        'Дата операции': ['2021-10', '2021-11', '2021-12'],  # Ожидаемая структура
        'Сумма операции': [-9000, 1500, -2500]  # Сумма для категорий за 3 месяца
    }
    expected_df = pd.DataFrame(expected_data)

    # Проверяем, что датафреймы равны
    pd.testing.assert_frame_equal(result, expected_df)

def test_spending_by_category_no_data(sample_transactions):
    """Тест для проверки отсутствующих данных."""
    result = spending_by_category(sample_transactions, category='Нет такой категории', date='2021-12-31')

    expected_df = pd.DataFrame(columns=['Дата операции', 'Сумма операции'])  # Пустой DataFrame
    expected_df = expected_df.astype({
        'Дата операции': 'period[M]',
        'Сумма операции': 'int64',
    })
    pd.testing.assert_frame_equal(result, expected_df)

def test_spending_by_category_with_default_date(sample_transactions):
    """Тест для проверки работы с датой по умолчанию."""
    result = spending_by_category(sample_transactions, category='Супермаркеты')

    expected_data = {
        'Дата операции': [],
        'Сумма операции': []
    }
    expected_df = pd.DataFrame(expected_data)
    expected_df = expected_df.astype({
        'Дата операции': 'period[M]',
        'Сумма операции': 'int64',
    })
    pd.testing.assert_frame_equal(result, expected_df)

def test_spending_by_category_empty(sample_transactions):
    """Тест для проверки обработки пустого DataFrame."""
    empty_df = pd.DataFrame(columns=['Дата операции', 'Категория', 'Сумма операции'])
    result = spending_by_category(empty_df, category='Супермаркеты', date='2021-12-31')

    expected_df = pd.DataFrame(columns=['Дата операции', 'Сумма операции'])
    expected_df = expected_df.astype({
        'Дата операции': 'period[M]',
        'Сумма операции': 'object',
    })
    pd.testing.assert_frame_equal(result, expected_df)

if __name__ == "__main__":
    pytest.main()