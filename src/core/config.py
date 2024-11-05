"""The project settings like the database connection URL."""

from environs import Env

env = Env()
env.read_env()


class Config:
    # Bot config.
    BOT_TOKEN = env("BOT_TOKEN")
    BOT_LOGS_FILEPATH = env("BOT_LOGS_FILEPATH")

    # Proxy config.
    PROXY = {
        "https": env("PROXY_HTTPS"), 
        "http": env("PROXY_HTTP")
    }
    PROXY_CHANGE_URL = env("PROXY_CHANGE_URL")

    # Database config.
    DATABASE_HOST = env("DATABASE_HOST")
    DATABASE_NAME = env("DATABASE_NAME")
    DATABASE_USERNAME = env("DATABASE_USERNAME")
    DATABASE_PASSWORD = env("DATABASE_PASSWORD")
    PATH_TO_SQL_QUERIES = env("PATH_TO_SQL_QUERIES")

    # Parser config.
    CLIENT_NOTIFIER_LOGS = env("CLIENT_NOTIFIER_LOGS")


config = Config()