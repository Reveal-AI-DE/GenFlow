# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Custom exception handler to replace the 'detail' key with 'message'.
    """
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)

    if response is not None and "detail" in response.data:
        # if detail is a list of strings, convert it to a string
        if isinstance(response.data["detail"], list) and all(
            isinstance(item, str) for item in response.data["detail"]
        ):
            response.data["detail"] = ", ".join(response.data["detail"])
            # Replace the 'detail' key with 'message'
            response.data["message"] = response.data.pop("detail")
        # if detail is a string, replace it with message
        elif isinstance(response.data["detail"], str):
            response.data["message"] = response.data.pop("detail")

    return response
