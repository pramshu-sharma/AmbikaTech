### FastAPI Application for Games CRUD Operations

## Steps to run the app:
  1. Clone the repository. ```git clone https://github.com/pramshu-sharma/AmbikaTech```
  2. Access the cloned repository from the terminal. ```cd AmbikaTech```
  3. Run docker compose. ```docker-compose up -d```
  4. The strawberry graphQL playground should be available at http://127.0.0.1:8000/gql

## Notes:
  # Sample Mutations:
  Find example mutation queries in mutations.txt. These can be used to create two sample documents.

  # Local Development:
  If running the app locally without Docker, ensure all active Python server processes are stopped to avoid potential timeout errors.

## GraphQL Endpoints:
  # Queries:
    getGame(ObjectId) — Retrieve a single game document by its Object ID.
    getAllGames — Retrieve all game documents.
  # Mutations:
    createGame — Create a new game document.
    updateGame(ObjectId) — Update an existing game document by Object ID.
    deleteGame(ObjectId) — Delete a game document by Object ID.
    
## Project structure:

  File/Folder	      Purpose
  __init__.py	      Marks directory as a Python package.
  db.py	            Database connection setup.
  main.py	          FastAPI and Strawberry GraphQL server configuration.
  models.py	        Database models and schema definitions.
  schema.py	        GraphQL queries, mutations, and resolvers.
  serializers.py	  Object serialization logic.
  utils.py	        Additional helper functions/utilities.


## Improvements and suggestions:
1. Adding automated test cases using pytest.
2. Database credentials management.
3. Async resolvers for improved performance.
4. Input validation using Pydantic.

  

