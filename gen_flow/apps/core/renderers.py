# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from rest_framework.renderers import JSONRenderer


class GenFlowAPIRenderer(JSONRenderer):
    '''
    This renderer extends the JSONRenderer and sets the media type to
    'application/vnd.gen_flow+json', which is used to specify the format
    of the response data for the GenFlow API.
    '''

    media_type = 'application/vnd.gen_flow+json'
