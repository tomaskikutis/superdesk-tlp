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
import logging
import datetime

from eve.utils import ParsedRequest
import superdesk
from superdesk.io.registry import register_feed_parser
from superdesk.io.feed_parsers import FeedParser
from superdesk.media.renditions import update_renditions
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE, GUID_FIELD

logger = logging.getLogger(__name__)


class ANPNewsApiFeedParser(FeedParser):
    """
    Feed Parser for ANP News API json
    """

    NAME = 'anp_news_api'
    label = 'ANP News API Feed Parser'

    def __init__(self):
        super().__init__()
        self._vocabularies = None

    def _prefetch_vocabularies(self):
        """
        Prefetch items from vocabularies.
        """

        # this method is called from `parse`, but it must be executed only once
        if self._vocabularies is not None:
            return

        self._vocabularies = {}
        req = ParsedRequest()
        req.projection = json.dumps({'items': 1})
        # prefetch vocabularies -> anp_genres
        self._vocabularies['anp_genres'] = superdesk.get_resource_service(
            'vocabularies'
        ).find_one(
            req=req, _id='anp_genres'
        ).get('items', [])
        # use qcode as a key to speed up work with it in the future methods
        self._vocabularies['anp_genres'] = {s['qcode']: s for s in self._vocabularies['anp_genres']}

    def can_parse(self, article):
        # this parser works only with "anp_news_api" feeding service
        return True

    def _add_featuremedia(self, provider, item, href):
        associations = item.setdefault('associations', {})
        association = {
            ITEM_TYPE: CONTENT_TYPE.PICTURE,
            GUID_FIELD: href.rsplit('/', 1)[-1],
            'ingest_provider': provider['feeding_service'],
            'headline': item['headline'],
            'description_text': item['headline'],
            'copyrightnotice': item['copyrightholder']
        }

        update_renditions(
            item=association,
            href=href,
            old_item=None,
            request_kwargs={
                'auth': (
                    provider['config'].get('username', '').strip(),
                    provider['config'].get('password', '').strip()
                )
            }
        )
        associations['featuremedia'] = association

    def parse(self, article, provider=None):
        """
        Parse ANP News API artice

        :param article: anp news item json
        :type article: dict
        :param provider: Ingest Provider Details, defaults to None
        :type provider: dict having properties defined in
                        :py:class: `superdesk.io.ingest_provider_model.IngestProviderResource`
        :return:
        """

        self._prefetch_vocabularies()

        item = {}
        item[ITEM_TYPE] = CONTENT_TYPE.TEXT
        item[GUID_FIELD] = article['id']
        item['firstcreated'] = self._parse_date(article['firstIssueDate'])
        item['versioncreated'] = self._parse_date(article['pubDate'])
        item['headline'] = article.get('title', '')
        item['body_html'] = article.get('bodyText', '')
        item['ednote'] = article.get('editorialNote', '')
        item['copyrightholder'] = article.get('sourceTitle', '')
        item['urgency'] = int(article.get('urgency', 0))
        item['priority'] = item['urgency']
        item['byline'] = ', '.join(article.get('authors', []))

        for category_qcode in [
            c for c in article.get('categories', []) if c in self._vocabularies['anp_genres']
        ]:
            item.setdefault('subject', []).append({
                'name': self._vocabularies['anp_genres'][category_qcode]['name'],
                'qcode': category_qcode,
                'scheme': 'anp_genres'
            })

        for keyword in article.get('keywords', []):
            item.setdefault('keywords', []).append(keyword)

        # fetch media if item contains a media_link
        if article.get('media_link'):
            self._add_featuremedia(provider, item, article['media_link'])

        return item

    def _parse_date(self, string):
        return datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%SZ')


register_feed_parser(ANPNewsApiFeedParser.NAME, ANPNewsApiFeedParser())
