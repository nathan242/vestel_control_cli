#!/usr/bin/python3

import sys
import socket
import getopt
import readline

controls = {
    "home": 1046,
    "power": 1012,
    "power_nav": 1012,
    "power_player": 1012,
    "power_pvm": 1012,
    "power_ges_nav": 1012,
    "power_ges_player": 1012,
    "power_ges_pvm": 1012,
    "record": 1051,
    "play": 1025,
    "pause": 1049,
    "stop": 1024,
    "previous": 1034,
    "rewind": 1027,
    "forward": 1028,
    "next": 1255,
    "screen": 1011,
    "lang": 1015,
    "subtitle": 1031,
    "presets": 1014,
    "epg": 1047,
    "text": 1255,
    "fav": 1040,
    "3d": 1040,
    "sleep": 1042,
    "0": 1000,
    "1": 1001,
    "2": 1002,
    "3": 1003,
    "4": 1004,
    "5": 1005,
    "6": 1006,
    "7": 1007,
    "8": 1008,
    "9": 1009,
    "menu": 1048,
    "mute": 1013,
    "up": 1020,
    "left": 1021,
    "ok": 1053,
    "right": 1022,
    "down": 1019,
    "vol_up": 1016,
    "vol_down": 1017,
    "prog_up": 1032,
    "prog_down": 1033,
    "back": 1010,
    "exit": 1037,
    "red": 1055,
    "green": 1054,
    "yellow": 1050,
    "blue": 1052,
    "info": 1018,
    "mmedia": 1057,
    "source": 1056,
    "swap": 1034,
    "chan": 1045,
    "qmenu": 1043
}

class UndefinedCommand(Exception):
    pass

def help():
    print("Vestel Control CLI")
    print("Usage: "+sys.argv[0]+" [-h] [TV IP] (optional)[COMMAND]")
    print(" -h - Show this help")

def main(argv):
    try:
        optlist, args = getopt.getopt(argv, 'h')
    except getopt.GetoptError as err:
        sys.stderr.write(str(err)+"\n")
        sys.exit(1)

    for o, a in optlist:
        if o == "-h":
            help()
            sys.exit(0)
        else:
            sys.stderr.write("Unknown option: "+str(o)+"\n")
            sys.exit(1)

    argslen = len(args)
    if argslen < 1:
        sys.stderr.write("Address not specified\n")
        sys.exit(1)

    if argslen > 2:
        sys.stderr.write("Too many arguments\n")
        sys.exit(1)

    address = (args[0], 4660)
    command = None

    if argslen == 2:
        command = args[1]

    if command is not None:
        try:
            send(address, command)
        except UndefinedCommand as ex:
            sys.stderr.write(ex.args[0]+"\n")
            sys.exit(1)

        sys.exit(0)

    print("Commands:")
    print("help - list controls")
    print("quit - exit program")
    while True:
        command = input("> ")

        if command == "":
            continue
        elif command == "quit":
            sys.exit(0)
        elif command == "help":
            list_controls()
        else:
            try:
                send(address, command)
            except UndefinedCommand as ex:
                print(ex.args[0])

def list_controls():
    print("Controls:")

    for item in controls.items():
        print(item[0]+" => "+str(item[1]))

def connect(sock, address):
    try:
        sock.connect(address)
    except:
        sys.stderr.write("Cannot connect to "+address[0]+":"+str(address[1])+"\n")
        sys.exit(2)

def disconnect(sock):
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

def send(address, command):
    if (command not in controls):
        raise UndefinedCommand("Command "+command+" not known")

    sent = 0

    while sent == 0:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connect(sock, address)
            sent = sock.send(bytes(str(controls[command])+"\n", 'utf-8'))
        except BrokenPipeError:
            pass

        disconnect(sock)

if __name__ == "__main__":
    main(sys.argv[1:])

