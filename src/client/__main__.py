import asyncio
import logging
import os
from dataclasses import dataclass

import click
import grpc
from simple_term_menu import TerminalMenu
from yarl import URL

from src.service.service_pb2 import DistanceRequest
from src.service.service_pb2_grpc import WikipediaDistanceStub
from src.wikipedia.utils import is_wikipedia_url


@dataclass
class Client:
    _host: str
    _port: int

    def __post_init__(self) -> None:
        self._channel = grpc.aio.insecure_channel(f"{self._host}:{self._port}")
        self._stub = WikipediaDistanceStub(self._channel)

    async def wikipedia_distance(
        self,
        source_url: str,
        target_url: str
    ) -> list[str]:
        reply = await self._stub.Distance(
            DistanceRequest(
                source_url=source_url,
                target_url=target_url
            )
        )

        return reply.path

    async def close(self) -> None:
        await self._channel.close()


async def run(host: str, port: int) -> None:
    client = Client(host, port)
    while True:
        terminal_menu = TerminalMenu(
            ["[d] Distance", "[e] Exit"],
            title="Wikipedia distance"
        )
        answer = int(terminal_menu.show())
        if answer == 1:
            await client.close()
            return

        while True:
            source_url = input("Type source URL:\n")
            u = URL(source_url)

            if not u.is_absolute():
                print("URL should be absolute", flush=True)
                continue

            if not is_wikipedia_url(u):
                print("URL should be from wikipedia", flush=True)
                continue

            break

        while True:
            target_url = input("Type target URL:\n")
            u = URL(target_url)

            if not u.is_absolute():
                print("URL should be absolute", flush=True)
                continue

            if not is_wikipedia_url(u):
                print("URL should be from wikipedia", flush=True)
                continue

            break

        try:
            reply = await client.wikipedia_distance(source_url, target_url)
        except Exception as e:
            print("ERROR:", flush=True)
            print(e, flush=True)
            continue

        print(f"Path length: {len(reply)}", flush=True)
        print("Path:", flush=True)
        print("- ", end='')
        print(*reply, sep="\n- ")


@click.command()
@click.option("--host", default="0.0.0.0", type=str)
@click.option("--port", default=50051, type=int)
def main(host: str, port: int) -> None:
    logging.basicConfig(level=logging.INFO)
    os.environ["GRPC_FORK_SUPPORT_ENABLED"] = "0"
    asyncio.run(run(host, port))


if __name__ == "__main__":
    main()
