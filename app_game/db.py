import os

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))


def get_db():
    try:
        client = MongoClient(
            host=str(os.getenv('MONGO_HOST')),
            port=int(os.getenv('MONGO_PORT'))
        )
        client.admin.command('ping')
        return client.game_db
    except ConnectionFailure as e:
        raise Exception(f'Connection Error: {e}')

