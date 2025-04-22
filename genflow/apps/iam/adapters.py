# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.http import HttpResponseRedirect


class DefaultAccountAdapterEx(DefaultAccountAdapter):
    def respond_email_verification_sent(self, request, user):
        return HttpResponseRedirect(settings.ACCOUNT_EMAIL_VERIFICATION_SENT_REDIRECT_URL)

    def render_mail(self, template_prefix, email, context, headers=None):
        protocol = "https" if self.request.is_secure() else "http"
        site = context["current_site"]
        context["current_site_url"] = f"{protocol}://{site.domain}"
        return super().render_mail(
            template_prefix,
            email,
            context,
            headers=headers,
        )
