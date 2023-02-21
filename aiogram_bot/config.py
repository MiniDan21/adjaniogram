import asyncio

from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    WEBHOOK_HOST: str
    WEBHOOK_PATH: str
    SSL_CERTIFICATE: str
    SSL_PKEY: str
    PAY_TOKEN: SecretStr
    DEBUG = False

    class Config:
        env_file = 'aiogram_bot/.env'
        env_file_encoding = 'utf-8'


def run_async(afunc: callable):
    try:
        loop = asyncio.get_running_loop()
        if loop:
            print('Async event loop already running. Adding coroutine to the event loop.')
            return loop.create_task(afunc())
        else:
            print('Starting new event loop')
            return asyncio.run(afunc())
    except RuntimeError:
        return False


settings = Settings()
