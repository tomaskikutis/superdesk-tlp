import datetime
import unittest
from unittest import mock
from requests import Response

from anp.search_providers import TalpaVideoSearchProvider


class PostResponse200(Response):

    def __init__(self):
        super().__init__()
        self.status_code = 200

    def json(self):
        return {
            'data': {
                'programs': {
                    'totalResults': 3,
                    'items': [
                        {
                            'guid': 'I8Cug8DR5pT',
                            'title': 'Episode: Ranking the Cars - S:NaN - E:6 - 2015-02-23',
                            'description': "In Ranking the Cars gaat Tess Milne langs bij de trotse voorbij.",
                            'added': 1569339351000,
                            'updated': 1573497712000,
                            'sourceProgram': None,
                            'duration': None,
                            'imageMedia': [],
                            'media': [
                                {
                                    'mediaContent': [
                                        {'sourceUrl': 'https://vod-kijk2-prod.talpatvcdn.nl/webvtt/561113E1.vtt'},
                                        {'sourceUrl': 'https://vod-kijk2-prod.talpatvcdn.nl/webvtt/561113E1OPE.vtt'}
                                    ]
                                }
                            ]
                        },
                        {
                            'guid': '2yw641fcTQr',
                            'title': 'Episode: Ranking the Cars - S:NaN - E:26 - 2015-03-25',
                            'description': "In Ranking the Cars gaat Tess Milne langs bij de trotse eigenaren van "
                                           "e auto's om te achterhalen wat het bijzondere verhaal achter de auto is.",
                            'added': 1569339339000,
                            'updated': 1573497757000,
                            'sourceProgram': None,
                            'duration': None,
                            'imageMedia': [],
                            'media': [
                                {
                                    'mediaContent': [
                                        {'sourceUrl': 'https://vod-kijk2-prod.talpatvcdn.nl/webvtt/564916E1.vtt'},
                                        {'sourceUrl': 'https://vod-kijk2-prod.talpatvcdn.nl/webvtt/564916E1OPE.vtt'}
                                    ]
                                }
                            ]
                        },
                        {
                            'guid': 'ti2FVyP555I',
                            'title': 'Episode: Ranking the Cars - S:2 - E:16 - 2013-12-30',
                            'description': "In Ranking the Cars gaat Tess Milne langs bij de trotse eigenaren van opval"
                                           "lende auto's om te achterhalen wat het bijzondere verhaal achter de auto is"
                                           ". Van stoere racewagen tot klassieke oldtimer, alles komt voorbij onder het"
                                           " toeziend oog van Tess.",
                            'added': 1568885104000,
                            'updated': 1574254557000,
                            'sourceProgram': None,
                            'duration': 1310,
                            'imageMedia': [
                                {
                                    'url': 'https://redactioneel.s3-eu-west-1.amazonaws.com/images/redactioneel/336614-'
                                           'LS.jpg'
                                }
                            ],
                            'media': [
                                {'mediaContent': [
                                    {'sourceUrl': 'https://vod-kijk2-prod.talpatvcdn.nl/ti2FVyP555I/92bf99ad-097e-466d-'
                                                  '84b0-913cef51e6d8/ti2FVyP555I-index.ism/ti2FVyP555I.mpd'},
                                    {'sourceUrl': 'https://vod-kijk2-prod.talpatvcdn.nl/ti2FVyP555I/92bf99ad-097e-466d-'
                                                  '84b0-913cef51e6d8/ti2FVyP555I-index.ism/ti2FVyP555I.ismc'},
                                    {'sourceUrl': 'https://vod-kijk2-prod.talpatvcdn.nl/ti2FVyP555I/92bf99ad-097e-466d-'
                                                  '84b0-913cef51e6d8/ti2FVyP555I-index.ism/ti2FVyP555I.m3u8'},
                                    {'sourceUrl': 'https://vod-kijk2-prod.talpatvcdn.nl/webvtt/501107E1.vtt'},
                                    {'sourceUrl': 'https://vod-kijk2-prod.talpatvcdn.nl/webvtt/501107E1OPE.vtt'}
                                ]
                                }
                            ]
                        }
                    ]
                }
            }
        }


