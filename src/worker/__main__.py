import asyncio

import click
import pika
from yarl import URL

from src.wikipedia.distance import wikipedia_distance


def callback(channel, method, properties, body) -> None:  # type ignore
    source_url, target_url = body.decode().split()

    d = asyncio.run(wikipedia_distance(URL(source_url), URL(target_url)))
    if d is not None:
        response = "\n".join([str(e) for e in d])
    else:
        response = ""

    channel.basic_publish(
        exchange="",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id
        ),
        body=response
    )
    channel.basic_ack(delivery_tag=method.delivery_tag)


@click.command()
@click.option("--host", default="localhost", type=str)
@click.option("--port", default=5672, type=int)
@click.option("--queue", default="rabbitmqqueue", type=str)
def main(host: str, port: int, queue: str) -> None:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host, port=port)
    )
    print("Worker is connected", flush=True)
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=callback)
    print("Worker starts consuming", flush=True)
    channel.start_consuming()


if __name__ == "__main__":
    main()
