from datetime import date

from sqlalchemy import and_, func, select
from sqlalchemy.orm import aliased

from app.Bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.Hotels.models import Hotels
from app.Hotels.Rooms.models import Rooms


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all(cls,user_id: int):
        bookings = await BaseDAO.find_all()

    @classmethod
    async def find_available_hotels(cls,
                                    location:str,
                                    date_from:date,
                                    date_to:date):
        async with async_session_maker() as session:

            bfd = (select(Bookings).where(and_(Bookings.date_from<=date_to,Bookings.date_to>=date_from))).cte('bfd')

            rb = (select(Rooms.hotel_id,func.count().label('booked_rooms')).select_from(Rooms).join(bfd,Rooms.id == bfd.c.room_id).group_by(Rooms.hotel_id)).cte('rb')

            query = (select(
                Hotels.id,
                Hotels.name,
                Hotels.location,
                Hotels.services,
                Hotels.rooms_quantity,
                Hotels.image_id,
                (Hotels.rooms_quantity-func.coalesce(rb.c.booked_rooms,0)).label('rooms_left')).select_from(Hotels).join(rb,Hotels.id == rb.c.hotel_id, isouter=True).where(Hotels.location.contains(location),(Hotels.rooms_quantity-func.coalesce(rb.c.booked_rooms,0))>0,

            ))

        res = await session.execute(query)
        return res.mappings().all()

    @classmethod
    async def find_bookings(
            cls,
            user_id):
        async with async_session_maker() as session:
            r = aliased(Bookings)
            b = aliased(Rooms)
            query = select(
                r.room_id,
                r.user_id,
                r.date_from,
                r.date_to,
                r.price,
                r.total_cost,
                r.total_days,
                b.image_id,
                b.name,
                b.description,
                b.services
            ).filter(r.user_id==user_id).select_from(r).join(b,r.user_id==b.id,isouter=True)

            res = await session.execute(query)
            return res.mappings().all()

    @classmethod
    async def get_precise_hotel(cls,hotel_id):
        async with async_session_maker() as session:
            query = select(
                Hotels.id,
                Hotels.name,
                Hotels.location,
                Hotels.services,
                Hotels.rooms_quantity,
                Hotels.image_id
            ).where(Hotels.id==hotel_id)

            res = await session.execute(query)
            return res.mappings().all()



