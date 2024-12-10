from pydantic import BaseModel


class Place(BaseModel):
    id: int
    name: str
    address: str
    latitude: float
    longitude: float
    rating: float
