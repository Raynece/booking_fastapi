from contextlib import asynccontextmanager
from datetime import date, time
import time
from typing import Annotated
from fastapi import Request

from fastapi import FastAPI, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI, version
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel
from redis import asyncio as aioredis
from sqladmin import Admin, ModelView

import highlight_io
from highlight_io.integrations.fastapi import FastAPIMiddleware
from app.admin.auth import authentication_backend
from app.admin.views import BookingAdmin, HotelAdmin, RoomAdmin, UserAdmin
from app.Bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.Hotels.Rooms.router import router as router_rooms
from app.Hotels.router import router as router_hotels
from app.images.router import router as router_image
from app.logger import logger
from app.pages.router import router as router_pages
from app.Users.models import Users
from app.Users.router import router as router_users
from app.prometheus.router import router as router_prometheus






# `instrument_logging=True` sets up logging instrumentation.
# if you do not want to send logs or are using `loguru`, pass `instrument_logging=False`
H = highlight_io.H(
	settings.CLIENT_ID,
	instrument_logging=True,
	service_name="my-app",
	service_version="git-sha",
	environment="production",
)

@asynccontextmanager
async def lifespan(app: FastAPI):

    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")

    FastAPICache.init(RedisBackend(redis), prefix="cache")

    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router_image)
app.include_router(router_pages)
app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_prometheus)

app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}',
    # description='Greet users with a nice message',
    # middleware=[
    #     Middleware(SessionMiddleware, secret_key='mysecretkey')
    # ]
)

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"]
)
instrumentator.instrument(app).expose(app)

admin = Admin(app, engine,authentication_backend=authentication_backend)

admin.add_view(UserAdmin)
admin.add_view(BookingAdmin)
admin.add_view(HotelAdmin)
admin.add_view(RoomAdmin)
app.add_middleware(FastAPIMiddleware)

app.mount('/static', StaticFiles(directory='app/static'),'static')

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # logger.info("Request handling time", extra={
    #     "process_time": round(process_time,4)
    # })
    return response


class SHotel(BaseModel):
    address: str
    name: str
    stars: int

@app.get('/hotels/{hotel_id}')
def get_hotels(
        location: str,
        date_from: date,
        date_to: date,
        has_spa: bool = None,
        stars: Annotated[int, Query(...,ge=1,le=5)] = None,
) -> list[SHotel]:
    hotels = [
        {'address': 'Something like that',
         'name': 'Super Puper Hotel',
         'stars': 5,
         },
    ]
    return hotels

# class SBooking(BaseModel):
#     room_id: int
#     date_to: date
#     date_from: date
#
# @app.post('/bookings')
# def add_booking(booking: SBooking):
#     pass