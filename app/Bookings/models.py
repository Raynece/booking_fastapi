from datetime import date

from sqlalchemy import Column, Computed, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base


class Bookings(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[date] = mapped_column(Date)
    date_to: Mapped[date] = mapped_column(Date)
    price: Mapped[int]
    total_cost: Mapped[int] = mapped_column(Computed("(date_to - date_from) * price"))
    total_days: Mapped[int] = mapped_column(Computed("date_to - date_from"))

    user: Mapped["Users"] = relationship(back_populates="bookings")
    room: Mapped["Rooms"] = relationship(back_populates="booking")
