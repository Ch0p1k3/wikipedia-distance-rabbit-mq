import asyncio
import logging
import os
import typing as tp
import uuid
from dataclasses import dataclass

import click
import grpc
import pika
from yarl import URL

import src.service.service_pb2 as service_pb2
import src.service.service_pb2_grpc as service_pb2_grpc
from src.wikipedia import is_wikipedia_url


@dataclass
class WikipediaDistance(service_pb2_grpc.WikipediaDistanceServicer):
    _rabbitmq_host: str
    _rabbitmq_port: int
    _rabbitmq_queue: str

    def __post_init__(self) -> None:
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self._rabbitmq_host, port=self._rabbitmq_port
            )
        )
        self._channel = self._connection.channel()
        self._channel.confirm_delivery()
        self._channel.queue_declare(queue=self._rabbitmq_queue, durable=True)
        result = self._channel.queue_declare(queue='', exclusive=True)
        self._callback_queue = result.method.queue
        self._channel.basic_consume(
            queue=self._callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def on_response(self, ch, method, props, body):  # type: ignore
        if self._corr_id == props.correlation_id:
            self._response = body.decode()

    async def Distance(
        self,
        request: service_pb2.DistanceRequest,
        context: grpc.ServicerContext
    ) -> tp.Optional[service_pb2.DistanceReply]:
        source_url = URL(request.source_url)
        target_url = URL(request.target_url)

        print(
            f"Distance request:"
            f"source_url=[{str(source_url)}], "
            f"target_url=[{str(target_url)}]",
            flush=True
        )

        if not source_url.is_absolute() or not target_url.is_absolute():
            await context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Source and target url should be absolute"
            )
            return

        if not is_wikipedia_url(source_url) or\
           not is_wikipedia_url(target_url):
            await context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Source and target url should be from wikipedia"
            )
            return

        self._response = None
        self._corr_id = str(uuid.uuid4())
        self._channel.basic_publish(
            exchange='',
            routing_key=self._rabbitmq_queue,
            properties=pika.BasicProperties(
                reply_to=self._callback_queue,
                correlation_id=self._corr_id,
            ),
            body=f"{source_url} {target_url}"
        )
        while self._response is None:
            await asyncio.sleep(0)
            self._connection.process_data_events()

        if len(self._response) == 0:
            await context.abort(
                grpc.StatusCode.NOT_FOUND,
                "Path is not found"
            )
            return

        reply = service_pb2.DistanceReply()
        reply.path.extend(self._response.split("\n"))
        return reply


async def run(
    host: str, port: int,
    rabbitmq_host: str, rabbitmq_port: int, rabbitmq_queue: str
) -> None:
    server = grpc.aio.server()
    service_pb2_grpc.add_WikipediaDistanceServicer_to_server(
        WikipediaDistance(rabbitmq_host, rabbitmq_port, rabbitmq_queue), server
    )
    server.add_insecure_port(f"{host}:{port}")
    await server.start()
    print(f"Server is started on [{host}]:[{port}]", flush=True)
    await server.wait_for_termination()


@click.command()
@click.option("--host", default="0.0.0.0", type=str)
@click.option("--port", default=50051, type=int)
@click.option("--rabbitmq_host", default="localhost", type=str)
@click.option("--rabbitmq_port", default=5672, type=int)
@click.option("--rabbitmq_queue", default="rabbitmqqueue", type=str)
def main(
    host: str, port: int,
    rabbitmq_host: str, rabbitmq_port: int, rabbitmq_queue: str
) -> None:
    logging.basicConfig(level=logging.INFO)
    os.environ["GRPC_FORK_SUPPORT_ENABLED"] = "0"
    asyncio.run(run(host, port, rabbitmq_host, rabbitmq_port, rabbitmq_queue))


if __name__ == "__main__":
    main()
