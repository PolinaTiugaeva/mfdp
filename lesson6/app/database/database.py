from dependency_injector.wiring import Provide, inject
from sqlmodel import Session, SQLModel
from sqlalchemy import Engine
from .containers import Container
from .services import SQLDBService, QueueService


@inject
def get_session(sql: SQLDBService = Provide[Container.sql_service]) -> Session:
    return sql.get_session()

@inject
def init_db(sql: SQLDBService = Provide[Container.sql_service]):
    """Initialize database"""
    SQLModel.metadata.drop_all(sql.get_engine())
    SQLModel.metadata.create_all(sql.get_engine())

@inject
def get_chanel(q_service: QueueService = Provide[Container.q_service]):
    return q_service.get_chanel()
