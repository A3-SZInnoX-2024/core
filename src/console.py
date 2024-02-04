from socketio import Client

sio = Client(reconnection=True)

@sio.event('arm_motion_end')
def arm_motion_end(data):
    print(f"Arm motion end: {data}")

@sio.event('robot_motion_end')
def robot_motion_end(data):
    print(f"Robot motion end: {data}")

@sio.event
def connect():
    print("I'm connected!")
    while True:
        command = input("Enter a command: ")
        if command == "exit":
            break
        elif command.startswith("arm"):
            cmd = command.split(" ")[1]
            if cmd == "status":
                print("arm status")
            elif cmd == "enable":
                print("arm enable")
                sio.emit('arm_motion_start', 'a')
            elif cmd == "disable":
                print("arm disable")
            else:
                print("Invalid arm command")
        elif command.startswith("location"):
            if command.split(' ')[1] == "status":
                print("location status")
            else:
                cmds = command.replace(',', ' ').split(' ')
                if len(cmds) == 4:
                    print(f"location set to x={cmds[1]}, y={cmds[2]}, theta={cmds[3]}")
                    sio.emit('move_to', data=(cmds[1], cmds[2], cmds[3]))
        elif command.startswith("status"):
            print("status")
        else:
            print("Invalid command")

sio.connect("http://localhost:8000")

sio.wait()
