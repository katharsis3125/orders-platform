import os


class Settings:
    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    postgres_db: str = os.getenv("POSTGRES_DB", "orders_db")
    postgres_user: str = os.getenv("POSTGRES_USER", "orders_user")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "orders_pass")

    kafka_bootstrap_servers: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    kafka_topic_orders: str = os.getenv("KAFKA_TOPIC_ORDERS", "orders")
    kafka_consumer_group: str = os.getenv("KAFKA_CONSUMER_GROUP", "orders-worker-group")

    @property
    def database_url(self) -> str:
        return (
            f"dbname={self.postgres_db} "
            f"user={self.postgres_user} "
            f"password={self.postgres_password} "
            f"host={self.postgres_host} "
            f"port={self.postgres_port}"
        )


settings = Settings()