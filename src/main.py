
import os
from src.views import generate_json_response

def main():
    # Пример входящей даты
    date_time = "2020-05-20 12:00:00"

    # Определяем путь к файлу user_settings.json
    settings_path = os.path.join(os.path.dirname(__file__), '../user_settings.json')

    # Проверяем, существует ли файл настроек
    if not os.path.exists(settings_path):
        print(f"Файл настроек не найден: {settings_path}")
        return  # Завершаем выполнение, если файл не найден

    # Генерация JSON-ответа, передавая путь к файлу настроек
    json_response = generate_json_response(date_time, settings_path)

    # Выводим ответ
    print(json_response)

if __name__ == '__main__':
    main()
