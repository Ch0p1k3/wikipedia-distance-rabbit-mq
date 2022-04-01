import typing as tp
from collections import deque

from yarl import URL

from src.wikipedia.url_parsing import wikipedia_url_parsing
from src.wikipedia.utils import is_wikipedia_url


async def wikipedia_distance(
    source_url: URL,
    target_url: URL,
    bfs_limit=10000,
) -> tp.Optional[list[URL]]:
    if not is_wikipedia_url(source_url) or not is_wikipedia_url(target_url):
        raise RuntimeError("Source or target url is not wikipedia url")

    if not source_url.is_absolute() or not target_url.is_absolute():
        raise RuntimeError("Source and target url should be absolute")

    queue: deque[URL] = deque([])
    parent: dict[str, tp.Optional[URL]] = {}
    queue.append(source_url)
    parent[source_url.path] = None

    i = 0
    while len(queue) != 0:
        url = queue.popleft()
        if url.path == target_url.path:
            result: list[URL] = []
            result.append(u := target_url)
            while (u := parent[u.path]) is not None:
                result.append(u)
            return result[::-1]

        try:
            neighbours = await wikipedia_url_parsing(url)
        except Exception:
            continue

        for neighbour in neighbours:
            if neighbour.path not in parent:
                parent[neighbour.path] = url
                queue.append(neighbour)
                if neighbour.path == target_url.path:
                    result: list[URL] = []
                    result.append(u := target_url)
                    while (u := parent[u.path]) is not None:
                        result.append(u)
                    return result[::-1]

        i += 1
        if i >= bfs_limit:
            return None

    return None
