import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

class CargoVisualizer:
    def __init__(self):
        plt.style.use('seaborn-v0_8')
        
    def plot_route_clusters(self, data, clusters):
        """Визуализация кластеров маршрутов"""
        plt.figure(figsize=(12, 8))
        scatter = plt.scatter(data['distance'], data['weight'], 
                            c=clusters, cmap='viridis', 
                            s=data['cost']/100, alpha=0.6)
        plt.colorbar(scatter, label='Кластер')
        plt.xlabel('Расстояние (км)')
        plt.ylabel('Вес (кг)')
        plt.title('Кластеризация маршрутов по расстоянию и весу')
        plt.savefig('route_clusters.png')
        plt.close()
        
    def plot_cost_analysis(self, data):
        """Анализ стоимости перевозок"""
        plt.figure(figsize=(12, 6))
        sns.regplot(data=data, x='distance', y='cost')
        plt.xlabel('Расстояние (км)')
        plt.ylabel('Стоимость (руб)')
        plt.title('Зависимость стоимости от расстояния')
        plt.savefig('cost_analysis.png')
        plt.close()
        
    def plot_delivery_time_analysis(self, data):
        """Анализ времени доставки"""
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=data, x='cluster', y='delivery_time')
        plt.xlabel('Кластер')
        plt.ylabel('Время доставки (часы)')
        plt.title('Распределение времени доставки по кластерам')
        plt.savefig('delivery_time_analysis.png')
        plt.close()
        
    def plot_success_rate_analysis(self, data):
        """Анализ успешности доставки"""
        plt.figure(figsize=(12, 6))
        sns.barplot(data=data, x='cluster', y='success_rate')
        plt.xlabel('Кластер')
        plt.ylabel('Успешность доставки')
        plt.title('Успешность доставки по кластерам')
        plt.savefig('success_rate_analysis.png')
        plt.close()
        
    def generate_report(self, data, clusters):
        """Генерация полного отчета с визуализациями"""
        self.plot_route_clusters(data, clusters)
        self.plot_cost_analysis(data)
        self.plot_delivery_time_analysis(data)
        self.plot_success_rate_analysis(data)
        
        # Создание HTML-отчета
        html_report = f"""
        <html>
        <head>
            <title>Анализ грузоперевозок</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .image-container {{ margin: 20px 0; }}
                img {{ max-width: 100%; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Анализ грузоперевозок</h1>
                <div class="image-container">
                    <h2>Кластеризация маршрутов</h2>
                    <img src="route_clusters.png" alt="Кластеризация маршрутов">
                </div>
                <div class="image-container">
                    <h2>Анализ стоимости</h2>
                    <img src="cost_analysis.png" alt="Анализ стоимости">
                </div>
                <div class="image-container">
                    <h2>Анализ времени доставки</h2>
                    <img src="delivery_time_analysis.png" alt="Анализ времени доставки">
                </div>
                <div class="image-container">
                    <h2>Анализ успешности доставки</h2>
                    <img src="success_rate_analysis.png" alt="Анализ успешности доставки">
                </div>
            </div>
        </body>
        </html>
        """
        
        with open('cargo_analysis_report.html', 'w', encoding='utf-8') as f:
            f.write(html_report) 