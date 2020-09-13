import os


def configurelevel1():
    os.system("mkdir -p /srv/tools/")
    os.system("cp /home/lowpriv/privesc/challenges/files/runas /srv/tools/runas")
    os.system("chown root:root /srv/tools/runas")
    os.system("chmod 755 /srv/tools/runas")
    os.system("chmod u+s /srv/tools/runas")


def configurelevel2():
    # Add suid to vi so users can privesc via multiple methods (vi bash escape, adding themselves to sudo, etc.)\
    os.system("chmod u+s /usr/bin/vim")


def configurelevel3():
    # Create highpriv user
    os.system("useradd -ms /bin/bash highpriv -p '$6$.XD0ewjNRzIBSySM$3G68UkC4FEpPACZ9o38J1dq8Rcm3bzm10kLeTHyJCgTZh"
              "VLyDW4B5goHd0FUdYoajWfPCnE8Ck5NgIdj9BmXz.'")
    # Copy find to location
    os.system("cp /usr/bin/find /tmp/find")
    os.system("chown highpriv:highpriv /tmp/find")
    # Set perms correctly
    os.system("chmod u+s /tmp/find")
    # Create directory tree and file
    os.system("mkdir -p /home/highpriv/3/1/3/3/7/")
    os.system("echo 'defconreallywascancelledthistime' > /home/highpriv/3/1/3/3/7/something.txt")
    # Copy visudo to relevant location
    os.system("mkdir -p /home/highpriv/.backup/admin/")
    os.system("cp /usr/sbin/visudo /home/highpriv/.backup/admin/visudo")
    # Give new visudo suid privs
    os.system("chmod u+s /home/highpriv/.backup/admin/visudo")
