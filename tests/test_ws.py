import pytest
import asyncio
import websockets
import json

@pytest.mark.asyncio
async def test_websocket():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({"message": "ping"}))
        response = await websocket.recv()
        assert response is not None