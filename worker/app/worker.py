import time
from app.db import get_connection
from app.kafka_consumer import create_consumer


def process_order(order_event: dict) -> None:
    conn = None
    cur = None

    try:
        order_id = order_event["order_id"]

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE orders
            SET status = %s
            WHERE id = %s
            RETURNING id, customer_name, product, status, created_at;
            """,
            ("processed", order_id),
        )
        updated_order = cur.fetchone()
        conn.commit()

        print(f"Processed order: {updated_order}")

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error processing order: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def main():
    while True:
        try:
            consumer = create_consumer()
            print("Worker started, waiting for messages...")

            for message in consumer:
                print(f"Received message: {message.value}")
                process_order(message.value)

        except Exception as e:
            print(f"Worker error: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)


if __name__ == "__main__":
    main()