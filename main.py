from fastapi.middleware.cors import CORSMiddleware
from api import setup_routers as setup_routers_api
from config_reader import dp, app, config
import uvicorn

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(setup_routers_api())

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=config.APP_HOST,
        port=config.APP_PORT,
    )
