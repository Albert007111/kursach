import requests
import json
from pprint import pprint
import time

# Базовый URL API
BASE_URL = "http://localhost:8000"

def test_system():
    print("Тестирование системы рекомендаций для грузоперевозок\n")
    
    # Тестовые данные
    test_cargo = {
        "weight": 2000,  # 2 тонны
        "distance": 300,  # 300 км
        "delivery_time": 6,  # 6 часов
        "cost": 3000  # 3000 рублей
    }
    
    try:
        # 1. Проверка статуса модели
        print("1. Проверка статуса модели...")
        response = requests.get(f"{BASE_URL}/model/info")
        print(f"Статус: {response.status_code}")
        print(f"Информация о модели: {response.json()}\n")
        
        # 2. Обучение модели
        print("2. Обучение модели...")
        response = requests.post(f"{BASE_URL}/train")
        print(f"Статус: {response.status_code}")
        print(f"Ответ: {response.json()}\n")
        
        # 3. Получение рекомендаций по маршрутам
        print("3. Рекомендации по маршрутам:")
        response = requests.post(f"{BASE_URL}/recommend/route", json=test_cargo)
        print(f"Статус: {response.status_code}")
        print("Рекомендации:")
        pprint(response.json()["recommendations"])
        print()
        
        # 4. Рекомендации по выбору транспорта
        print("4. Рекомендации по выбору транспорта:")
        response = requests.post(f"{BASE_URL}/recommend/vehicle", json=test_cargo)
        print(f"Статус: {response.status_code}")
        print("Рекомендации:")
        pprint(response.json()["recommendations"])
        print()
        
        # 5. Оптимизация стоимости
        print("5. Рекомендации по оптимизации стоимости:")
        response = requests.post(f"{BASE_URL}/optimize/cost", json=test_cargo)
        print(f"Статус: {response.status_code}")
        print("Рекомендации:")
        pprint(response.json())
        print()
        
        # 6. Рекомендации с учетом погодных условий
        print("6. Рекомендации с учетом погодных условий:")
        response = requests.post(f"{BASE_URL}/recommend/weather", json=test_cargo)
        print(f"Статус: {response.status_code}")
        print("Рекомендации:")
        pprint(response.json())
        print()
        
        print("\nТестирование завершено успешно!")
        print("Для просмотра визуального отчета откройте файл cargo_analysis_report.html")
        
    except requests.exceptions.ConnectionError:
        print("Ошибка: Не удалось подключиться к серверу. Убедитесь, что API сервер запущен.")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    test_system() 