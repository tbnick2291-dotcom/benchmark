from pydantic import BaseModel


class EloEntry(BaseModel):
    model_id: int
    model_name: str
    dimension: str
    rating: float
    wins: int
    losses: int
    ties: int

    model_config = {"from_attributes": True}


class LeaderboardResponse(BaseModel):
    dimension: str
    entries: list[EloEntry]
