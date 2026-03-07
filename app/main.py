from fastapi import FastAPI, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI()

REQUESTS = Counter("api_requests_total", "Total API requests", ["path", "method", "status"])
LATENCY = Histogram("api_request_latency_seconds", "Request latency", ["path"])

@app.middleware("http")
async def metrics_middleware(request, call_next):
    path = request.url.path
    method = request.method
    with LATENCY.labels(path=path).time():
        response = await call_next(request)
    REQUESTS.labels(path=path, method=method, status=str(response.status_code)).inc()
    return response

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/hello")
def hello():
    return {"message": "hello"}
