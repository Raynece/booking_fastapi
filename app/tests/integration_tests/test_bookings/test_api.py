import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("room_id,date_from,date_to,rooms_left,status_code",  *[
    [(4, "2030-05-01", "2030-05-15", i, 200) for i in range(3, 11)] +
    [(4, "2030-05-01", "2030-05-15", 10, 409)] * 2
    ])
async def test_add_and_get_bookings(room_id,date_from, date_to, rooms_left, status_code,
                                    authenticate_ac: AsyncClient):
    response = await authenticate_ac.post('/bookings',params={
        "room_id": room_id,
        "date_from":date_from,
        "date_to": date_to,
    })

    assert response.status_code == status_code

    response = await authenticate_ac.get('/bookings')

    assert len(response.json()) == rooms_left


