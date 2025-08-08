from contextlib import asynccontextmanager
from typing import AsyncGenerator

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from aiogram import Bot, Dispatcher
from fastapi import FastAPI
from tortoise import Tortoise
from dotenv import load_dotenv
import os

load_dotenv()

bot_name = os.getenv("BOT_NAME")
webapp_url = os.getenv("WEBAPP_URL")
app_port = os.getenv("APP_PORT")

class Config(BaseSettings):
    BOT_TOKEN: SecretStr

    WEBAPP_URL: str = webapp_url
    WEBHOOK_URL: str = f"{WEBAPP_URL}/{bot_name}"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = app_port
    DB_URL: SecretStr

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

@asynccontextmanager
async def lifespan() -> AsyncGenerator:
    await bot.set_webhook(
        url=f"{config.WEBHOOK_URL}/webhook",
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )
    await Tortoise.init(TORTOISE_ORM)
    yield
    await Tortoise.close_connections()
    await bot.session.close()


config = Config()
bot = Bot(config.BOT_TOKEN.get_secret_value())
dp = Dispatcher()
app = FastAPI(lifespan=lifespan)

TORTOISE_ORM = {
    "connections": {"default": config.DB_URL.get_secret_value()},
    "apps": {
        "models": {
            "models": ["db.models.user", "aerich.models"],
            "default_connection": "default",
        },
    },
}
