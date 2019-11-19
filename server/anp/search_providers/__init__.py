# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2019 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
import superdesk
from .anp_photo import PhotoSearchProvider
from .talpa_video import TalpaVideoSearchProvider


def init_app(app):
    superdesk.register_search_provider('anp', provider_class=PhotoSearchProvider)
    superdesk.register_search_provider('talpa_video', provider_class=TalpaVideoSearchProvider)
