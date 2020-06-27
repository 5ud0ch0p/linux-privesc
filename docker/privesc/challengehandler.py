import tempfile
from os import path
from os import remove
from challenges import *


def configurechallenge(chall, difficulty):
    createchallmutex(chall, difficulty)
    if chall == 1:
        if difficulty == 1:
            challenge1.configurelevel1()
        elif difficulty == 2:
            challenge1.configurelevel2()
        elif difficulty == 3:
            challenge1.configurelevel3()


def createchallmutex(chall, diff):
    tempdir = tempfile.gettempdir()
    tempf = open(tempdir + "/privesc-p" + str(chall) + "l" + str(diff), 'x')
    tempf.close()


# TODO: Test this
def teardownchallenge(chall, difficulty):
    if chall == 1:
        if difficulty == 1:
            challenge1.rewindlevel1()
        elif difficulty == 2:
            challenge1.rewindlevel2()
        elif difficulty == 3:
            challenge1.rewindlevel3()
    removechallmutex(chall, difficulty)


# TODO: Test this
def removechallmutex(chall, diff):
    mutexpath = tempfile.gettempdir() + "/privesc-p" + str(chall) + "l" + str(diff)
    if path.exists(mutexpath):
        remove(mutexpath)


def checkchallmutex(chall, diff):
    tempdir = tempfile.gettempdir()
    return path.exists(tempdir + "/privesc-p" + str(chall) + "l" + str(diff))
