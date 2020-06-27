#!/usr/bin/env python3
import menu
from os import path


def runningindocker():
    return path.exists("/.dockerenv")


if __name__ == '__main__':
    # Make sure we don't unintentionally introduce security vulns into a device we didn't mean to!
    if not runningindocker():
        print('''        
        It looks like we aren't running in a docker container.
        This script is designed to intentionally introduce security weaknesses into whichever device it runs in.
        It is STRONGLY RECOMMENDED not to run this on a device you do not wish to make weaker than it already is!
        If you REALLY, REALLY, REALLYREALLYREALLY, R E A L L Y want to run this script, you need to remove 
        this check, or there are obviously other ways to run the contents of this script. 
        Which you will likely figure out!
        ''')
        exit(0)
    else:
        menu.menu()
