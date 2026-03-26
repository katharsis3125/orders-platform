from fastapi import FastAPI, HTTPException
from app.db import get_connection
from app.schemas import OrderCreate
from app.kafka_producer import send_order_event
from fastapi.middleware.cors import CORSMiddleware
from time import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
from app.config import settings
app = FastAPI(title="orders-api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
REQUEST_COUNT = Counter("app_requests_total", "Total count of requests", ["method", "endpoint", "http_status"])
REQUEST_LATENCY = Histogram("app_request_duration_seconds", "Request latency in seconds", ["method", "endpoint"])
REQUEST_CREATED = Counter("orders_created_total", "Total number of created orders")

@app.middleware("http")
async def prometheus_middleware(request, call_next):
    start_time = time()
    response = await call_next(request)
    duration = time() - start_time
    endpoint = request.url.path
    method = request.method
    status_code = response.status_code
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status_code).inc()
    REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)

    return response

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/health")
def health():
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


@app.get("/orders")
def get_orders():
    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, customer_name, product, status, created_at
            FROM orders
            ORDER BY id;
            """
        )
        orders = cur.fetchall()
        return orders

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


@app.post("/orders")
def create_order(order: OrderCreate):
    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO orders (customer_name, product, status)
            VALUES (%s, %s, %s)
            RETURNING id, customer_name, product, status, created_at;
            """,
            (order.customer_name, order.product, "created"),
        )
        new_order = cur.fetchone()
        conn.commit()
        REQUEST_CREATED.inc()

        if settings.kafka_enabled:
            event = {
                "order_id": new_order["id"],
                "customer_name": new_order["customer_name"],
                "product": new_order["product"],
                "status": new_order["status"],
            }

            send_order_event(event)

        return new_order

    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()