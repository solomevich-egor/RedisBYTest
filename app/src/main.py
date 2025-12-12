import httpx
from fastapi import APIRouter, FastAPI
from src.api import router
from src.configs import RetailCRMConfig


async def lifespan(app: FastAPI):
    async with httpx.AsyncClient(
        headers={"X-API-KEY": RetailCRMConfig().api_key.get_secret_value()}
    ) as client:
        app.state.async_client = client
        yield


app = FastAPI(
    title="RedisBy test api",
    description="",
    swagger_ui_parameters={"displayRequestDuration": True},
    lifespan=lifespan,
)

api_router = APIRouter(prefix="/api")
api_router.include_router(router)

app.include_router(api_router)
