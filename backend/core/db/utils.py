from sqlalchemy.engine.url import URL, make_url


def make_url_safe(raw_url: str | URL) -> URL:
    """
    Wrapper for SQLAlchemy's make_url(), which tends to raise too detailed of
    errors, which inevitably find their way into server logs. ArgumentErrors
    tend to contain usernames and passwords, which makes them non-log-friendly
    :param raw_url:
    :return:
    """

    if isinstance(raw_url, str):
        url = raw_url.strip()
        try:
            return make_url(url)
        except Exception as ex:
            raise ex

    else:
        return raw_url