class TalpaVideoTestCase(unittest.TestCase):

    def test_instance(self):
        provider = TalpaVideoSearchProvider({})
        self.assertEqual('Talpa', provider.label)

    def test_build_query(self):
        provider = TalpaVideoSearchProvider({})

        params = {
            'searchParam': 'cars films'
        }
        query = provider._build_query(**params)
        self.assertEqual(query['operationName'], 'TalpaVideoSearch')
        self.assertEqual(query['variables'], {'searchParam': 'cars films'})
        self.assertEqual(
            query['query'],
            'query TalpaVideoSearch ($searchParam: String) {\n'
            '  programs(searchParam: $searchParam) {\n'
            '    totalResults\n'
            '    items {\n'
            '      guid\n'
            '      title\n'
            '      description\n'
            '      added\n'
            '      updated\n'
            '      sourceProgram\n'
            '      duration\n'
            '      imageMedia {\n'
            '        url\n'
            '      }\n'
            '      media {\n'
            '        mediaContent {\n'
            '          sourceUrl\n'
            '        }\n'
            '      }\n'
            '    }\n'
            '  }\n'
            '}'
        )

        params = {
            'skip': 0,
            'limit': 25,
            'sort': 'ADDED'
        }
        query = provider._build_query(**params)
        self.assertEqual(query['operationName'], 'TalpaVideoSearch')
        self.assertEqual(query['variables']['skip'], 0)
        self.assertEqual(query['variables']['limit'], 25)
        self.assertEqual(query['variables']['sort'], 'ADDED')
        self.assertEqual(
            query['query'],
            'query TalpaVideoSearch ($limit: Int, $skip: Int, $sort: ProgramSortKey) {\n'
            '  programs(limit: $limit, skip: $skip, sort: $sort) {\n'
            '    totalResults\n'
            '    items {\n'
            '      guid\n'
            '      title\n'
            '      description\n'
            '      added\n'
            '      updated\n'
            '      sourceProgram\n'
            '      duration\n'
            '      imageMedia {\n'
            '        url\n'
            '      }\n'
            '      media {\n'
            '        mediaContent {\n'
            '          sourceUrl\n'
            '        }\n'
            '      }\n'
            '    }\n'
            '  }\n'
            '}'
        )

    def test_find(self):
        provider = TalpaVideoSearchProvider({})
        # mock self._session
        provider._session = mock.MagicMock()
        provider._session.post.return_value = PostResponse200()
        query = {
            'skip': 0,
            'limit': 25,
            'searchParam': 'cars films'
        }
        cursor = provider.find(query, {})
        self.assertEqual(3, cursor.count())
        self.assertEqual(
            {'_fetchable': False,
             '_id': 'I8Cug8DR5pT',
             'description_text': 'In Ranking the Cars gaat Tess Milne langs bij de trotse '
                                 'voorbij.',
             'duration': None,
             'firstcreated': datetime.datetime(2019, 9, 24, 15, 35, 51),
             'guid': 'I8Cug8DR5pT',
             'headline': 'Episode: Ranking the Cars - S:NaN - E:6 - 2015-02-23',
             'pubstatus': 'usable',
             'renditions': {'baseImage': {'href': None},
                            'original': {},
                            'thumbnail': {'href': None},
                            'viewImage': {'href': None}},
             'source': None,
             'type': 'video',
             'versioncreated': datetime.datetime(2019, 11, 11, 18, 41, 52)},
            cursor[0]
        )
        self.assertEqual(
            {'_fetchable': False,
             '_id': 'ti2FVyP555I',
             'description_text': 'In Ranking the Cars gaat Tess Milne langs bij de trotse '
                                 "eigenaren van opvallende auto's om te achterhalen wat "
                                 'het bijzondere verhaal achter de auto is. Van stoere '
                                 'racewagen tot klassieke oldtimer, alles komt voorbij '
                                 'onder het toeziend oog van Tess.',
             'duration': 1310,
             'firstcreated': datetime.datetime(2019, 9, 19, 9, 25, 4),
             'guid': 'ti2FVyP555I',
             'headline': 'Episode: Ranking the Cars - S:2 - E:16 - 2013-12-30',
             'pubstatus': 'usable',
             'renditions': {
                 'baseImage': {
                     'href': 'https://redactioneel.s3-eu-west-1.amazonaws.com/images/redactioneel/336614-LS.jpg'
                 },
                 'original': {
                     'href': 'https://vod-kijk2-prod.talpatvcdn.nl/ti2FVyP555I/92bf99ad-097e-466d-84b0-913cef51e6d8/ti2'
                             'FVyP555I-index.ism/ti2FVyP555I.m3u8',
                     'mimetype': 'application/x-mpegurl'
                 },
                 'thumbnail': {
                     'href': 'https://redactioneel.s3-eu-west-1.amazonaws.com/images/redactioneel/336614-LS.jpg'
                 },
                 'viewImage': {
                     'href': 'https://redactioneel.s3-eu-west-1.amazonaws.com/images/redactioneel/336614-LS.jpg'
                 }
             },
             'source': None,
             'type': 'video',
             'versioncreated': datetime.datetime(2019, 11, 20, 12, 55, 57)},
            cursor[-1]
        )
