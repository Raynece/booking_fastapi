from sqladmin import ModelView

from app.Bookings.models import Bookings
from app.Hotels.models import Hotels
from app.Hotels.Rooms.models import Rooms
from app.Users.models import Users


class UserAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name = 'Пользователь'
    name_plural = 'Пользователи'
    icon = 'fa-solid fa-user'

class BookingAdmin(ModelView, model=Bookings):
    column_list = [i.name for i in Bookings.__table__.c] + [Bookings.user]
    name = 'Бронь'
    name_plural = 'Брони'
    icon = 'fa-solid fa-book'

class HotelAdmin(ModelView, model=Hotels):
    column_exclude_list = [Hotels.image_id]
    column_details_exclude_list = [Hotels.image_id]
    can_delete = False
    name = 'Отель'
    name_plural = 'Отели'
    icon = 'fa-solid fa-hotel'

class RoomAdmin(ModelView, model=Rooms):
    column_exclude_list = [Rooms.image_id, Rooms.hotel_id]
    column_details_exclude_list = [Rooms.image_id, Rooms.hotel_id]
    can_delete = False
    name = 'Комната'
    name_plural = 'Комнаты'
    icon = 'fa-solid fa-bed'