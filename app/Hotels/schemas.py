from datetime import date

from pydantic import BaseModel


class HotelInfo(BaseModel):
    location: str
    date_to: date
    date_from: date