import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "3307"))
    db_user: str = os.getenv("DB_USER", "root")
    db_password: str = os.getenv("DB_PASSWORD", "123456")
    db_name: str = os.getenv("DB_NAME", "news_management")
    link_job_time: str = os.getenv("LINK_JOB_TIME", "08:00")
    detail_job_interval_minutes: int = int(os.getenv("DETAIL_JOB_INTERVAL_MINUTES", "30"))
    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "15"))


settings = Settings()
