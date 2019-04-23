# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013 - 2018 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license


import os
import json
import datetime
from superdesk.tests import TestCase
from anp.io.feed_parsers.anp_news_api import ANPNewsApiFeedParser


class ANPNewsApiFeedParserTestCase(TestCase):
    filename = 'anp_news_api-item-detail-38bdbbbdae1320f77049b5a32538e09c.json'

    def setUp(self):
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture_path = os.path.normpath(os.path.join(dirname, '../fixtures', self.filename))
        provider = {'name': 'test'}
        with open(fixture_path, 'r') as f:
            self.article = json.loads(f.read())['data']
            parser = ANPNewsApiFeedParser()
            self.item = parser.parse(self.article, provider)

    def test_can_parse(self):
        self.assertTrue(ANPNewsApiFeedParser().can_parse(self.article))

    def test_content(self):
        self.assertEqual(
            self.item['type'],
            'text'
        )
        self.assertEqual(
            self.item['guid'],
            '38bdbbbdae1320f77049b5a32538e09c'
        )
        self.assertEqual(
            self.item['firstcreated'],
            datetime.datetime(2019, 5, 2, 12, 4, 56)
        )
        self.assertEqual(
            self.item['versioncreated'],
            datetime.datetime(2019, 5, 2, 12, 4, 56)
        )
        self.assertEqual(
            self.item['headline'],
            'Zanger Dotan maakt comeback na trollenaffaire'
        )
        self.assertEqual(
            self.item['body_html'],
            "<p>AMSTERDAM (ANP) - Zanger Dotan wil een comeback maken en komt nog dit jaar met nieuwe "
            "nummers. De zanger kwam vorig jaar onder vuur te liggen omdat hij een aantal nepaccounts "
            "op social media had om zijn muziek te promoten. De Volkskrant onthulde de "
            "'trollenaffaire'. Platenmaatschappij 8Ball Music heeft het bericht over de comeback van "
            "Dotan, waarover Het Parool schrijft, bevestigd.</p><p>Het nieuwe werk zou nog dit jaar "
            "uit moeten komen. De laatste plaat van Dotan dateert uit 2014. Hij werkt momenteel aan "
            "de nieuwe nummers. Daarmee zou de zanger zijn imago willen oppoetsen.</p><p>De zanger "
            "had ook diverse verhalen over ontmoetingen met fans verzonnen. De Volkskrant wist te "
            "melden dat er vanaf 2011 minstens 140 nepprofielen zijn aangemaakt om op Twitter, "
            "Facebook en Instagram het imago van de zanger op te poetsen. Dotan ontkende eerst er "
            "iets mee te maken te hebben, maar gaf later toe dat het klopte.</p><p>Meer toelichting "
            "op de comeback wil 8Ball Music niet geven. De manager van Dotan was donderdag niet "
            "bereikbaar voor commentaar.</p>"
        )
        self.assertEqual(
            self.item['ednote'],
            ''
        )
        self.assertEqual(
            self.item['copyrightholder'],
            'ANP 101'
        )
        self.assertEqual(
            self.item['urgency'],
            3
        )
        self.assertEqual(
            self.item['priority'],
            3
        )
        self.assertEqual(
            self.item['authors'],
            [{'name': 'ANP Producties', 'role': 'writer'}]
        )
