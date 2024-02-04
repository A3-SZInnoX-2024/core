import datetime
import numpy as np
from socketio import AsyncServer, ASGIApp
from aiohttp import web

sio = AsyncServer(cors_allowed_origins="*")
socket = web.Application()
sio.attach(socket)

@sio.on('connect')
async def connect(sid, environ):
    print(f"connected {sid}")

@sio.on('disconnect')
async def disconnect(sid):
    print(f"disconnected {sid}")

@sio.on('location-cv')
async def location_cv(sid, x, y, theta):
    print(f"Received location data from cv: {x}, {y}, {theta}")
    await sio.emit('location-rc', (x, y, theta))

@sio.on('block-cv')
async def block_cv(sid, x, y, color: str):
    print(f"Received block data from cv: {x}, {y}, {color}")
    await sio.emit('block-rc', (x, y, color))

if __name__ == "__main__":
    web.run_app(socket, port=8000)
