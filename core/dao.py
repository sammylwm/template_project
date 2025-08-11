from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from .BaseDb import BaseDAO
from core.models import User


class UserDb(BaseDAO[User]):
    model = User
