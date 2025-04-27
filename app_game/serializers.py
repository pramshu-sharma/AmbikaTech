from datetime import datetime, timezone
from app_game.models import Game


def game_serializer(game) -> Game:
    return Game(
        id=str(game.get('_id')),
        name=game.get('name'),
        type=game.get('type'),
        publisher_name=game.get('publisher_name'),
        external_game_id=game.get('external_game_id'),
        description=game.get('description', ''),
        is_featured=game.get('is_featured', False),
        cover_image_url=game.get('cover_image_url'),
        created_ts=game.get('created_ts', datetime.now(timezone.utc)),
        updated_ts=game.get('updated_ts', datetime.now(timezone.utc)),
    )
