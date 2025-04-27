import strawberry

from strawberry.exceptions import GraphQLError
from bson import ObjectId
from datetime import datetime, timezone
from typing import List, Optional

from app_game.db import get_db
from app_game.models import Game, GameInput, GameUpdateInput
from app_game.serializers import game_serializer
from app_game.utils import is_url


@strawberry.type
class Query:
    @staticmethod
    def get_game_resolver(game_id: str) -> Optional[Game]:
        try:
            game = get_db().games.find_one({'_id': ObjectId(game_id)})
            if not game:
                raise GraphQLError(
                    message=f'Game with ID: {game_id} was not found.',
                )
            return game_serializer(game)
        except Exception as e:
            if isinstance(e, GraphQLError):
                raise e
            raise GraphQLError(
                message=f'Internal server error: {str(e)}',
            )

    @staticmethod
    def get_all_games_resolver() -> List[Game]:
        try:
            games = get_db().games.find()
            return [game_serializer(game) for game in games]
        except Exception as e:
            raise GraphQLError(
                message=f'Internal server error: {str(e)}',
            )

    get_game: Optional[Game] = strawberry.field(resolver=get_game_resolver)
    get_all_games: List[Game] = strawberry.field(resolver=get_all_games_resolver)


@strawberry.type
class Mutation:
    @staticmethod
    def create_game_resolver(game_input: GameInput) -> Game:
        try:
            duplicate_external_id = get_db().games.find_one({'external_game_id': game_input.external_game_id})
            if duplicate_external_id:
                raise GraphQLError(
                    message='Game with the provided external id already exists.'
                )

            if not is_url(game_input.cover_image_url):
                raise ValueError(
                    'The provided URL format is incorrect.'
                )

            game_data = {}
            for key, value in game_input.__dict__.items():
                if not key.startswith('_'):
                    game_data[key] = value

            game_data['created_ts'], game_data['updated_ts'] = datetime.now(timezone.utc), datetime.now(timezone.utc)

            game_to_be_created = get_db().games.insert_one(game_data)
            game = get_db().games.find_one({'_id': game_to_be_created.inserted_id})
            if not game:
                raise GraphQLError(
                    message='The game could not be created.'
                )
            return game_serializer(game)
        except Exception as e:
            if isinstance(e, GraphQLError) or isinstance(e, ValueError):
                raise e
            raise GraphQLError(
                message=f'Internal server error: {str(e)}',
            )

    @staticmethod
    def update_game_resolver(game_id: str, game_input: GameUpdateInput) -> Optional[Game]:
        try:
            if hasattr(game_input, 'external_game_id'):
                duplicate_external_id = get_db().games.find_one({
                    'external_game_id': game_input.external_game_id,
                    '_id': {'$ne': ObjectId(game_id)}
                })
                if duplicate_external_id:
                    raise GraphQLError(
                        message='A game with the provided external id already exists.'
                    )

            if hasattr(game_input, 'cover_image_url') and not is_url(game_input.cover_image_url):
                raise ValueError(
                    'The provided URL format is incorrect.'
                )

            if not get_db().games.find_one({'_id': ObjectId(game_id)}):
                raise GraphQLError(
                    message=f'Game with ID: {game_id} was not found.'
                )

            game_update_data = {}
            for key, value in game_input.__dict__.items():
                if not key.startswith('_') and value is not None:
                    game_update_data[key] = value

            game_update_data['updated_ts'] = datetime.now(timezone.utc)

            game_to_update = get_db().games.update_one(
                {"_id": ObjectId(game_id)},
                {"$set": game_update_data}
            )
            if game_to_update.matched_count == 0:
                raise GraphQLError(
                    message=f'Game with ID: {game_id} could not be updated.'
                )
            updated_game = get_db().games.find_one({'_id': ObjectId(game_id)})
            return game_serializer(updated_game)
        except Exception as e:
            if isinstance(e, GraphQLError) or isinstance(e, ValueError):
                raise e
            raise GraphQLError(
                message=f'Internal server error: {str(e)}',
            )

    @staticmethod
    def delete_game_resolver(game_id: str) -> bool:
        try:
            game_to_delete = get_db().games.delete_one({"_id": ObjectId(game_id)})
            if game_to_delete.deleted_count == 0:
                raise GraphQLError(
                    message=f'Game with ID: {game_id} was not found.'
                )
            return True
        except Exception as e:
            if isinstance(e, GraphQLError):
                raise e
            raise GraphQLError(
                message=f'Internal server error: {str(e)}',
            )

    create_game: Game = strawberry.field(resolver=create_game_resolver)
    update_game: Optional[Game] = strawberry.field(resolver=update_game_resolver)
    delete_game: bool = strawberry.field(resolver=delete_game_resolver)


schema = strawberry.Schema(query=Query, mutation=Mutation)

