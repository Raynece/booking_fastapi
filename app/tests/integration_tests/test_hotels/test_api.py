import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("location,date_from,date_to,status_code", [
    ("Altay", "2024-10-25","2024-11-10",200),
    ("Altay", "2024-10-25","2024-11-10",200),
    ("Altay", "2024-10-25","2024-11-27",400),
    ("Altay", "2024-11-25","2024-11-15",400),
    ])
async def test_get_hotels_by_location_and_time(location, date_from, date_to, status_code,
                                               authenticate_ac: AsyncClient):
    response = await authenticate_ac.get('/hotels',params={
        "location": location,
        "date_from":date_from,
        "date_to":date_to,
    })

    assert response.status_code == status_code




