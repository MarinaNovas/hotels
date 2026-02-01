from datetime import date

from sqlalchemy import ForeignKey, func, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

class BookingsOrm(Base):
    __tablename__ = 'bookings'
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id:Mapped[int] = mapped_column(ForeignKey('rooms.id'))
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'))
    date_from:Mapped[date]
    date_to:Mapped[date]
    price: Mapped[int]

    @hybrid_property
    def total_cost(self) -> int:
        return self.price * (self.date_to - self.date_from).days

    @total_cost.expression
    def total_cost(cls) -> int:
        return cls.price * func.date_part("day", cls.date_to - cls.date_from)

