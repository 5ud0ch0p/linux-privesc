import os
from random import randint


def configurelevel1():
    # Set root password properly
    os.system("echo 'phr43k3r$' | passwd --stdin root 2>&1 >/dev/null")
    # Pseudo-randomly generate our .bash_history from a few pre-determined commands
    HISTLENGTH = 500
    COMMANDOFFSET = 242
    historycommands = ["ls -l",
                       "cd ..",
                       "pwd",
                       "cat /etc/passwd > /dev/null",
                       "vi",
                       "find / -iname *.pub 2>/dev/null",
                       "echo",
                       "grep '=' /etc/*",
                       "cat /etc/passwd | awk -F':' '{print $1, $7}'",
                       "history",
                       "nmap -sS --top-ports 1000 0.0.0.0/0"]
    relevantcommand = "mysql -u root -p 'phr43k3r$'"
    for i in range(0, HISTLENGTH):
        commandindex = randint(0, len(historycommands) - 1)
        os.system("echo '" + historycommands[commandindex] + "' >> /home/lowpriv/.bash_history")
        if i == COMMANDOFFSET:
            os.system("echo " + relevantcommand + ">> /home/lowpriv/.bash_history")
    # Make sure .bash_history is owned by lowpriv
    os.system("chown lowpriv:lowpriv /home/lowpriv/.bash_history")
    print("""=== You might want to log out of your SSH session and log back in for this one! ===""")


def configurelevel2():
    # Create our highpriv user with the appropriate password
    os.system("useradd -ms /bin/bash highpriv -p '$6$j3ujlf9zaQ78ufkG$xbNIS5yfhOTeusvEZiUWKd6T7qB3mU8jnoZTigvbcIY7d"
              "pqSlgcPOZ7vNK1hGHcW5um4A69Jf0q7EzzdRYuj2.'")
    # Create our build-user.sh script containing the password for highpriv
    os.system("mkdir -p /srv/scripts/")
    os.system("touch /srv/scripts/build-user.sh")
    os.system("echo 'PASSWORD=m4xHeadr00m' >> /srv/scripts/build-user.sh")
    os.system("echo 'useradd -ms /bin/bash $USER -p \`echo $PASSWORD | openssl passwd -6 -stdin\`' "
              ">> /srv/scripts/build-user.sh")
    # Grant highpriv sudo access to useradd and userdel (just in case)
    os.system("echo 'highpriv ALL=(ALL) /usr/sbin/useradd' > /etc/sudoers.d/highpriv")
    os.system("echo 'highpriv ALL=(ALL) /sbin/userdel' >> /etc/sudoers.d/highpriv")
    # Create our temp user to own passwords file
    os.system("useradd -ms /bin/bash tempuser -u 1337 -p '$6$qN9SB1vasfEgY3SJ$r0UyXhNs1qjWJ63PzH1p5IoRn.MZh."
              "irFWILRcip8M/tkXXPLqF6W9xYKLSR/7UTBv0v3ByN04Ymx3EU2ULZX/'")
    # Create file in right location with password value and chown this to our temp user
    os.system("mkdir -p /srv/creds/")
    os.system("echo 'h4ck3rj30pardy' > /srv/creds/passwords.txt")
    os.system("chown tempuser:tempuser /srv/creds/passwords.txt")
    # And remove read perms for everyone else
    os.system("chmod 400 /srv/creds/passwords.txt")
    # Remove our temp user, orphaning the file
    os.system("userdel -r tempuser")
    # Set the root password appropriately
    os.system("echo 'h4ck3rj30pardy' | passwd --stdin root 2>&1 >/dev/null")


def configurelevel3():
    # Create temp user and home directory, populate .bash_history with password for highpriv
    os.system("useradd -ms /bin/bash crash -u 444 -p '$6$qN9SB1vasfEgY3SJ$r0UyXhNs1qjWJ63PzH1p5IoRn.MZh."
              "irFWILRcip8M/tkXXPLqF6W9xYKLSR/7UTBv0v3ByN04Ymx3EU2ULZX/'")
    os.system("touch /home/crash/.bash_history")
    os.system("echo 'cat /etc/passwd' > /home/crash/.bash_history")
    os.system("echo 'echo b_i-g_h-a_c-c | passwd -stdin $USER' > /home/crash/.bash_history")
    # Create highpriv user with password set above
    os.system("useradd -ms /bin/bash highpriv -p '$6$7Wlax9GNlB8mHVUY$6lyTbeRWlsqEKRR27rnHnplM55RYQEKsYof.HE33iZgamY"
              "jQ1M8zL2xhHuvzYavqP.7SMZeQWWQ3bVRDK5Wte0'")
    # Delete temp user, but keep homedir in place and all contained files
    os.system("userdel crash")
    # lowpriv has sudo on useradd - but not on userdel; need to be careful otherwise rebuild docker!
    os.system("echo 'lowpriv ALL=(ALL) /usr/sbin/useradd' > /etc/sudoers.d/lowpriv")
    # Copy across our log file
    os.system("cp /home/lowpriv/privesc/challenges/files/apache.log /var/log/")
    # Create our intermediary group ('admin')
    os.system("groupadd logadmin")
    # Chown the log file to allow group read access
    os.system("chown root:logadmin /var/log/apache.log")
    # Add highpriv to this group
    os.system("usermod -a -G logadmin highpriv")
    # And give the file read permissions on group
    os.system("chmod g+r /var/log/apache.log")
    # Set the root password appropriately
    os.system("echo 'fr33nod3L1v3s' | passwd --stdin root 2>&1 >/dev/null")
