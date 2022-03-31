import asyncio
import logging
import os
import typing as tp

import grpc
import click
from yarl import URL

import src.service.service_pb2 as service_pb2
import src.service.service_pb2_grpc as service_pb2_grpc
from src.wikipedia import is_wikipedia_url, wikipedia_distance


class WikipediaDistance(service_pb2_grpc.WikipediaDistanceServicer):
    async def Distance(
        self,
        request: service_pb2.DistanceRequest,
        context: grpc.ServicerContext
    ) -> tp.Optional[service_pb2.DistanceReply]:
        source_url: URL = URL(request.source_url)
        target_url: URL = URL(request.target_url)

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

        answer = await wikipedia_distance(source_url, target_url)
        if answer is None:
            await context.abort(
                grpc.StatusCode.NOT_FOUND,
                "Path is not found"
            )
            return

        reply = service_pb2.DistanceReply()
        reply.path.extend([str(e) for e in answer])
        return reply


async def run(host: str, port: int) -> None:
    server = grpc.aio.server()
    service_pb2_grpc.add_WikipediaDistanceServicer_to_server(
        WikipediaDistance(), server
    )
    server.add_insecure_port(f"{host}:{port}")
    await server.start()
    print(f"Server is started on {host}:{port}", flush=True)
    await server.wait_for_termination()


@click.command()
@click.option("--host", default="0.0.0.0", type=str)
@click.option("--port", default=50051, type=int)
def main(host: str, port: int) -> None:
    logging.basicConfig(level=logging.INFO)
    os.environ["GRPC_FORK_SUPPORT_ENABLED"] = "0"
    asyncio.run(run(host, port))


if __name__ == "__main__":
    main()
