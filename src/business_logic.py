from datetime import datetime


def calculate_greeting():
    """Возвращает приветствие в зависимости от времени суток."""
    hour = datetime.now().hour

    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"

def analyze_expenses(data, date_time):
    """Анализирует данные о транзакциях и возвращает нужные параметры."""
    start_date = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S').replace(day=1)
    end_date = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')

    filtered_data = data[
        (data['Дата операции'] >= start_date) &
        (data['Дата операции'] <= end_date)
    ]

    result = {
        "cards": [],
        "top_transactions": []
    }

    # Группируем по картам
    card_group = filtered_data.groupby('Номер карты')
    for card, group in card_group:
        total_spent = group['Сумма операции'].sum()
        cashback = total_spent / 100.0
        last_digits = str(card)[-4:]
        result['cards'].append({
            'last_digits': last_digits,
            'total_spent': total_spent,
            'cashback': cashback
        })

    # Топ-5 транзакций
    top_transactions = filtered_data.nlargest(5, 'Сумма платежа')[['Дата операции', 'Сумма платежа', 'Категория', 'Описание']]
    result['top_transactions'] = top_transactions.to_dict(orient='records')

    return result