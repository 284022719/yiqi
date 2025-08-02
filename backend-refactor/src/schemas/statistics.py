from pydantic import BaseModel
from typing import List, Optional

class ClassDistribution(BaseModel):
    class_name: str
    count: int
    percentage: float

class RealmDistribution(BaseModel):
    realm_name: str
    count: int
    percentage: float

class ScoreDistribution(BaseModel):
    range: str
    count: int

class MythicPlusStats(BaseModel):
    average_score: Optional[float]
    max_score: Optional[float]
    active_players: int
    score_distribution: List[ScoreDistribution]

class TopPlayer(BaseModel):
    id: int
    name: str
    realm_name: str
    level: Optional[int]
    class_name: Optional[str]
    faction: str
    mythic_plus_score: Optional[float]
    achievement_points: Optional[int]
    mounts_count: Optional[int]
    average_item_level: Optional[float]

class Statistics(BaseModel):
    total_members: int
    active_members: int
    online_members: int
    classes_count: int
    realms_count: int
    average_level: Optional[float]
    average_item_level: Optional[float]
    average_mythic_plus_score: Optional[float]
    average_achievement_points: Optional[float]
    max_level: Optional[int]
    max_item_level: Optional[float]
    max_mythic_plus_score: Optional[float]
    max_achievement_points: Optional[int]
    top_mythic_players: List[TopPlayer]
    top_mount_collectors: List[TopPlayer]
    top_achievement_players: List[TopPlayer]

    class Config:
        from_attributes = True 