import json
import threading
from queue import Queue

from pika.adapters.blocking_connection import BlockingChannel

from logger import logger
from rabbit.rabbit_connect import make_exchange_queue_bind
from read_config import get_conf_value

rabbit_exchange = get_conf_value("RABBIT_MQ", "exchange_name")
rabbit_queue = get_conf_value("RABBIT_MQ", "queue_name")


def read_rabbit_msg(channel: BlockingChannel, queue_name: str, result_queue: Queue,
                    locker: threading.RLock):
    def callback(ch, method, properties, body):
        message = json.loads(body.decode())
        logger.info(f" [x] Received {message}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        with locker:
            result_queue.put(message)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    channel.start_consuming()


if __name__ == "__main__":
    urls = []
    channel, connection = make_exchange_queue_bind(exchange_name=rabbit_exchange,
                                                   queue_name=rabbit_queue)
    thread = threading.Thread(target=read_rabbit_msg, args=(channel, rabbit_queue, urls))
    thread.start()
    thread.join()
    # connection.close()
    print(urls)