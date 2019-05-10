#!/usr/bin/env python
# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import os
from pathlib import Path
from superdesk.default_settings import INSTALLED_APPS, strtobool


def env(variable, fallback_value=None):
    env_value = os.environ.get(variable, '')
    if len(env_value) == 0:
        return fallback_value
    else:
        if env_value == "__EMPTY__":
            return ''
        else:
            return env_value


ABS_PATH = str(Path(__file__).resolve().parent)

init_data = Path(ABS_PATH) / 'data'
if init_data.exists():
    INIT_DATA_PATH = init_data

INSTALLED_APPS = [
    'apps.languages',
    'anp.io',
    'anp.photo',
]

RENDITIONS = {
    'picture': {
        'thumbnail': {'width': 220, 'height': 120},
        'viewImage': {'width': 640, 'height': 640},
        'baseImage': {'width': 1400, 'height': 1400},
    },
    'avatar': {
        'thumbnail': {'width': 60, 'height': 60},
        'viewImage': {'width': 200, 'height': 200},
    }
}

WS_HOST = env('WSHOST', '0.0.0.0')
WS_PORT = env('WSPORT', '5100')

LOG_CONFIG_FILE = env('LOG_CONFIG_FILE', 'logging_config.yml')

REDIS_URL = env('REDIS_URL', 'redis://localhost:6379')
if env('REDIS_PORT'):
    REDIS_URL = env('REDIS_PORT').replace('tcp:', 'redis:')
BROKER_URL = env('CELERY_BROKER_URL', REDIS_URL)

SECRET_KEY = env('SECRET_KEY', '')

DEFAULT_TIMEZONE = "Europe/Amsterdam"

DEFAULT_LANGUAGE = 'nl'
LANGUAGES = [
    {'language': 'nl', 'label': 'Dutch', 'source': True, 'destination': True},
    {'language': 'fr', 'label': 'French', 'source': True, 'destination': True},
    {'language': 'en', 'label': 'English', 'source': False, 'destination': False},
    {'language': 'de', 'label': 'German', 'source': False, 'destination': False},
    {'language': 'ja', 'label': 'Japanese', 'source': False, 'destination': False},
    {'language': 'es', 'label': 'Spanish', 'source': False, 'destination': False},
    {'language': 'ru', 'label': 'Russian', 'source': False, 'destination': False}
]

TIMEZONE_CODE = {
    'aus': 'America/Chicago',
    'bat': 'Asia/Manila',
    'bgl': 'Asia/Kolkata',
    'cav': 'Asia/Manila',
    'cat': 'Europe/Rome',
    'chb': 'Asia/Bangkok',
    'chd': 'America/Phoenix',
    'chm': 'America/New_York',
    'cos': 'America/Denver',
    'cpn': 'America/Chicago',
    'cri': 'America/New_York',
    'dal': 'America/Chicago',
    'dlf': 'Europe/Amsterdam',
    'drs': 'Europe/Berlin',
    'ftc': 'America/Denver',
    'gdh': 'Asia/Kolkata',
    'grn': 'Europe/Paris',
    'hlb': 'America/Los_Angeles',
    'hrt': 'America/Chicago',
    'irv': 'America/Los_Angeles',
    'ist': 'Asia/Istanbul',
    'kws': 'Asia/Tokyo',
    'lac': 'Europe/Paris',
    'lee': 'America/New_York',
    'mbf': 'America/New_York',
    'mfn': 'America/Los_Angeles',
    'nwb': 'Europe/London',
    'pav': 'Europe/Rome',
    'rlh': 'America/New_York',
    'roz': 'Europe/Rome',
    'shg': 'Asia/Shanghai',
    'sjc': 'America/Los_Angeles',
    'ssk': 'Asia/Seoul',
    'svl': 'America/Los_Angeles',
    'tai': 'Asia/Taipei',
    'ups': 'Europe/Vienna',
    'wst': 'America/Indiana/Indianapolis'
}

# This value gets injected into NewsML 1.2 and G2 output documents.
NEWSML_PROVIDER_ID = 'ANP'
ORGANIZATION_NAME = env('ORGANIZATION_NAME', 'ANP')
ORGANIZATION_NAME_ABBREVIATION = env('ORGANIZATION_NAME_ABBREVIATION', 'ANP')

PUBLISH_QUEUE_EXPIRY_MINUTES = 60 * 24 * 10  # 10d

# schema for images, video, audio
SCHEMA = {
    'picture': {
        'headline': {'required': False},
        'description_text': {'required': True},
        'credit': {'required': False},
        'byline': {'displayOnMediaEditor': False},
        'copyrightnotice': {'displayOnMediaEditor': False},
    },
    'video': {
        'headline': {'required': False},
        'description_text': {'required': True},
        'media_type': {'required': False},
        'credit': {'required': False},
        'byline': {'displayOnMediaEditor': False},
        'copyrightnotice': {'displayOnMediaEditor': False},
    },
}

# editor for images, video, audio
EDITOR = {
    'picture': {
        'headline': {'order': 1, 'sdWidth': 'full'},
        'description_text': {'order': 2, 'sdWidth': 'full', 'textarea': True},
        'credit': {'order': 3, 'sdWidth': 'full'},
        'byline': {'displayOnMediaEditor': False},
        'copyrightnotice': {'displayOnMediaEditor': False},
    },
    'video': {
        'headline': {'order': 2, 'sdWidth': 'full'},
        'description_text': {'order': 3, 'sdWidth': 'full', 'textarea': True},
        'media_type': {'order': 4, 'sdWidth': 'full'},
        'credit': {'order': 5, 'sdWidth': 'full'},
        'byline': {'displayOnMediaEditor': False},
        'copyrightnotice': {'displayOnMediaEditor': False},
    },
}

SCHEMA['audio'] = SCHEMA['video']
EDITOR['audio'] = EDITOR['video']

# media required fields for upload
VALIDATOR_MEDIA_METADATA = {
    "headline": {
        "required": False,
    },
    "description_text": {
        "required": True,
    },
    "credit": {
        "required": False,
    },
    "byline": {
        "required": False,
    },
    "copyrightnotice": {
        "required": False,
    },
}

# Template for "export as article" from planning
PLANNING_EXPORT_BODY_TEMPLATE = '''
{% for item in items %}
{% set pieces = [
    item.get('planning_date') | format_datetime(date_format='%H:%M'),
    item.get('slugline'),
    item.get('name'),
] %}
<h2>{{ pieces|select|join(' - ') }}</h2>
{% if item.coverages %}<p>{{ item.coverages | join(' - ') }}</p>{% endif %}
{% if item.get('description_text') or item.get('links') %}
<p>{{ item.description_text }}{% if item.get('links') %} URL: {{ item.links | join(' ') }}{% endif %}</p>
{% endif %}
{% if item.contacts %}{% for contact in item.contacts %}
<p>{{ contact.honorific }} {{ contact.first_name }} {{ contact.last_name }}{% if contact.contact_email %} - {{ contact.contact_email|join(' - ') }}{% endif %}{% if contact.contact_phone %} - {{ contact.contact_phone|selectattr('public')|join(' - ', attribute='number') }}{% endif %}</p>
{% endfor %}{% endif %}
{% if item.event and item.event.location %}
<p>{{ item.event.location|join(', ', attribute='name') }}</p>
{% endif %}
{% endfor %}
'''
