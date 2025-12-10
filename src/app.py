from fastapi import FastAPI, Response
import requests
import os
import time
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Histogram, Gauge

app = FastAPI()

REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

TEMPERATURE_GAUGE = Gauge(
    'weather_temperature_celsius',
    'Current temperature in Celsius',
    ['city']
)

ERROR_COUNT = Counter(
    'http_errors_total',
    'Total HTTP errors',
    ['endpoint']
)

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
CITY = os.getenv("CITY", "Moscow")

@app.middleware("http")
async def prometheus_middleware(request, call_next):
    start_time = time.time()
    method = request.method
    endpoint = request.url.path
    
    try:
        response = await call_next(request)
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=response.status_code).inc()
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(time.time() - start_time)
        
        if response.status_code >= 400:
            ERROR_COUNT.labels(endpoint=endpoint).inc()
            
        return response
    except Exception:
        ERROR_COUNT.labels(endpoint=endpoint).inc()
        raise

@app.get("/")
async def get_weather():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        temp = data["main"]["temp"]

        TEMPERATURE_GAUGE.labels(city=CITY).set(temp)
        
        return {
            "city": CITY,
            "temperature": temp,
            "unit": "Celsius",
            "status": "success"
        }
    except Exception as e:
        return {
            "error": e,
            "status": "failed"
        }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)