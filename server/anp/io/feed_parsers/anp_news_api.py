# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import logging
import datetime

from superdesk.io.registry import register_feed_parser
from superdesk.io.feed_parsers import FeedParser
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

    def can_parse(self, article):
        # this parser works only with "anp_news_api" feeding service
        return True

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

        for author in article.get('authors', []):
            item.setdefault('authors', []).append({
                'name': author,
                'role': 'writer'
            })

        for category in article.get('categories', []):
            item.setdefault('anpa_category', []).append({
                'name': category,
                'qcode': category
            })

        for keyword in article.get('keywords', []):
            item.setdefault('keywords', []).append(keyword)

        return item

    def _parse_date(self, string):
        return datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%SZ')


register_feed_parser(ANPNewsApiFeedParser.NAME, ANPNewsApiFeedParser())
