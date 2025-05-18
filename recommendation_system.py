import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Optional
import json
import joblib
from datetime import datetime
from visualization import CargoVisualizer

class CargoRecommendationSystem:
    def __init__(self):
        self.data = None
        self.scaler = StandardScaler()
        self.model = None
        self.visualizer = CargoVisualizer()
        
    def load_data(self, file_path: str):
        """Загрузка данных о грузоперевозках"""
        self.data = pd.read_csv(file_path)
        
    def preprocess_data(self):
        """Предобработка данных"""
        if self.data is None:
            raise ValueError("Данные не загружены")
            
        # Выбираем числовые признаки для кластеризации
        features = ['weight', 'distance', 'delivery_time', 'cost']
        X = self.data[features].copy()
        
        # Масштабирование данных
        X_scaled = self.scaler.fit_transform(X)
        return X_scaled
        
    def train_model(self, n_clusters: int = 5):
        """Обучение модели кластеризации"""
        X_scaled = self.preprocess_data()
        self.model = KMeans(n_clusters=n_clusters, random_state=42)
        self.data['cluster'] = self.model.fit_predict(X_scaled)
        
        # Генерация визуализаций
        self.visualizer.generate_report(self.data, self.data['cluster'])
        
    def save_model(self, path: str = "cargo_model"):
        """Сохранение модели и скейлера"""
        if self.model is None:
            raise ValueError("Модель не обучена")
            
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'timestamp': datetime.now().isoformat()
        }
        joblib.dump(model_data, f"{path}.joblib")
        
    def load_model(self, path: str = "cargo_model"):
        """Загрузка сохраненной модели"""
        model_data = joblib.load(f"{path}.joblib")
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        
    def get_route_recommendations(self, cargo_data: Dict) -> List[Dict]:
        """Получение рекомендаций по маршрутам"""
        if self.model is None:
            raise ValueError("Модель не обучена")
            
        # Преобразование входных данных
        input_features = np.array([[
            cargo_data['weight'],
            cargo_data['distance'],
            cargo_data['delivery_time'],
            cargo_data['cost']
        ]])
        
        # Масштабирование входных данных
        input_scaled = self.scaler.transform(input_features)
        
        # Определение кластера для нового груза
        cluster = self.model.predict(input_scaled)[0]
        
        # Поиск похожих маршрутов в том же кластере
        similar_routes = self.data[self.data['cluster'] == cluster]
        
        # Сортировка по схожести
        recommendations = []
        for _, route in similar_routes.iterrows():
            recommendations.append({
                'route_id': route['route_id'],
                'similarity_score': float(route['success_rate']),
                'estimated_time': float(route['delivery_time']),
                'estimated_cost': float(route['cost']),
                'cluster': int(route['cluster'])
            })
            
        return sorted(recommendations, key=lambda x: x['similarity_score'], reverse=True)[:5]
        
    def get_vehicle_recommendations(self, cargo_data: Dict) -> List[Dict]:
        """Рекомендации по выбору транспорта"""
        recommendations = []
        
        # Простая логика выбора транспорта на основе веса и расстояния
        weight = cargo_data['weight']
        distance = cargo_data['distance']
        
        if weight < 1000 and distance < 100:
            recommendations.append({
                'vehicle_type': 'small_truck',
                'capacity': 'до 1 тонны',
                'suitable_for': 'короткие городские перевозки',
                'estimated_fuel_consumption': '10-12 л/100км',
                'advantages': ['Экономичность', 'Маневренность', 'Простота парковки']
            })
        elif weight < 5000 and distance < 500:
            recommendations.append({
                'vehicle_type': 'medium_truck',
                'capacity': 'до 5 тонн',
                'suitable_for': 'региональные перевозки',
                'estimated_fuel_consumption': '15-18 л/100км',
                'advantages': ['Оптимальное соотношение грузоподъемности и расхода топлива', 'Универсальность']
            })
        else:
            recommendations.append({
                'vehicle_type': 'large_truck',
                'capacity': 'более 5 тонн',
                'suitable_for': 'межрегиональные перевозки',
                'estimated_fuel_consumption': '25-30 л/100км',
                'advantages': ['Высокая грузоподъемность', 'Комфорт для водителя', 'Экономичность при больших объемах']
            })
            
        return recommendations
        
    def get_cost_optimization(self, cargo_data: Dict) -> Dict:
        """Рекомендации по оптимизации стоимости"""
        recommendations = {
            'current_cost': cargo_data['cost'],
            'optimization_suggestions': [],
            'potential_savings': 0
        }
        
        # Анализ и рекомендации по оптимизации
        if cargo_data['distance'] > 500:
            recommendations['optimization_suggestions'].append({
                'suggestion': 'Рассмотрите возможность использования железнодорожного транспорта',
                'potential_savings_percent': 20,
                'reason': 'Для больших расстояний железнодорожный транспорт может быть более экономичным'
            })
            
        if cargo_data['delivery_time'] > 24:
            recommendations['optimization_suggestions'].append({
                'suggestion': 'Оптимизация маршрута может сократить время доставки',
                'potential_savings_percent': 15,
                'reason': 'Сокращение времени в пути снижает расходы на топливо и обслуживание'
            })
            
        # Расчет потенциальной экономии
        total_savings_percent = sum(s['potential_savings_percent'] for s in recommendations['optimization_suggestions'])
        recommendations['potential_savings'] = cargo_data['cost'] * (total_savings_percent / 100)
        
        return recommendations
        
    def get_weather_recommendations(self, cargo_data: Dict) -> Dict:
        """Рекомендации с учетом погодных условий"""
        recommendations = {
            'weather_considerations': [],
            'safety_recommendations': []
        }
        
        # Примеры рекомендаций (в реальной системе здесь был бы API погоды)
        if cargo_data['distance'] > 300:
            recommendations['weather_considerations'].append(
                'Рекомендуется проверить прогноз погоды на маршруте'
            )
            recommendations['safety_recommendations'].append(
                'Убедитесь, что транспортное средство оборудовано для работы в различных погодных условиях'
            )
            
        return recommendations 