from yarl import URL


def is_wikipedia_url(url: URL) -> bool:
    return "wikipedia.org" in str(url)
