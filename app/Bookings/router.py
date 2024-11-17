from datetime import date

from fastapi import APIRouter, Depends
from pydantic import TypeAdapter

from fastapi_versioning import version
from app.Bookings.dao import BookingDAO
from app.Bookings.schemas import SBooking
from app.exceptions import RoomCannotBeBooked
from app.tasks.tasks import send_booking_confirmation_email
from app.Users.dependencies import get_current_user
from app.Users.models import Users

router = APIRouter(
    prefix='/bookings',
    tags=['Бронирование']
)

@router.get("")
@version(1)
async def get_bookings(user: Users = Depends(get_current_user)):
     return await BookingDAO.find_all(user_id = user.id)

@router.get('/{booking_id}')
@version(1)
async def get_booking_by_id(booking_id:int, user: Users = Depends(get_current_user)):
    return await BookingDAO.find_by_id(booking_id)





@router.post('')
@version(1)
async def add_booking(
        room_id: int, date_from: date, date_to: date,
        user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(user_id=user.id,room_id=room_id,date_from=date_from,date_to=date_to)
    booking_dict = TypeAdapter(SBooking).validate_python(booking).model_dump()
    send_booking_confirmation_email.delay(booking_dict,user.email)
    if not booking:
        raise RoomCannotBeBooked
    return booking_dict

@router.delete('/{booking_id}')
@version(1)
async def delete_booking(booking_id:int,user:Users = Depends(get_current_user)):
    return await BookingDAO.delete_booking(booking_id, user.id)