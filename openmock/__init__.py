# -*- coding: utf-8 -*-

from functools import wraps

from openmock.normalize_hosts import _normalize_hosts
from unittest.mock import patch

from openmock.fake_opensearch import FakeOpenSearch

OPEN_INSTANCES = {}


def _get_openmock(hosts=None, *args, **kwargs):
    host = _normalize_hosts(hosts)[0]
    open_key = '{0}:{1}'.format(
        host.get('host', 'localhost'), host.get('port', 9200)
    )

    if open_key in OPEN_INSTANCES:
        connection = OPEN_INSTANCES.get(open_key)
    else:
        connection = FakeOpenSearch()
        OPEN_INSTANCES[open_key] = connection
    return connection


def openmock(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        OPEN_INSTANCES.clear()
        with patch('opensearchpy.OpenSearch', _get_openmock):
            result = f(*args, **kwargs)
        return result
    return decorated