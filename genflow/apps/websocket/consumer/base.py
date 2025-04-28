# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from abc import abstractmethod

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from genflow.apps.websocket.consumer import exception, status


class BaseConsumer(AsyncJsonWebsocketConsumer):
    """
    Abstract base class that extends AsyncJsonWebsocketConsumer
    to handle WebSocket connections with JSON payloads. It provides a mechanism
    to authenticate users and enforce permissions before establishing a connection.
    """

    async def connect(self):
        """
        Handles the WebSocket connection process. Authenticates the user,
            checks permissions, and accepts or closes the connection accordingly.
            Sends an error message if an exception occurs during the process.
        """

        error = None
        code = 0
        try:
            user = self.scope["user"]
            if user.is_authenticated:
                await self.check_permission()
                await self.accept(subprotocol="json")
            else:
                await self.close(code=status.WS_401_UNAUTHORIZED)
        except exception.BadRequestError as e:
            error = str(e)
            code = status.WS_400_BAD_REQUEST
        except exception.ForbiddenError as e:
            error = str(e)
            code = status.WS_403_FORBIDDEN
        except exception.NotFoundError as e:
            error = str(e)
            code = status.WS_404_NOT_FOUND
        except Exception as e:
            error = str(e)
            code = status.WS_500_INTERNAL_SERVER_ERROR

        if error is not None:
            await self.close(code=code, reason=error)

    @abstractmethod
    def check_permission(self):
        """
        Abstract method that must be implemented by subclasses to define
            specific permission checks for the WebSocket connection.
        """
