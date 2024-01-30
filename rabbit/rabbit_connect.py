from typing import Tuple

import pika
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection

from read_config import get_conf_value

rabbit_user = get_conf_value("RABBIT_MQ", "user")
rabbit_pass = get_conf_value("RABBIT_MQ", "pass")
rabbit_host = get_conf_value("RABBIT_MQ", "host")
rabbit_port = get_conf_value("RABBIT_MQ", "port")
rabbit_exchange = get_conf_value("RABBIT_MQ", "exchange_name")
rabbit_queue = get_conf_value("RABBIT_MQ", "queue_name")


def make_channel() -> Tuple[BlockingChannel, BlockingConnection]:
    credentials = pika.PlainCredentials(rabbit_user, rabbit_pass)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=rabbit_host, port=rabbit_port, credentials=credentials
        )
    )
    channel = connection.channel()
    return channel, connection


def make_exchange_queue_bind(exchange_name: str = rabbit_exchange,
                             queue_name: str = rabbit_queue):
    channel, connection = make_channel()

    channel.exchange_declare(exchange=exchange_name, exchange_type="direct")
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange=exchange_name, queue=queue_name)
    return channel, connection
