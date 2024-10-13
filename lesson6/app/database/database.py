from chromadb import Collection
from dependency_injector.wiring import Provide, inject
from sqlmodel import Session, SQLModel
from sqlalchemy import Engine
from .containers import Container
from .services import VectorDBService, SQLDBService


@inject
def get_collection(vector: VectorDBService = Provide[Container.vector_service]) -> Collection:
    return vector.get_collection(name="games")

@inject
def get_session(sql: SQLDBService = Provide[Container.sql_service]) -> Session:
    return sql.get_session()

@inject
def init_db(sql: SQLDBService = Provide[Container.sql_service]):
    """Initialize database"""
    SQLModel.metadata.drop_all(sql.get_engine())
    SQLModel.metadata.create_all(sql.get_engine())