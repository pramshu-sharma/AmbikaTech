from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app_game.schema import schema

app = FastAPI()
strawberry_graphql_app = GraphQLRouter(schema)
app.include_router(strawberry_graphql_app, prefix='/gql')