"""Services module."""
import chromadb
from loguru import logger
from sqlmodel import create_engine, Session
from sqlalchemy import Engine

class VectorDBService():

    def __init__(self, host: str, port: int):
        self.client = chromadb.HttpClient(host=host, port=port)

    def get_collection(self, name: str) -> chromadb.Collection:
        return self.client.get_collection(name)

class SQLDBService():

    def __init__(self, host: str, port: int, user: str, password: str, name: str):
        url = f'postgresql+psycopg://{user}:{password}@{host}:{port}/{name}'
        self.engine = create_engine(
            url=url,
            echo=True,
            pool_size=5,
            max_overflow=10,
        )
        self.session = Session(self.engine)

    def get_session(self) -> Session:
        return self.session

    def get_engine(self) -> Engine:
        return self.engine
