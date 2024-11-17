from datetime import datetime

from app.Bookings.dao import BookingDAO


async def test_add_and_get_bookings():
    new_booking = await BookingDAO.add(
        user_id=2,
        room_id=2,
        date_from=datetime.strptime('2024-09-11','%Y-%m-%d'),
        date_to=datetime.strptime('2024-10-11','%Y-%m-%d'),
    )

    assert new_booking.user_id == 2
    assert new_booking.room_id == 2

    new_booking = await BookingDAO.find_by_id(new_booking.id)

    assert new_booking is not None