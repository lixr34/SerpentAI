import sys
import subprocess
import socket
import time

import enum

from serpent.config import config


class SerpentError(BaseException):
    pass


class OperatingSystem(enum.Enum):
    LINUX = 0
    WINDOWS = 1
    MACOS = 2


def operating_system():
    if sys.platform in ["linux", "linux2"]:
        return OperatingSystem.LINUX
    elif sys.platform == "darwin":
        return OperatingSystem.MACOS
    elif sys.platform == "win32":
        return OperatingSystem.WINDOWS


def is_linux():
    return operating_system().name == "LINUX"


def is_macos():
    return operating_system().name == "MACOS"


def is_unix():
    return operating_system().name in ["LINUX", "MACOS"]


def is_windows():
    return operating_system().name == "WINDOWS"


def clear_terminal():
    if is_unix():
        print("\033c")
    elif is_windows():
        subprocess.call(["cls"], shell=True)


def display_serpent_logo():
    print("""
888888888888888888888888888888888888888888888888888888888888
888888888888888888888888877777777O88888888888888888888888888
8888888888888888888D77777777777777777$$888888888888888888888
88888888888888888777777777777777777777777O888888888888888888
88888888888888D7777777777777777777777777777$D888888888888888
8888888888888$77777777777777~ ........7777777888888888888888
8888888888877777777777777.      ..777777777777$8888888888888
8888888888777777777777?.       ~7777.?7.77777777888888888888
888888888777777777777.       .77.. ..77.7$777777788888888888
8888888877777777777$.       .$.  . 777.7.$7.7777778888888888
8888888D77777777777.       .77...777. ,7.$7.777777$888888888
888888877777777777~        ~777,..   77..7I $777777888888888
888888D77777777777.      .:7     ..77. .77..7777777788888888
888888$77777777777.    ..$.   ..$$7.. .77. 7.777777788888888
888888777777777777.   ,77.$7777+..   .77...7.$.7777788888888
88888877777777777777..77777777:   ..777...7..7.77777D8888888
8888887777777777777777777777$. ..?777.  .$. 7:.77777D8888888
888888777777777777777777+...I7777,.77. 7$. =7..7777788888888
8888887777777777777777777777777.. .7$.$...,7..77777788888888
888888$777777777777777777777777  .777,  .77. .77777788888888
888888877777777777777777777777:  .77.  .77.  777777888888888
8888888$7777777777777777777777. .77. .$77...I777777888888888
88888888$777777777777777777777..77..777.   I7777778888888888
88888888877777777777777777777..77.777.   .777777788888888888
888888888D777777777777777777.I7777...   .$777777888888888888
888888888887777777777777777777~.     ..$77777778888888888888
888888888888O7777777777777..       .:77777777788888888888888
888888888888887777777=...        :$7777777778888888888888888
8888888888888888I$.       ...:777777777777D88888. 88 8888888
888888888888888O     ...$7777777777777788888888.D.88 8888888
88888888888888.   .O888777777777777D88888888888 DD.8.8888888
888888888888. .?88888888888888888888888888888888888888888888
88888888888. 88888888888888888888888888888888888888888888888
8888888888 =888888888888888888888888888888888888888888888888
888888888888888888888888888888888888888888888888888888888888
888888888888888888888888888888888888888888888888888888888888
888888888888888888888888888888888888888888888888888888888888
888888888888888888888888888888888888888888888888888888888888
    """)


def wait_for_crossbar():
    while True:
        s = socket.socket()

        try:
            s.connect((config["crossbar"]["host"], config["crossbar"]["port"]))
            s.close()
            break
        except Exception:
            print("Waiting for Crossbar server...")
            time.sleep(0.1)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
