import click
import pika


def callback(channel, method, properties, body) -> None:  # type ignore
    m = body.decode()
    caption: str = get_image_caption(m)
    assert "path" in properties.headers
    with open(properties.headers["path"], "w") as f:
        f.write(caption)
    channel.basic_ack(delivery_tag=method.delivery_tag)


@click.command()
@click.option(
    "--host",
    default="rabbitmq",
    type=str
)
@click.option(
    "--queue",
    default="rabbitmqqueue",
    type=str
)
def main(host: str, queue: str) -> None:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host)
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=callback)
    channel.start_consuming()


if __name__ == "__main__":
    main()
