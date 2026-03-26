import json
from kafka import KafkaConsumer
from app.config import settings


def create_consumer() -> KafkaConsumer:
    return KafkaConsumer(
        settings.kafka_topic_orders,
        bootstrap_servers=settings.kafka_bootstrap_servers,
        group_id=settings.kafka_consumer_group,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )