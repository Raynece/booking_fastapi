import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email,password,status_code", [
    ("first@try.com","1234",200),
    ("first@try.com","1234",409),
    ("second@try.com","1234",200),
    ("wrongemail","1234",422),
])
async def test_register_user(email, password, status_code, ac:AsyncClient):
    response = await ac.post("/auth/register",json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code

@pytest.mark.parametrize("email,password,status_code",[
    ("first@try.com",'1234',200),
    ('wrong@try.com','1234',401),
])
async def test_login_user(email, password, status_code, ac:AsyncClient):
    response = await ac.post("/auth/login", json={
        "email": email,
        "password": password
    })

    assert response.status_code == status_code