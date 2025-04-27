import strawberry

from datetime import datetime
from typing import Optional


@strawberry.type
class Game:
    id: str
    name: str
    type: str
    publisher_name: str
    external_game_id: str
    description: Optional[str]
    is_featured: bool
    cover_image_url: str
    created_ts: datetime
    updated_ts: datetime


@strawberry.input
class GameInput:
    name: str
    type: str
    publisher_name: str
    external_game_id: str
    description: Optional[str] = None
    is_featured: bool = False
    cover_image_url: str


@strawberry.input
class GameUpdateInput:
    name: Optional[str] = None
    type: Optional[str] = None
    publisher_name: Optional[str] = None
    external_game_id: Optional[str] = None
    description: Optional[str] = None
    is_featured: Optional[bool] = None
    cover_image_url: Optional[str] = None
