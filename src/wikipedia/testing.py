import asyncio
from yarl import URL

from src.wikipedia.distance import wikipedia_distance
from src.wikipedia.url_parsing import wikipedia_url_parsing


async def parsing() -> None:
    print(await wikipedia_url_parsing(URL(
        "https://ru.wikipedia.org/wiki/"
        "%D0%9D%D0%B5%D0%BF%D1%80%D0%B5%"
        "D1%80%D1%8B%D0%B2%D0%BD%D0%BE%D0%"
        "B5_%D0%BE%D1%82%D0%BE%D0%B1%D1%80%"
        "D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D0%"
        "B5"
    )))


async def distance1() -> None:
    print(await wikipedia_distance(URL(
        "https://ru.wikipedia.org/wiki/"
        "%D0%9D%D0%B5%D0%BF%D1%80%D0%B5%"
        "D1%80%D1%8B%D0%B2%D0%BD%D0%BE%D0%"
        "B5_%D0%BE%D1%82%D0%BE%D0%B1%D1%80%"
        "D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D0%"
        "B5"
    ), URL(
        "https://ru.wikipedia.org/wiki/%D0%A4%D1%83%D0%BD%D0%BA%D1%86%D0%B8%D1"
        "%8F_(%D0%BC%D0%B0%D1%82%D0%B5%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B0)"
    )))


async def distance2() -> None:
    print(await wikipedia_distance(URL(
        "https://ru.wikipedia.org/wiki/Linux"
    ), URL(
        "https://ru.wikipedia.org/wiki/%D0%A1%D1%82%D0%BE%D0%BB%D0%BB%D0%"
        "BC%D0%B0%D0%BD,_%D0%A0%D0%B8%D1%87%D0%B0%D1%80%D0%B4_%D0%9C%"
        "D1%8D%D1%82%D1%82%D1%8C%D1%8E"
    )))


if __name__ == "__main__":
    asyncio.run(distance2())
