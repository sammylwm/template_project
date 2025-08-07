from fastapi.middleware.cors import CORSMiddleware
from api import setup_routers as setup_routers_api
from config_reader import dp, app, config
from bot.handlers import setup_routers

import uvicorn

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
dp.include_router(setup_routers())
app.include_router(setup_routers_api())

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=config.APP_HOST,
        port=config.APP_PORT,
    )
