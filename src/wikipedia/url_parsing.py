from urllib.parse import unquote

from aiohttp import web
from aiohttp.client import ClientSession
from bs4 import BeautifulSoup
from yarl import URL

from src.wikipedia.utils import is_wikipedia_url


URLs = list[URL]


async def wikipedia_url_parsing(url: URL) -> URLs:
    async with ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != web.HTTPOk.status_code:
                raise RuntimeError(f"Response status: {resp.status}")
            text = await resp.text()

    paragraph = BeautifulSoup(text, "html.parser")
    result: URLs = []
    s: set[URL] = set()
    for parsed_url in paragraph.find_all('a'):
        if "href" not in parsed_url.attrs:
            continue

        href = parsed_url["href"]

        if href.startswith("/wiki/"):
            full_url = URL(unquote(str(URL.build(
                scheme=url.scheme,
                host=url.host,
                port=url.port
            ) / href.lstrip("/"))))
            if full_url not in s:
                s.add(full_url)
                result.append(full_url)
            continue

        if is_wikipedia_url(u := URL(href)):
            if u in s:
                continue

            s.add(u)
            result.append(u)

    return result
