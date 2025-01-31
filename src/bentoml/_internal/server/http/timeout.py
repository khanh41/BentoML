from __future__ import annotations

from typing import TYPE_CHECKING

import anyio
from starlette.responses import PlainTextResponse

if TYPE_CHECKING:
    from ... import external_typing as ext


class TimeoutMiddleware:
    def __init__(self, app: ext.ASGIApp, timeout: int) -> None:
        self.app = app
        self.timeout = timeout

    async def __call__(
        self, scope: ext.ASGIScope, receive: ext.ASGIReceive, send: ext.ASGISend
    ) -> None:
        if scope["type"] not in ("http", "websocket"):
            return await self.app(scope, receive, send)
        async with anyio.create_task_group():
            try:
                with anyio.fail_after(self.timeout):
                    await self.app(scope, receive, send)
            except TimeoutError:
                resp = PlainTextResponse(
                    f"Not able to process the request in {self.timeout} seconds",
                    status_code=504,
                )
                await resp(scope, receive, send)
