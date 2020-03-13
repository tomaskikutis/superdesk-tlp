
import superdesk

from superdesk.publish.formatters import NINJSFormatter


class CustomNINJSFormatter(NINJSFormatter):

    def __init__(self):
        super().__init__()
        self.format_type = 'custom_ninjs'

    def _transform_to_ninjs(self, article, subscriber, recursive=True):
        ninjs = super()._transform_to_ninjs(article, subscriber, recursive=recursive)

        orig = article
        for i in range(0, 50):  # just in case
            if orig.get('rewrite_of'):
                orig = superdesk.get_resource_service('archive').find_one(req=None, _id=orig['rewrite_of'])
                continue
            elif orig != article:
                ninjs['original'] = orig['_id']
            break

        return ninjs
