import tempfile
from os import path
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
    if chall == 2:
        if difficulty == 1:
            challenge2.configurelevel1()
        elif difficulty == 2:
            challenge2.configurelevel2()
        elif difficulty == 3:
            challenge2.configurelevel3()
    if chall == 3:
        if difficulty == 1:
            challenge3.configurelevel1()
        elif difficulty == 2:
            challenge3.configurelevel2()
        elif difficulty == 3:
            challenge3.configurelevel3()
    if chall == 4:
        if difficulty == 1:
            challenge4.configurelevel1()
        elif difficulty == 2:
            challenge4.configurelevel2()
        elif difficulty == 3:
            challenge4.configurelevel3()
    if chall == 5:
        if difficulty == 1:
            challenge5.configurelevel1()
        elif difficulty == 2:
            challenge5.configurelevel2()
        elif difficulty == 3:
            challenge5.configurelevel3()
    if chall == 6:
        if difficulty == 1:
            challenge6.configurelevel1()
        elif difficulty == 2:
            challenge6.configurelevel2()
        elif difficulty == 3:
            challenge6.configurelevel3()
    if chall == 7:
        if difficulty == 1:
            challenge7.configurelevel1()
        elif difficulty == 2:
            challenge7.configurelevel2()
        elif difficulty == 3:
            challenge7.configurelevel3()
    if chall == 8:
        if difficulty == 1:
            challenge8.configurelevel1()
        elif difficulty == 2:
            challenge8.configurelevel2()
        elif difficulty == 3:
            challenge8.configurelevel3()
    if chall == 1337:
        if difficulty == 1:
            challenge1337.configurechall1()
        elif difficulty == 2:
            challenge1337.configurechall2()
        elif difficulty == 3:
            challenge1337.configurechall3()


def createchallmutex(chall, diff):
    tempdir = tempfile.gettempdir()
    #tempf = open(tempdir + "/privesc-p" + str(chall) + "l" + str(diff), 'x')
    tempf = open(tempdir + "/privesc-configured", 'x')
    tempf.close()


def checkchallmutex(chall, diff):
    tempdir = tempfile.gettempdir()
    #return path.exists(tempdir + "/privesc-p" + str(chall) + "l" + str(diff))
    return path.exists(tempdir + "/privesc-configured")
