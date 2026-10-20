from dotenv import load_dotenv
import os


class Config:
    load_dotenv()

    DB_USER = os.getenv("DB_USER")

    DB_PASSWORD = os.getenv("DB_PASSWORD")

    DB_HOST = os.getenv(
        "DB_HOST",
        "localhost"
    )

    DB_PORT = os.getenv(
        "DB_PORT",
        "5432"
    )

    DB_NAME = os.getenv(
        "DB_NAME",
        "archive_db"
    )

    PORT = os.getenv(
        "PORT",
        "8080"
    )

    CONCURRENCY = int(
        os.getenv(
            "CONCURRENCY",
            "4"
        )
    )