from dependency_injector.wiring import Provide, inject
from .containers import Container
from .services import QueueService



@inject
def get_chanel(q_service: QueueService = Provide[Container.q_service]):
    return q_service.get_chanel()

@inject
def get_bot_token(config = Provide[Container.config]):
    return config['bot_token']
