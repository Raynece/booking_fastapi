import asyncio
from datetime import date, datetime
from typing import List

from fastapi import APIRouter, Depends, Query
from fastapi_cache.decorator import cache

from app.exceptions import IncorrectDaysFormat
from app.Hotels.dao import HotelDAO
from app.Hotels.schemas import HotelInfo
from app.Users.dependencies import get_current_user
from app.Users.models import Users

router = APIRouter(prefix='/hotels', tags=['Отели'])

@router.get('')
#@cache(expire=30)
async def get_hotels_by_location_and_time(
        location:str,
        date_from: date = Query(..., description=f'Например, {datetime.now().date()}'),
        date_to: date = Query(..., description=f'Например, {datetime.now().date()}'),
):
    await asyncio.sleep(1)
    hotels = await HotelDAO.find_available_hotels(location,date_from,date_to)
    if ((datetime.strptime(str(date_to),'%Y-%m-%d')-datetime.strptime(str(date_from),'%Y-%m-%d'))).days > 30 or date_from>=date_to:
        raise IncorrectDaysFormat
    return hotels

@router.get('/bookings')
async def get_list_bookings(user:Users = Depends(get_current_user)):
    return await HotelDAO.find_bookings(user.id)

@router.get('/id/{hotel_id}')
async def get_precise_hotel(hotel_id:int):
    return await HotelDAO.get_precise_hotel(hotel_id)