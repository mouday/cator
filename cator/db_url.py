# -*- coding: utf-8 -*-
from urllib.parse import urlparse, parse_qsl


# code reference : playhouse.db_url.parse
def parse_query(query):
    qs_args = parse_qsl(query, keep_blank_values=True)

    query_dict = {}

    for key, value in qs_args:
        if value.lower() == 'false':
            value = False
        elif value.lower() == 'true':
            value = True
        elif value.isdigit():
            value = int(value)
        elif '.' in value and all(p.isdigit() for p in value.split('.', 1)):
            try:
                value = float(value)
            except ValueError:
                pass
        elif value.lower() in ('null', 'none'):
            value = None

        query_dict[key] = value

    return query_dict


def parse_url_to_dict(db_url):
    parsed = urlparse(db_url)

    connect_kwargs = {
        'database': parsed.path[1:],
        'scheme': parsed.scheme
    }

    if parsed.username:
        connect_kwargs['username'] = parsed.username
    if parsed.password:
        connect_kwargs['password'] = parsed.password
    if parsed.hostname:
        connect_kwargs['host'] = parsed.hostname
    if parsed.port:
        connect_kwargs['port'] = parsed.port

    query_kwargs = parse_query(parsed.query)
    connect_kwargs.update(query_kwargs)
    return connect_kwargs
