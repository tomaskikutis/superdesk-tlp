
import unittest

from superdesk.tests import TestCase
from anp.formatters import CustomNINJSFormatter


class MetadataTestCase(unittest.TestCase):

    def test_can_format(self):
        formatter = CustomNINJSFormatter()
        self.assertTrue(formatter.can_format('custom_ninjs', {}))


class CustomNINJSFormatterTestCase(TestCase):

    def test_family_id(self):
        items = [
            {'_id': 'orig'},
            {'_id': 'next', 'rewrite_of': 'orig'},
            {'_id': 'last', 'rewrite_of': 'next'},
        ]

        for item in items:
            item.update({'language': 'en', 'type': 'text', 'copyrightholder': 'foo'})

        self.app.data.insert('archive', items)

        formatter = CustomNINJSFormatter()

        for i, item in enumerate(items):
            ninjs = formatter._transform_to_ninjs(items[i], {})
            if i == 0:
                self.assertIsNone(ninjs.get('original'))
            else:
                self.assertEqual('orig', ninjs['original'])
