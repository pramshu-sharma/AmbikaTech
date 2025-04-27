from urllib.parse import urlparse


def is_url(url):
    result = urlparse(url)
    return all([result.scheme, result.netloc])


