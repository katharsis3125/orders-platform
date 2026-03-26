import os


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "orders-api")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))

    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "orders_db")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "orders_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "orders_pass")
    
    kafka_enabled: bool = os.getenv("KAFKA_ENABLED", "false").lower() == "true"
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    KAFKA_TOPIC_ORDERS: str = os.getenv("KAFKA_TOPIC_ORDERS", "orders")
    


    @property
    def database_url(self) -> str:
        return (
            f"dbname={self.POSTGRES_DB} "
            f"user={self.POSTGRES_USER} "
            f"password={self.POSTGRES_PASSWORD} "
            f"host={self.POSTGRES_HOST} "
            f"port={self.POSTGRES_PORT}"
        )


settings = Settings()