from datetime import datetime
import requests

import superdesk
from superdesk.utils import ListCursor
from superdesk.metadata.item import CONTENT_STATE, ITEM_STATE


def jstimestamp_to_utcdatetime(jstimestamp):
    timestamp = jstimestamp / 1000
    return datetime.utcfromtimestamp(timestamp)


class TalpaVideoListCursor(ListCursor):

    def __init__(self, docs, count):
        super().__init__(docs)
        self._count = count

    def count(self, **kwargs):
        return self._count


class TalpaVideoSearchProvider(superdesk.SearchProvider):
    """
    Talpa video search provider.

    It uses graphQL API to retrieve data.
    Kijk apollo playground: https://graph.kijk.nl/graphql
    """

    label = 'Talpa'
    source = 'Talpa'

    query_variables_types = {
        'limit': 'Int',
        'skip': 'Int',
        'searchParam': 'String',
        'sort': 'ProgramSortKey',
    }

    def __init__(self, provider):
        super().__init__(provider)
        self.url = provider.get('url')
        self._session = requests.Session()

    def _get_query_definition(self, query_variables):
        definition = ''

        for key in sorted(query_variables):
            if definition:
                definition += ', ${}: {}'.format(key, self.query_variables_types[key])
            else:
                definition = '${}: {}'.format(key, self.query_variables_types[key])

        return definition

    def _get_query_arguments(self, query_variables):
        arguments = ''

        for key in sorted(query_variables):
            if arguments:
                arguments += ', {}: ${}'.format(key, key)
            else:
                arguments = '{}: ${}'.format(key, key)

        return arguments

    def _build_query(self, **kwargs):
        # ensure that all graphql variables types are defined
        assert set(self.query_variables_types.keys()) >= set(kwargs.keys())

        query = ('query TalpaVideoSearch ({definition}) {{\n'
                 '  programs({arguments}) {{\n'
                 '    totalResults\n'
                 '    items {{\n'
                 '      guid\n'
                 '      title\n'
                 '      description\n'
                 '      added\n'
                 '      updated\n'
                 '      sourceProgram\n'
                 '      duration\n'
                 '      imageMedia {{\n'
                 '        url\n'
                 '      }}\n'
                 '      media {{\n'
                 '        mediaContent {{\n'
                 '          sourceUrl\n'
                 '        }}\n'
                 '      }}\n'
                 '    }}\n'
                 '  }}\n'
                 '}}')
        query = query.format(
            definition=self._get_query_definition(kwargs),
            arguments=self._get_query_arguments(kwargs)
        ).strip()

        return {
            'operationName': 'TalpaVideoSearch',
            'query': query,
            'variables': kwargs
        }

    def _format_list_item(self, item):
        try:
            image_media_url = {'href': item['imageMedia'][0]['url']}
        except (IndexError, KeyError):
            image_media_url = {}

        try:
            hls_video = {
                'href': [
                    mc['sourceUrl']
                    for mc in item['media'][0]['mediaContent']
                    if mc['sourceUrl'].rsplit('.', 1)[-1] == 'm3u8'
                ][0],
                'mimetype': "application/x-mpegurl"
            }
        except (IndexError, KeyError):
            hls_video = {}

        return {
            'type': 'video',
            'pubstatus': 'usable',
            '_id': item['guid'],
            ITEM_STATE: CONTENT_STATE.PUBLISHED,
            'guid': item['guid'],
            'headline': item['title'],
            'source': item['sourceProgram'],
            'description_text': item['description'],
            'extra': {
                'duration': item['duration'],
            },
            'firstcreated': jstimestamp_to_utcdatetime(item['added']),
            'versioncreated': jstimestamp_to_utcdatetime(item['updated']),
            'renditions': {
                'original': hls_video,
                'viewImage': image_media_url, # used as poster
                'baseImage': image_media_url,
                'thumbnail': image_media_url,
            },
            # this flag specifies if search provider result's item should be fetched or just related
            '_fetchable': False
        }

    def find(self, query, params=None):
        # pagination
        params = {
            'skip': query.get('from', 0),
            'limit': query.get('size', 25),
            'sort': 'ADDED'
        }
        # full text search
        try:
            params['searchParam'] = query['query']['filtered']['query']['query_string']['query']
            if not params['searchParam'].strip():
                del params['searchParam']
        except KeyError:
            pass

        resp = self._session.post(
            url=self.url,
            json=self._build_query(**params)
        )
        resp.raise_for_status()
        programs = resp.json()['data']['programs']

        return TalpaVideoListCursor(
            tuple(self._format_list_item(item) for item in programs['items']),
            programs['totalResults']
        )
