import datetime
import unittest
from unittest import mock
from requests import Response

from superdesk.metadata.item import CONTENT_STATE, ITEM_STATE
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
        provider = TalpaVideoSearchProvider({'config': {'url': 'https://graph.kijk.nl/graphql'}})
        self.assertEqual('Talpa', provider.label)

    def test_build_query(self):
        provider = TalpaVideoSearchProvider({'config': {'url': 'https://graph.kijk.nl/graphql'}})

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
        provider = TalpaVideoSearchProvider({'config': {'url': 'https://graph.kijk.nl/graphql'}})
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
        item_first = cursor[0]
        item_last = cursor[-1]

        self.assertFalse(item_first['_fetchable'])
        self.assertEqual(item_first['_id'], 'I8Cug8DR5pT')
        self.assertEqual(item_first['guid'], 'I8Cug8DR5pT')
        self.assertEqual(item_first['type'], 'video')
        self.assertEqual(item_first[ITEM_STATE], CONTENT_STATE.PUBLISHED)
        self.assertEqual(
            item_first['description_text'], 'In Ranking the Cars gaat Tess Milne langs bij de trotse voorbij.'
        )
        self.assertEqual(item_first['extra']['duration'], 0)
        self.assertIsNone(item_first['source'])
        self.assertEqual(item_first['firstcreated'], datetime.datetime(2019, 9, 24, 15, 35, 51))
        self.assertEqual(item_first['versioncreated'], datetime.datetime(2019, 11, 11, 18, 41, 52))
        self.assertEqual(item_first['headline'], 'Episode: Ranking the Cars - S:NaN - E:6 - 2015-02-23')
        self.assertEqual(item_first['pubstatus'], 'usable')
        self.assertEqual(item_first['renditions']['original'], {})
        self.assertEqual(item_first['renditions']['thumbnail'], None)
        self.assertEqual(item_first['renditions']['viewImage'], None)

        self.assertFalse(item_last['_fetchable'])
        self.assertEqual(item_last['_id'], 'ti2FVyP555I')
        self.assertEqual(item_last['guid'], 'ti2FVyP555I')
        self.assertEqual(item_last['type'], 'video')
        self.assertEqual(item_first[ITEM_STATE], CONTENT_STATE.PUBLISHED)
        self.assertEqual(
            item_last['description_text'],
            'In Ranking the Cars gaat Tess Milne langs bij de trotse '
            "eigenaren van opvallende auto's om te achterhalen wat "
            'het bijzondere verhaal achter de auto is. Van stoere '
            'racewagen tot klassieke oldtimer, alles komt voorbij '
            'onder het toeziend oog van Tess.'
        )
        self.assertEqual(item_last['extra']['duration'], 1310)
        self.assertIsNone(item_last['source'])
        self.assertEqual(item_last['firstcreated'], datetime.datetime(2019, 9, 19, 9, 25, 4))
        self.assertEqual(item_last['versioncreated'], datetime.datetime(2019, 11, 20, 12, 55, 57))
        self.assertEqual(item_last['headline'], 'Episode: Ranking the Cars - S:2 - E:16 - 2013-12-30')
        self.assertEqual(item_last['pubstatus'], 'usable')
        self.assertEqual(
            item_last['renditions']['original'],
            {
                'href': 'https://vod-kijk2-prod.talpatvcdn.nl/ti2FVyP555I/92bf99ad-097e-466d-84b0-913cef51e6d8/ti2'
                        'FVyP555I-index.ism/ti2FVyP555I.m3u8',
                'mimetype': 'application/x-mpegurl'
            }
        )
        self.assertEqual(
            item_last['renditions']['thumbnail'],
            {
                'href': 'https://redactioneel.s3-eu-west-1.amazonaws.com/images/redactioneel/336614-LS.jpg',
                'mimetype': 'image/jpeg',
            }
        )
        self.assertEqual(
            item_last['renditions']['viewImage'],
            {
                'href': 'https://redactioneel.s3-eu-west-1.amazonaws.com/images/redactioneel/336614-LS.jpg',
                'mimetype': 'image/jpeg',
            }
        )
