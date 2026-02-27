from fastapi import FastAPI, Request, Response
from prometheus_client import (
    Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
)

app = FastAPI()

# Counter of all requests
REQUESTS_COUNT = Counter(
    'request_count',
    'Total number of requests',
    ['method', 'endpoint', 'http_status']
)

# Latency
REQUESTS_LATENCY = Histogram(
    'request_latency_seconds',
    'Request latency',
    ['endpoint']
)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    import time
    response = await call_next(request)
    resp_time = time.time()

    endpoint = request.url.path
    REQUESTS_COUNT.labels(
        request.method,
        endpoint,
        response.status_code
    ).inc()

    REQUESTS_LATENCY.labels(endpoint).observe(resp_time)

    return response


# Prometheus endpoint
@app.get("/metrics")
async def metrics():
    return Response(generate_latest, media_type=CONTENT_TYPE_LATEST)
