from datetime import date

from app.Hotels.Rooms.dao import RoomDAO
from app.Hotels.router import router


@router.get('/{hotel_id}/rooms')
async def get_rooms_by_hotel(hotel_id:int,date_from:date,date_to:date):
    return await RoomDAO.find_available_rooms(hotel_id,date_from,date_to)