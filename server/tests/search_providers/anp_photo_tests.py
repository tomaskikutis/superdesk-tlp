
import unittest

from anp.search_providers import PhotoSearchProvider


RESPONSE = {
    'totalresults': 123,
    '1': {
        'id': 71948104,
        'reference1': '000_1FR1T8',
        'reference2': 'AFP',
        'entrydate': '20190418 14:16:50',
        'picturedate': '20190418 13:03:47',
        'filename': '71948104',
        'status': 1,
        'rights': 1,
        'objecttype': 0,
        'externalsource': 39,
        'thumbnail_url': 'https://storage.googleapis.com/anp-thumbnails-prod/71945000-71949999/71948104.jpg',
        'preview_url': 'https://www.anpfoto.nl//downloadpicturepreview.pp?id=71948104',
        'description': 'Stephanie Bierholdt, dressed in traditional Sorbian clothes',
        'title': 'tradition - Easter',
    },
}


class TestProxy():

    def __init__(self, response):
        self.response = response

    def search(self, params):
        return self.response


class ANPPhotoTestCase(unittest.TestCase):

    def test_instance(self):
        provider = PhotoSearchProvider({})
        self.assertEqual('ANP', provider.label)

    def test_find(self):
        config = {}
        provider = PhotoSearchProvider(config)
        setattr(provider, '_proxy', TestProxy(RESPONSE))

        query = {}
        cursor = provider.find(query, {})
        self.assertEqual(123, cursor.count())

        item = cursor[0]
        self.assertEqual('picture', item['type'])
        self.assertEqual('urn:anp:71948104', item['guid'])
        self.assertEqual('AFP', item['source'])
        self.assertEqual('AFP', item['credit'])
        self.assertEqual('AFP', item['byline'])
        self.assertEqual('AFP', item['copyrightnotice'])
        self.assertEqual(RESPONSE['1']['title'], item['headline'])
        self.assertEqual(RESPONSE['1']['description'], item['description_text'])
        self.assertEqual('2019-04-18T11:03:47+00:00', item['firstcreated'].isoformat())
        self.assertEqual('2019-04-18T12:16:50+00:00', item['versioncreated'].isoformat())

        renditions = item['renditions']
        self.assertEqual(RESPONSE['1']['thumbnail_url'], renditions['thumbnail']['href'])
        self.assertEqual(RESPONSE['1']['preview_url'], renditions['viewImage']['href'])
        self.assertEqual(RESPONSE['1']['preview_url'], renditions['baseImage']['href'])
        self.assertEqual(RESPONSE['1']['preview_url'], renditions['original']['href'])

    def test_picture_date_overflow(self):
        config = {}
        provider = PhotoSearchProvider(config)
        setattr(provider, '_proxy', TestProxy(RESPONSE.copy()))
        provider.proxy.response['1'] = RESPONSE['1'].copy()
        provider.proxy.response['1']['picturedate'] = '00010101 00:00:00'

        query = {}
        cursor = provider.find(query, {})
        item = cursor[0]
        self.assertEqual('2019-04-18T12:16:50+00:00', item['firstcreated'].isoformat())
