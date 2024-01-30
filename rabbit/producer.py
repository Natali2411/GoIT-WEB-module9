import pika
from rabbit.rabbit_connect import make_exchange_queue_bind
import json
from logger import logger
from read_config import get_conf_value


rabbit_exchange = get_conf_value("RABBIT_MQ", "exchange_name")
rabbit_queue = get_conf_value("RABBIT_MQ", "queue_name")


def publish_author_info(author_name: str, author_part_link: str):
    channel, connection = make_exchange_queue_bind(exchange_name=rabbit_exchange,
                                                   queue_name=rabbit_queue)
    message = {
        "name": author_name,
        "link": author_part_link
    }
    channel.basic_publish(
        exchange=rabbit_exchange,
        routing_key=rabbit_queue,
        body=json.dumps(message).encode(),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ),
    )
    logger.info(" [x] Sent %r" % message)
    connection.close()


if __name__ == "__main__":
    publish_author_info(author_name="Tedd Talk", author_part_link="/ted_talk")

