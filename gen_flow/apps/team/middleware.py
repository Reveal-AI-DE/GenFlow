# Copyright (C) 2024 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.core.exceptions import BadRequest
from django.utils.functional import SimpleLazyObject
from django.conf import settings

def get_team(request):
    '''
    Retrieves the team and privilege information for the given request.

    Args:
        request (HttpRequest): The HTTP request object containing user and query parameters.

    Returns:
        dict: A dictionary containing the team object and the privilege name.

    Raises:
        BadRequest: If the "team" query parameter and "X-Team" HTTP header have different values,
                    or if the specified team does not exist.
    '''

    from gen_flow.apps.team.models import Team

    IAM_ROLES = {
        role: priority
        for priority, role in enumerate(settings.IAM_ROLES)
    }
    groups = list(request.user.groups.filter(name__in=list(IAM_ROLES.keys())))
    groups.sort(key=lambda group: IAM_ROLES[group.name])
    privilege = groups[0] if groups else None

    team = None
    try:
        team_id = request.GET.get('team')
        team_header = request.headers.get('X-Team')

        if team_id is not None and team_header is not None and team_id != team_header:
            raise BadRequest('You cannot specify "team" query parameter and '
                             '"X-Team" HTTP header with different values.')
        team_id = team_id if team_id is not None else team_header
        if team_id is not None:
            team = Team.objects.get(id=int(team_id))
    except Team.DoesNotExist:
        raise BadRequest(f'{team_id} team does not exist.')

    context = {
        'team': team,
        'privilege': getattr(privilege, 'name', None)
    }

    return context


class ContextMiddleware:
    '''
    Middleware to attach team context to the request object.

    This middleware adds an `iam_context` attribute to the request object,
    which is a lazy object that evaluates to the team context for the current user.
    '''

    def __init__(self, get_response):
        # The next middleware or view in the chain
        self.get_response = get_response

    def __call__(self, request):
        '''
        Attaches the `iam_context` attribute to the request and calls the next middleware or view.
        '''

        # https://stackoverflow.com/questions/26240832/django-and-middleware-which-uses-request-user-is-always-anonymous
        request.iam_context = SimpleLazyObject(lambda: get_team(request))

        return self.get_response(request)
