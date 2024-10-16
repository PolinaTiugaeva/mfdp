"""Containers module."""

from dependency_injector import containers, providers
from loguru import logger
from .services import QueueService



class Container(containers.DeclarativeContainer):

    config = providers.Configuration("config")
    # bot token
    config.bot_token.from_env("BOT_TOKEN", required=True)
    # queue service
    config.q_host.from_env("Q_HOST", required=True)
    config.q_port.from_env("Q_PORT", required=True)
    config.q_user.from_env("Q_USER", required=True)
    config.q_pass.from_env("Q_PASS", required=True)

    # Services

    q_service = providers.Singleton(
        QueueService,
        config.q_host,
        config.q_port,
        config.q_user,
        config.q_pass,
    )

    def get_bot_token(self):
        return self.config.bot_token
