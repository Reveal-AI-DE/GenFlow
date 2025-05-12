# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from allauth.account.adapter import get_adapter
from allauth.account.forms import default_token_generator
from allauth.account.utils import user_pk_to_url_str
from dj_rest_auth.forms import AllAuthPasswordResetForm
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

UserModel = get_user_model()


class ResetPasswordFormEx(AllAuthPasswordResetForm):
    # pylint: disable=too-many-positional-arguments
    def save(
        self,
        request=None,
        domain_override=None,
        email_template_prefix="authentication/password_reset_key",
        use_https=False,
        token_generator=default_token_generator,
        extra_email_context=None,
        **kwargs,
    ):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        for user in self.users:
            protocol = "https" if use_https else "http"
            uid = user_pk_to_url_str(user)
            token = token_generator.make_token(user)
            reset_url = (
                f"{protocol}://{domain}{settings.RESET_PASSWORD_URL}?uid={uid}&token={token}"
            )
            context = {
                "reset_url": reset_url,
                "user": user,
                "current_site_url": f"{protocol}://{domain}",
                "site_name": site_name,
                **(extra_email_context or {}),
            }

            get_adapter(request).send_mail(email_template_prefix, email, context)

        return self.cleaned_data["email"]
