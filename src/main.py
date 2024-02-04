import datetime
import numpy as np
from socketio import AsyncServer, ASGIApp
from aiohttp import web

sio = AsyncServer(cors_allowed_origins="*")
socket = web.Application()
sio.attach(socket)

arm_status = "stopped"
status = "stopped"
stamp_arm = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
location = {"x": 0, "y": 0, "z": 0, "roll": 0, "pitch": 0, "yaw": 0}
stamp_move = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@sio.on("location")
async def load_location(sid, data: np.ndarray):
    print(data)
    global location, stamp_move
    location = {
        "x": data[0],
        "y": data[1],
        "z": data[2],
        "roll": data[3],
        "pitch": data[4],
        "yaw": data[5],
    }
    stamp_move = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@sio.on('move_to')
async def move_to(sid, x: float, y: float, theta: float):
    global status
    status = "moving"
    print(f'Moving to x={x} y={y} theta={theta}')
    await sio.emit('robot_motion_start', data=(x, y, theta))

@sio.on("robot_motion_success")
async def robot_motion(sid, motion_status: str):
    global status, stamp_move
    status = "stopped"
    stamp_move = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await sio.emit("robot_motion_end", data={"status": motion_status})


@sio.on("robot_motion_failure")
async def robot_motion(sid, motion_status: str):
    global status, stamp_move
    status = "stopped"
    stamp_move = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await sio.emit("robot_motion_end", data={"status": motion_status})


@sio.on("arm_success")
async def arm_motion(sid, status: str):
    global arm_status, stamp_arm
    arm_status = status
    stamp_arm = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await sio.emit("arm_motion_end", data={"status": status})


@sio.on("arm_failure")
async def arm_motion(sid, status: str):
    global arm_status, stamp_arm
    arm_status = "stopped"
    stamp_arm = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await sio.emit("arm_motion_end", data={"status": status})


@sio.on("arm_motion_start")
async def arm_motion(sid, data: str):
    with open("log.txt", "a") as f:
        f.write(f"{data}\n")
    global arm_status
    arm_status = "moving"
    print(data, arm_status)
    await sio.emit("arm_motion_start", data={"status": "moving"})


if __name__ == "__main__":
    web.run_app(socket, port=8000)
