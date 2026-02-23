import asyncio
import json
from collections.abc import Callable
from typing import Any

import websockets
from pydantic import TypeAdapter
from websockets.client import WebSocketClientProtocol

from rocket_sdk_python.types.ws import ClientMessage, ServerMessage


class WsClient:
    def __init__(self, url: str, handler: Callable[[ServerMessage], None]):
        self._url = url
        self._handler = handler
        self._ws: WebSocketClientProtocol | None = None
        self._running = False
        self._send_queue: asyncio.Queue[ClientMessage | None] = asyncio.Queue()
        self._server_message_adapter = TypeAdapter(ServerMessage)

    async def connect(self):
        self._ws = await websockets.connect(self._url)
        self._running = True
        await asyncio.gather(
            self._receive_loop(),
            self._send_loop(),
        )

    async def _receive_loop(self):
        if not self._ws:
            return
        try:
            async for message in self._ws:
                if isinstance(message, str):
                    try:
                        data = json.loads(message)
                        server_msg = self._server_message_adapter.validate_python(data)
                        self._handler(server_msg)
                    except Exception as e:
                        print(f"Failed to parse server message: {e}")
                        print(f"Raw message: {message}")
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed")
        finally:
            self._running = False

    async def _send_loop(self):
        if not self._ws:
            return
        while self._running:
            try:
                msg = await asyncio.wait_for(self._send_queue.get(), timeout=0.1)
                if msg is None:
                    break
                msg_dict = msg.model_dump(by_alias=True, exclude_none=True)
                await self._ws.send(json.dumps(msg_dict))
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"Error sending message: {e}")

    def send(self, message: ClientMessage):
        asyncio.create_task(self._send_queue.put(message))

    async def close(self):
        self._running = False
        await self._send_queue.put(None)
        if self._ws:
            await self._ws.close()


class WsClientSync:
    def __init__(self, url: str, handler: Callable[[ServerMessage], None]):
        self._url = url
        self._handler = handler
        self._client: WsClient | None = None
        self._loop: asyncio.AbstractEventLoop | None = None
        self._thread: Any = None

    def connect(self):
        import threading

        def run_loop():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._client = WsClient(self._url, self._handler)
            self._loop.run_until_complete(self._client.connect())

        self._thread = threading.Thread(target=run_loop, daemon=True)
        self._thread.start()

    def send(self, message: ClientMessage):
        if self._client and self._loop:
            asyncio.run_coroutine_threadsafe(
                self._client._send_queue.put(message), self._loop
            )

    def close(self):
        if self._client and self._loop:
            asyncio.run_coroutine_threadsafe(self._client.close(), self._loop)
        if self._thread:
            self._thread.join(timeout=5)
