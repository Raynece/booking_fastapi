import pytest
from httpx import AsyncClient

from app.Users.dao import UsersDAO


@pytest.mark.parametrize("user_id,email,is_user_exist", [
    (1,"test@test.com",True),
    (2,"fil@example.com",True),
    (5,"....",False),
])
async def test_find_user_by_id(user_id, email, is_user_exist, ac:AsyncClient):
    user = await UsersDAO.find_by_id(user_id)
    if is_user_exist:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user