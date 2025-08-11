from contextlib import asynccontextmanager
from typing import AsyncGenerator

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from aiogram import Bot, Dispatcher
from fastapi import FastAPI

class Config(BaseSettings):
    BOT_TOKEN: SecretStr
    WEBHOOK_URL: str
    WEBAPP_URL: str
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int
    DB_URL: SecretStr

    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    url = f"{config.WEBHOOK_URL}/webhook"
    print("Webhook URL:", url)
    await bot.set_webhook(
        url=f"{config.WEBHOOK_URL}/webhook",
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )
    yield
    await bot.session.close()


config = Config()
bot = Bot(config.BOT_TOKEN.get_secret_value())
dp = Dispatcher()
app = FastAPI(lifespan=lifespan)
