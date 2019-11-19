from datetime import datetime
import requests

import superdesk
from superdesk.utils import ListCursor


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
    url = 'https://graph.kijk.nl/graphql'

    query_variables_types = {
        'limit': 'Int',
        'skip': 'Int',
        'searchParam': 'String',
        'sort': 'ProgramSortKey',
    }

    def __init__(self, provider):
        super().__init__(provider)
        self._session = requests.Session()

    def _get_query_definition(self, query_variables):
        definition = ''

        for key in query_variables.keys():
            if definition:
                definition += ', ${}: {}'.format(key, self.query_variables_types[key])
            else:
                definition = '${}: {}'.format(key, self.query_variables_types[key])

        return definition

    def _get_query_arguments(self, query_variables):
        arguments = ''

        for key in query_variables.keys():
            if arguments:
                arguments += ', {}: ${}'.format(key, key)
            else:
                arguments = '{}: ${}'.format(key, key)

        return arguments

    def _build_query(self, **kwargs):
        # ensure that all graphql variables types are defined
        assert set(self.query_variables_types.keys()) >= set(kwargs.keys())

        query = \
            r'''
            query TalpaVideoSearch ({definition}) {{
              programs({arguments}) {{
                totalResults
                items {{
                  guid
                  title
                  description
                  added
                  updated
                  sourceProgram
                  imageMedia {{
                    url
                  }}
                  media {{
                    mediaContent {{
                      sourceUrl
                    }}
                  }}
                }}
              }}
            }}
            '''.format(
                definition=self._get_query_definition(kwargs),
                arguments=self._get_query_arguments(kwargs)
            ).strip()

        return {
            'operationName': 'TalpaVideoSearch',
            'query': query,
            'variables': kwargs
        }

    def _format_list_item(self, item):
        # video_media_url = item['media'][0]['url'] if item['media'] else None
        video_media_url = 'http://cdnapi.kaltura.com/p/1878761/sp/187876100/playManifest/entryId/1_usagz19w/flavorIds/1_5spqkazq,1_nslowvhp,1_boih5aji,1_qahc37ag/format/applehttp/protocol/http/a.m3u8'
        image_media_url = item['imageMedia'][0]['url'] if item['imageMedia'] else None

        return {
            'type': 'video',
            'pubstatus': 'usable',
            '_id': item['guid'],
            'guid': item['guid'],
            'headline': item['title'],
            'source': item['sourceProgram'],
            'description_text': item['description'],
            'firstcreated': jstimestamp_to_utcdatetime(item['added']),
            'versioncreated': jstimestamp_to_utcdatetime(item['updated']),
            'renditions': {
                'original': {
                    'href': 'http://cdnapi.kaltura.com/p/1878761/sp/187876100/playManifest/entryId/1_usagz19w/flavorIds/1_5spqkazq,1_nslowvhp,1_boih5aji,1_qahc37ag/format/applehttp/protocol/http/a.m3u8',
                    # 'mimetype': "application/x-mpegurl"
                    # 'href': 'http://localhost:5000/api/upload-raw/5dd4296d58f6623612e0aacb.mp4',
                    # 'mimetype': "video/mp4"
                },
                'thumbnail': {
                    'href': image_media_url,
                },
                'viewImage': {
                    'href': image_media_url,
                },
                'baseImage': {
                    'href': image_media_url,
                },
            }
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

        # print(self._build_query(**params)['query'])

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

