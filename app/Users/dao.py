from app.dao.base import BaseDAO
from app.Users.models import Users


class UsersDAO(BaseDAO):
    model = Users