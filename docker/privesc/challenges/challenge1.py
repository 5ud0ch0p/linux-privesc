import os
import subprocess


def configurelevel1():
    # Back up /etc/shadow
    os.system("cp /etc/shadow /etc/shadow.bak")
    # Set 'root' password to 'root'
    os.system("echo \"root\" | passwd --stdin root 2>&1 >/dev/null")
    # SSH should already be configured to allow root access, so shouldn't need any more.


def configurelevel2():
    # Back up shadow so we can roll back
    os.system("cp /etc/shadow /etc/shadow.bak")
    # Configure the root account with a weak password ('hunter2'),
    # but not hashing using MD5 in shadow. Only using MD5 in the script
    os.system("echo \"hunter2\" | passwd --stdin root 2>&1 >/dev/null")
    os.system("echo \"for i in {1..10}; do head /dev/urandom; "
              "done\n\nfor i in {1..10}; do\necho $RANDOM;\ndone"
              "\n\nSEED=2ab96390c7dbe3439de74d0c9b0b1767\n\" > /home/lowpriv/encrypt-files.sh")
    # Similar situation here; SSH as 'root' should now be possible


def configurelevel3():
    # Python script to handle the command execution on the local loopback below
    pythonscript = """#!/usr/bin/env python3
import socket
import os

def bindlistener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 31337))
    sock.listen(5)
    while True:
        (clientsocket, address) = sock.accept()
        clientsocket.send("Enter password: ".encode("utf-8"))
        password = clientsocket.recv(999).decode("utf-8").strip()
        if checkauth(password):
            clientsocket.send("Enter command: ".encode("utf-8"))
            command = clientsocket.recv(999).decode("utf-8").strip()
            output = os.popen(command).read()
            clientsocket.send(output.encode("utf-8"))
        else:
            clientsocket.send("INCORRECT PASSWORD!\\n".encode("utf-8"))
        clientsocket.close()


def checkauth(inputpass):
    if inputpass == "password1":
        return True
    return False


if __name__ == '__main__':
    print("Binding")
    bindlistener()
"""
    # Write the above script to a file with the right permissions
    bindshellscript = open("/root/shellbound.py", "w")
    bindshellscript.write(pythonscript)
    bindshellscript.close()
    os.system("chmod 600 /root/shellbound.py")
    # And start the bind shell in the background
    subprocess.Popen("python3 /root/shellbound.py", shell=True)


def rewindlevel1():
    # Roll back shadow
    os.system("mv /etc/shadow.bak /etc/shadow")


def rewindlevel2():
    # Roll back shadow
    os.system("mv /etc/shadow.bak /etc/shadow")


def rewindlevel3():
    # TODO Ensure bind shell is killed
    # Delete the "password" file in /tmp/
    os.system("rm /tmp/bindshellpwd")
    # Delete the bind shell Python script
    os.system("rm /root/shellbound.py")