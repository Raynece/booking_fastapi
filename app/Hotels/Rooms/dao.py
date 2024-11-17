from datetime import date

from sqlalchemy import and_, func, select

from app.Bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.Hotels.models import Hotels
from app.Hotels.Rooms.models import Rooms


class RoomDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_available_rooms(
            cls,
            hotel_id:int,
            date_from:date,
            date_to:date
    ):
        async with async_session_maker() as session:
            relbook = select(
                Rooms.id,
                func.count().label('booked_rooms')
            ).select_from(Rooms).join(Bookings,Rooms.id == Bookings.room_id).filter(Bookings.date_from<=date_to,Bookings.date_to>=date_from).group_by(Rooms.id).cte('rb')

            relhot = select(Hotels).select_from(Hotels).filter(Hotels.id==hotel_id).cte('rh')

            query = (select(
                relhot.c.id.label('hotel_id'),
                Rooms.id,
                Rooms.name,
                Rooms.description,
                Rooms.services,
                Rooms.price,
                Rooms.quantity,
                Rooms.image_id,
                ((date_to-date_from).days * Rooms.price).label('total_cost'),
                (Rooms.quantity-func.coalesce(relbook.c.booked_rooms,0)).label('rooms_left'))
            .select_from(relhot)
            .join(Rooms,relhot.c.id == Rooms.hotel_id)
            .join(relbook,Rooms.id == relbook.c.id,isouter=True))

            res = await session.execute(query)
            return res.mappings().all()

