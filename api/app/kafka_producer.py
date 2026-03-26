import json
from kafka import KafkaProducer
from app.config import Settings

def create_producer() -> KafkaProducer:
  return KafkaProducer(
    bootstrap_servers=Settings.KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
  )

def send_order_event(event: dict) -> None:
  producer = create_producer()
  producer.send(Settings.KAFKA_TOPIC_ORDERS, event)
  producer.flush()  
  producer.close() 