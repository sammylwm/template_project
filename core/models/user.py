from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger


class User(Base):
    uid: Mapped[int] = mapped_column(BigInteger, unique=True, primary_key=True)
    count_schemes: Mapped[int] = mapped_column(default=0)
    verify: Mapped[bool] = mapped_column(default=False)
    verify_id: Mapped[bool] = mapped_column(default=False)
