# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from rest_framework.renderers import JSONRenderer


class GeniFlowAPIRenderer(JSONRenderer):
    """
    This renderer extends the JSONRenderer and sets the media type to
    'application/vnd.geniflow+json', which is used to specify the format
    of the response data for the GeniFlow API.
    """

    media_type = "application/vnd.geniflow+json"
