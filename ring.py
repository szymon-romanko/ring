#! /bin/python
import _thread
import sys

try:
    import ring_config
except ImportError:
    print("ring_config.py not found, using default settings")


    class ring_config:  # default settings
        ring_method = "terminal_bell"
        winsound_frequency = 2500
        winsound_duration = 1000
        beepy_sound = "ping"
        loop_count = 10
        loop_interval = 1


def terminal_bell():
    """Works on all systems,
    can be ignored by terminal emulator"""
    print("\a", end="", flush=True)


def terminal_bell_echo():
    """Linux only,
    can be ignored by terminal emulator"""
    from os import system
    if _check_os("posix"):
        system('echo -e "\07"')
    else:
        _unsupported_system_warning()


def winsound_beep():
    """Windows only,
    using winsound module,
    frequency and duration can be changed in ring_config.py"""
    if _check_os("nt") and _check_module("winsound"):
        from winsound import Beep
        Beep(ring_config.winsound_frequency, ring_config.winsound_duration)
    else:
        _unsupported_system_warning()


def mac_nsbeep():
    """Mac only,
    using AppKit module (not tested)"""
    if _check_os("posix") and _check_module("AppKit"):
        from AppKit import NSBeep
        NSBeep()
    else:
        _unsupported_system_warning()


def beepy_module():
    """Cross-platform beep,
    using beepy module"""
    if _check_module("beepy"):
        from beepy import beep
        beep(sound=ring_config.beepy_sound)
    else:
        _unsupported_system_warning()


def _check_os(os_name: str) -> bool:
    """Checks if the current system is the same as the one specified,
    'nt' for Windows, 'posix' for Linux nad Mac"""
    from os import name
    return name == os_name


def _check_module(module_name: str) -> bool:
    """Checks if a module is imported"""
    # from sys import modules as sys_modules
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False
    # return module_name in sys_modules


def _unsupported_system_warning():
    # This warning is also displayed when required module is not found
    print("Trying to use ring method that is not supported on your system")


def single_ring():
    """Ring once"""
    if ring_config.ring_method == "terminal_bell":
        terminal_bell()
    elif ring_config.ring_method == "terminal_bell_echo":
        terminal_bell_echo()
    elif ring_config.ring_method == "winsound_beep":
        winsound_beep()
    elif ring_config.ring_method == "mac_nsbeep":
        mac_nsbeep()
    elif ring_config.ring_method == "beepy":
        beepy_module()
    else:
        print("Invalid ring method specified in ring_config.py, using default")
        terminal_bell()


def input_thread(a_list):
    input()
    a_list.append(True)


def loop_ring():
    """Ring in a loop"""
    from time import sleep
    count_down = ring_config.loop_count

    tmp_list = []  # captures user input while waiting
    _thread.start_new_thread(input_thread, (tmp_list,))  # https://stackoverflow.com/a/25442391

    print(f"Starting {count_down} ring loop, press Enter to stop")
    while True:
        if count_down == 0 or tmp_list:
            break
        single_ring()
        # sleep(ring_config.loop_interval)
        if ring_config.loop_interval > 1:  # helps with user input with long intervals
            for _ in range(ring_config.loop_interval):
                sleep(1)
                if tmp_list:
                    break
        else:
            sleep(ring_config.loop_interval)
        count_down -= 1
    print("Ring loop finished")


if __name__ == '__main__':
    if "-l" in sys.argv or "--loop" in sys.argv:
        loop_ring()
    else:
        single_ring()
