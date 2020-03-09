
from superdesk.publish.formatters import NINJSFormatter


class CustomNINJSFormatter(NINJSFormatter):

    direct_copy_properties = NINJSFormatter.direct_copy_properties + ('family_id',)

    def __init__(self):
        super().__init__()
        self.format_type = 'custom_ninjs'
