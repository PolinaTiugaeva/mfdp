import json
import os
import pika
from loguru import logger
from database.containers import Container
from database.database import get_chanel, get_session
from services.crud import history
from models.history import History

def process_request(ch, method, properties, body):
    logger.info(f'body - {body}')
    message = json.loads(body)
    logger.info(f'message - {message}')
    session = get_session()
    recommendations = history.get_recommendations(message['username'], session)
    logger.info(f'result - {recommendations}')
    new_game_score = []
    for game_score in message['titles']:
        score = game_score[1]
        if game_score[0] in recommendations:
            score *= 10
        new_game_score.append((game_score[0], score))
    result = json.dumps({
        'username' : message['username'],
        'chat_id' : message['chat_id'],
        'game_scores' : new_game_score
    })
    logger.info(result)
    ch.basic_publish(
        exchange='',
        routing_key='notify_queue',
        body=result,
        properties=pika.BasicProperties(
            delivery_mode=2
        )        
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)



if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__], packages=["database"])
    chanel = get_chanel()
    chanel.queue_declare(queue='sort_request', durable=True)
    chanel.basic_consume(queue='sort_request', on_message_callback=process_request)
    logger.info("Start consumption")
    chanel.start_consuming()