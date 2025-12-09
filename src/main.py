from src.views import generate_json_response


def main():
    # Пример входящей даты
    date_time = "2020-05-20 12:00:00"

    # Генерируем JSON-ответ
    json_response = generate_json_response(date_time)

    print(json_response)

if __name__ == '__main__':
    main()
