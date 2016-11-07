from urllib.parse import urlparse, urljoin


def is_absolute_url(string):
    parse_result = urlparse(string)
    return bool(parse_result.netloc)


def get_link_url(link, base_url=None):
    link_href = link.css('::attr(href)')[0].extract()

    if is_absolute_url(link_href):
        return link_href

    if base_url is None:
        raise ValueError('Link contains relative url and base url is not specified')

    return urljoin(base_url, link_href)



