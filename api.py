from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Dict, Optional
from recommendation_system import CargoRecommendationSystem
import uvicorn
import os

app = FastAPI(
    title="Cargo Recommendation System API",
    description="API для системы рекомендаций по грузоперевозкам",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")
recommendation_system = CargoRecommendationSystem()

class CargoData(BaseModel):
    weight: float
    distance: float
    delivery_time: float
    cost: float

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/web/recommend", response_class=HTMLResponse)
async def web_recommend(request: Request,
                       weight: float = Form(...),
                       distance: float = Form(...),
                       delivery_time: float = Form(...),
                       cost: float = Form(...)):
    if recommendation_system.model is None:
        if os.path.exists("cargo_data.csv"):
            recommendation_system.load_data("cargo_data.csv")
            recommendation_system.train_model()
            recommendation_system.save_model()
    cargo = {
        "weight": weight,
        "distance": distance,
        "delivery_time": delivery_time,
        "cost": cost
    }
    routes = recommendation_system.get_route_recommendations(cargo)
    vehicles = recommendation_system.get_vehicle_recommendations(cargo)
    cost_optimization = recommendation_system.get_cost_optimization(cargo)
    result = {
        "routes": routes,
        "vehicles": vehicles,
        "cost_optimization": cost_optimization
    }
    return templates.TemplateResponse("index.html", {"request": request, "result": result})

@app.get("/web/report", response_class=HTMLResponse)
async def web_report():
    if os.path.exists("cargo_analysis_report.html"):
        return FileResponse("cargo_analysis_report.html")
    return HTMLResponse("<h2>Отчёт ещё не сгенерирован. Сначала обучите модель.</h2>")

@app.post("/train")
async def train_model():
    try:
        if not os.path.exists("cargo_data.csv"):
            raise HTTPException(status_code=404, detail="Training data file not found")
        recommendation_system.load_data("cargo_data.csv")
        recommendation_system.train_model()
        recommendation_system.save_model()
        return {
            "message": "Model trained successfully",
            "report_url": "cargo_analysis_report.html"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommend/route")
async def get_route_recommendations(cargo_data: CargoData):
    try:
        if recommendation_system.model is None:
            raise HTTPException(status_code=400, detail="Model not trained. Please train the model first.")
        recommendations = recommendation_system.get_route_recommendations(cargo_data.dict())
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommend/vehicle")
async def get_vehicle_recommendations(cargo_data: CargoData):
    try:
        recommendations = recommendation_system.get_vehicle_recommendations(cargo_data.dict())
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/optimize/cost")
async def get_cost_optimization(cargo_data: CargoData):
    try:
        recommendations = recommendation_system.get_cost_optimization(cargo_data.dict())
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommend/weather")
async def get_weather_recommendations(cargo_data: CargoData):
    try:
        recommendations = recommendation_system.get_weather_recommendations(cargo_data.dict())
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model/info")
async def get_model_info():
    try:
        if recommendation_system.model is None:
            return {"status": "Model not trained"}
        return {
            "status": "Model trained",
            "n_clusters": recommendation_system.model.n_clusters,
            "n_samples": len(recommendation_system.data) if recommendation_system.data is not None else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True) 