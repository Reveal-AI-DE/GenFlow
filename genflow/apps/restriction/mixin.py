# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from abc import ABCMeta, abstractmethod

from genflow.apps.restriction.models import Limit


class UserLimitMixin(metaclass=ABCMeta):
    """
    Mixin to handle limit checks on the user level.
    """

    @abstractmethod
    def get_user_usage(self) -> int:
        """
        Get the current usage for a specific user.
        """
        ...

    def check_user_limit(self, user_id, key: str) -> bool:
        """
        Check if the user has reached their limit for a specific key.
        """

        try:
            user_limit = Limit.objects.get(key=key, user_id=user_id)
            return bool(user_limit.value <= self.get_user_usage())
        except Limit.DoesNotExist:
            # If no limit is set for the user, return False (not limited)
            return False


class TeamLimitMixin(metaclass=ABCMeta):
    """
    Mixin to handle limit checks on the team level.
    """

    @abstractmethod
    def get_team_usage(self) -> int:
        """
        Get the current usage for a specific team.
        """
        ...

    def check_global_limit(self, key: str) -> bool:
        """
        Check if the global limit has been reached for a specific key.
        """

        try:
            global_limit = Limit.objects.get(key=key, user=None, team=None)
            return bool(global_limit.value <= self.get_team_usage())
        except Limit.DoesNotExist:
            # If no global limit is set, return False (not limited)
            return False

    def check_team_limit(self, team_id, key: str) -> bool:
        """
        Check if the team has reached their limit for a specific key.
        """

        try:
            team_limit = Limit.objects.get(key=key, team_id=team_id)
            return bool(team_limit.value <= self.get_team_usage())
        except Limit.DoesNotExist:
            # If no limit is set for the team, check for global limit
            return self.check_global_limit(key)


class LimitMixin(UserLimitMixin, TeamLimitMixin, metaclass=ABCMeta):
    """
    Mixin to handle limit checks.
    """

    def check_limit(self, user_id, team_id, key: str) -> bool:
        """
        Check if the limit has been reached.
        """

        user_limit = self.check_user_limit(user_id, key)
        team_limit = self.check_team_limit(team_id, key)

        if user_limit or team_limit:
            return True
        return False
