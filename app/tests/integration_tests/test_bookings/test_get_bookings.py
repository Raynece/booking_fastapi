import pytest
from httpx import AsyncClient

from app.dao.base import BaseDAO


async def test_hotel_bookings(authenticate_ac: AsyncClient):
    response = await authenticate_ac.get('/bookings')

    print(response.json())
    assert response.json() is not None
    for i in range(1,3):
        response = await authenticate_ac.delete(f'/bookings/{i}')
        print(response.json())

    response = await authenticate_ac.get('/bookings')
    print(response.json())
    assert len(response.json())==0

@pytest.mark.parametrize("room_id,date_from,date_to,status_code", [
    (2,'2024-10-12','2024-10-17',200),
    (2,'2024-10-12','2024-10-17',200),
])
async def test_work_with_bookings(room_id,date_from,date_to,status_code,authenticate_ac: AsyncClient):
    response = await authenticate_ac.post('/bookings', params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })

    booking_id = response.json()['id']
    assert response.status_code == status_code

    response = await authenticate_ac.get(f'/bookings/{booking_id}')
    print(response.json())

    response = await authenticate_ac.delete(f'/bookings/{booking_id}')
    print(response.json())
    response = await authenticate_ac.get('/bookings')
    print(response.json())
    assert len(response.json()) == 0
