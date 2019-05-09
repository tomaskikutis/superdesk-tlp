# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import json
import re
from unittest import mock
import os

from superdesk.tests import TestCase
from superdesk.io.feeding_services import http_base_service
from apps.prepopulate.app_populate import AppPopulateCommand
import anp
from anp.io.feed_parsers.anp_news_api import ANPNewsApiFeedParser
from anp.io.feeding_services.anp_news_api import ANPNewsApiFeedingService

PROVIDER = {
    "update_schedule": {
        "minutes": 0,
        "seconds": 0
    },
    "idle_time": {
        "hours": 0,
        "minutes": 0
    },
    "content_expiry": 14398560,
    "name": "ANP",
    "source": "ANP",
    "feeding_service": "anp_news_api",
    "config": {
        "username": "fake@anp.nl",
        "password": "fakepswd",
        "source_titles": "AFN, AFP EN (Editorial)"
    },
    "feed_parser": "anp_news_api",
    "content_types": [
        "text"
    ],
    "allow_remove_ingested": False,
    "is_closed": False,
    "private": {}
}


class ANPNewsApiFeedingServiceTestCase(TestCase):

    def setUp(self):
        super().setUp()
        # load vocabularies
        with self.app.app_context():
            voc_file = os.path.join(
                os.path.abspath(os.path.dirname(os.path.dirname(anp.__file__))), 'data', 'vocabularies.json'
            )
            AppPopulateCommand().run(voc_file)
        # load fixtures
        self.fixtures = {}
        dirname = os.path.dirname(os.path.realpath(__file__))
        # sources
        sources = os.path.normpath(os.path.join(dirname, '../fixtures', 'anp_news_api-sources.json'))
        with open(sources, 'r') as f:
            self.fixtures['sources'] = json.load(f)
        # items
        for source_id in ('5af9a2e4-3825-45d6-8445-419b1cb365dc',
                          '3dc77946-38dc-4469-b0a9-c10519035824',
                          '5b8bc05d-2421-454d-b363-b043d503c6b7',
                          '03b7a184-f6f4-4879-85f6-b43f21acb940',
                          '4ad32715-3221-49b1-b93b-30b02c1c6eb6'):
            items = os.path.normpath(
                os.path.join(dirname, '../fixtures', 'anp_news_api-items-{}.json'.format(source_id))
            )
            with open(items, 'r') as f:
                self.fixtures.setdefault('items', {})[source_id] = json.load(f)
        # items details
        for item_id in ('ac3dc857e87ea0a0b98635b314941d12',
                        'bd34da5aa71ea490639e5601f98b238a',
                        'ac47563d3fe56f62972f0f7e55d323cd',
                        'c4b893fec041a87ee340b513e8b11860'):
            items = os.path.normpath(
                os.path.join(dirname, '../fixtures', 'anp_news_api-item-detail-{}.json'.format(item_id))
            )
            with open(items, 'r') as f:
                self.fixtures.setdefault('item-details', {})[item_id] = json.load(f)

    @mock.patch.object(http_base_service, 'requests')
    @mock.patch.object(ANPNewsApiFeedingService, 'get_feed_parser')
    def test_feeding_service(self, get_feed_parser, requests):

        def mock_get_side_effect(url, *args, **kwargs):
            response = mock.MagicMock()
            response.status_code = 200
            match_items = re.match(r'https://newsapi.anp.nl/services/sources/(.*)/items$', url)
            match_details = re.match(r'https://newsapi.anp.nl/services/sources/(.*)/items/(.*)$', url)

            if url == 'https://newsapi.anp.nl/services/sources':
                response.json.return_value = self.fixtures['sources']
            elif match_items:
                source_id = match_items.group(1)
                response.json.return_value = self.fixtures['items'][source_id]
            elif match_details:
                item_id = match_details.group(2)
                response.json.return_value = self.fixtures['item-details'][item_id]

            return response

        mock_get = requests.get
        mock_get.side_effect = mock_get_side_effect
        get_feed_parser.return_value = ANPNewsApiFeedParser()

        provider = PROVIDER.copy()
        service = ANPNewsApiFeedingService()
        service.provider = provider
        update = {}
        items = service._update(provider, update)[0]

        self.assertEqual(len(items), 4)
        self.assertDictEqual(
            update,
            {
                'private': {
                    'sources': {
                        '5af9a2e4-3825-45d6-8445-419b1cb365dc': {
                            'title': 'AFN',
                            'last_item_id': 'ac3dc857e87ea0a0b98635b314941d12'
                        },
                        '03b7a184-f6f4-4879-85f6-b43f21acb940': {
                            'title': 'AFP EN (Editorial)',
                            'last_item_id': 'ac47563d3fe56f62972f0f7e55d323cd'
                        }
                    }
                }
            }
        )
