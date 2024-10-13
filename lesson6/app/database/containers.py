"""Containers module."""

from dependency_injector import containers, providers
from sqlmodel import Session, create_engine
from .services import VectorDBService, SQLDBService
from loguru import logger



class Container(containers.DeclarativeContainer):

    config = providers.Configuration("config")
    config.vec_host.from_env("VEC_HOST", required=True)
    config.vec_port.from_env("VEC_PORT", required=True)
    config.sql_host.from_env("SQL_HOST", required=True)
    config.sql_port.from_env("SQL_PORT", required=True)
    config.sql_user.from_env("SQL_USER", required=True)
    config.sql_pass.from_env("SQL_PASS", required=True)
    config.sql_name.from_env("SQL_NAME", required=True)

    # Services

    vector_service = providers.Singleton(
        VectorDBService,
        host=config.vec_host,
        port=config.vec_port,
    )

    sql_service = providers.Singleton(
        SQLDBService,
        config.sql_host,
        config.sql_port,
        config.sql_user,
        config.sql_pass,
        config.sql_name,
    )

