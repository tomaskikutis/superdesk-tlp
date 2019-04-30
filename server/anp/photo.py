
import math
import requests
import superdesk

from flask import json, request
from datetime import datetime
from xmlrpc.client import ServerProxy
from superdesk.utils import ListCursor
from superdesk.utc import local_to_utc
from superdesk.logging import logger


TZ = 'Europe/Amsterdam'

THUMBNAIL = 1
PREVIEW = 2
TITLE = 4
DESCRIPTION = 8
KEYWORDS = 16

PICTURE_DATE = 2

ASC = 0
DESC = 1

TYPES = {
    0: 'picture',
    1: 'video',
    2: 'graphic',
    3: 'picture',
    4: 'graphic',
}


class PhotoListCursor(ListCursor):

    def __init__(self, docs, count):
        super().__init__(docs)
        self._count = count

    def count(self, **kwargs):
        return self._count


class PhotoSearchProvider(superdesk.SearchProvider):

    label = 'ANP'
    source = 'ANP'
    url = 'https://search.anpfoto.nl/'

    @property
    def proxy(self):
        if not hasattr(self, '_proxy'):
            self._proxy = ServerProxy(self.url)
        return self._proxy

    def find(self, query, params=None):
        pagesize = query.get('size', 25)
        try:
            sortorder = ASC if query['sort'][0]['versioncreated'] == 'asc' else DESC
        except KeyError:
            sortorder = DESC
        _params = {
            'api_key': self.provider.get('config', {}).get('password', ''),
            'page': math.ceil(query.get('from', 0) / pagesize) + 1,
            'pagesize': pagesize,
            'sortfield': 0,
            'sortorder': sortorder,
            'returnfields': THUMBNAIL | PREVIEW | TITLE | DESCRIPTION,
        }

        if params is None and request.args.get('params'):
            params = json.loads(request.args.get('params'))

        if params:
            if params.get('orientation'):
                _params['orientation'] = int(params['orientation'])
            if params.get('reference'):
                _params['reference'] = params['reference']
            if params.get('filename'):
                _params['filename'] = params['filename']
            if params.get('firstdate'):
                _params['firstdate'] = params['firstdate'].split('T')[0]
                _params['sortorder'] = ASC

        try:
            query_string = query['query']['filtered']['query']['query_string']['query']
            if query_string:
                _params['keywords'] = query_string
        except KeyError:
            pass

        data = self.proxy.search(_params)
        items = []
        for i in range(0, _params['pagesize']):
            item = self._parse_item(data.get(str(i + 1)))
            if item:
                items.append(item)
        return PhotoListCursor(items, data['totalresults'])

    def _parse_item(self, data):
        if not data:
            return
        try:
            firstcreated = self._parse_date(data['picturedate'])
        except OverflowError:
            firstcreated = self._parse_date(data['entrydate'])
        return {
            'guid': 'urn:anp:{}'.format(str(data['id'])),
            'type': TYPES[data['objecttype']],
            'source': data['reference2'] or self.source,
            'headline': data['title'],
            'description_text': data['description'],
            'firstcreated': firstcreated,
            'versioncreated': self._parse_date(data['entrydate']),
            'renditions': {
                'thumbnail': {'href': data['thumbnail_url']},
                'viewImage': {'href': data['preview_url']},
                'baseImage': {'href': data['preview_url']},
                'original': {'href': data['preview_url']},
            }
        }

    def _parse_date(self, string):
        local = datetime.strptime(string, '%Y%m%d %H:%M:%S')
        return local_to_utc(TZ, local)


def init_app(app):
    superdesk.register_search_provider('anp', provider_class=PhotoSearchProvider)
