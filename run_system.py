import subprocess
import time
import webbrowser
import requests
import sys
import os

def check_dependencies():
    """Проверка и установка зависимостей"""
    print("Проверка зависимостей...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Зависимости установлены успешно")
    except Exception as e:
        print(f"Ошибка при установке зависимостей: {str(e)}")
        return False
    return True

def start_server():
    """Запуск сервера"""
    print("Запуск сервера...")
    try:
        # Запускаем сервер в отдельном процессе
        server_process = subprocess.Popen(
            [sys.executable, "api.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Даем серверу время на запуск
        time.sleep(3)
        
        # Проверяем, запустился ли сервер
        try:
            response = requests.get("http://127.0.0.1:8000/")
            if response.status_code == 200:
                print("Сервер успешно запущен")
                return server_process
        except:
            try:
                response = requests.get("http://127.0.0.1:8080/")
                if response.status_code == 200:
                    print("Сервер успешно запущен на порту 8080")
                    return server_process
            except:
                print("Не удалось запустить сервер")
                server_process.terminate()
                return None
                
    except Exception as e:
        print(f"Ошибка при запуске сервера: {str(e)}")
        return None

def open_browser():
    """Открытие браузера с документацией API"""
    print("Открытие документации API...")
    try:
        webbrowser.open("http://127.0.0.1:8000/docs")
    except:
        try:
            webbrowser.open("http://127.0.0.1:8080/docs")
        except:
            print("Не удалось открыть документацию в браузере")

def main():
    """Основная функция запуска системы"""
    print("Запуск системы рекомендаций для грузоперевозок...")
    
    # Проверяем наличие всех необходимых файлов
    required_files = ["api.py", "recommendation_system.py", "visualization.py", "cargo_data.csv"]
    for file in required_files:
        if not os.path.exists(file):
            print(f"Ошибка: файл {file} не найден")
            return
    
    # Устанавливаем зависимости
    if not check_dependencies():
        return
    
    # Запускаем сервер
    server_process = start_server()
    if not server_process:
        return
    
    # Открываем документацию в браузере
    open_browser()
    
    print("\nСистема запущена и готова к использованию!")
    print("Документация API открыта в вашем браузере")
    print("Для остановки сервера нажмите Ctrl+C")
    
    try:
        # Держим процесс запущенным
        server_process.wait()
    except KeyboardInterrupt:
        print("\nОстановка сервера...")
        server_process.terminate()
        print("Сервер остановлен")

if __name__ == "__main__":
    main() 