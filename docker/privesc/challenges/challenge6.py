import os


def configurelevel1():
    # Create testuser with a weak password ('testuser'), and assign their login shell to /usr/bin/python3
    os.system("useradd -ms /usr/bin/python3 testuser -p '$6$TK.f90Ah5oPxWATl$9JrorUc6dHsSMqpO9u92e.xpiRnfEnGkcYHjlT43K"
              "H16GZQpAgttWvl9LjVe1Gk/YeEn9t4ShEnPbsKXM12cq1'")
    # Create 'highpriv' user with appropriate login shell (vim) and password ('morph3us'),
    # and store it in the right location (/home/testuser/next.txt)
    os.system("useradd -ms /usr/bin/vim highpriv -p '$6$i7FceTnXtK1hRaG3$MUUm3KGMrxLDeZkBJ3L866hRqojl9ZB/XOsS85HCtZh66"
              "xRNam0dJDIR.yntt1VjFdRnzKtnZXq9wNnT3.sBq.'")
    os.system("echo 'morph3us' >> /home/testuser/next.txt")
    os.system("chown testuser:testuser /home/testuser/next.txt")
    os.system('chmod 400 /home/testuser/next.txt')
    # Change root password (to 'sw0rdf1sh') and store plaintext value at '/home/highpriv/root.txt'
    os.system("echo \"sw0rdf1sh\" | passwd --stdin root 2>&1 >/dev/null")
    os.system("echo 'sw0rdf1sh' >> /home/highpriv/root.txt")
    os.system("chown highpriv:highpriv /home/highpriv/root.txt")
    os.system("chmod 400 /home/highpriv/root.txt")


def configurelevel2():
    # Copy /bin/bash to /bin/rbash (apparently for some reason this actually implements rbash!)
    os.system("cp /bin/bash /bin/rbash")
    # Create the 'restricted' user and set rbash as the login shell for our 'restricted' user. The password for this
    # account is "nfoi24W9osda", but isn't supposed to be accessed via password authentication
    os.system("useradd -ms /bin/rbash restricted -p '$6$Z2ldK8RY7UXBY1v2$0kc.ydq.28pUmlg3Vfu9m9oyftiUpZo/GX0QWqF"
              "PyO1PwFivHYGZ1y.p/N5mS.PJIFuenn04cD.vdHijgGEJZ1'")
    # Generate SSH keys and the appropriate dirs and perms for our rbash user, and store the keys in /tmp/
    os.system('mkdir /home/restricted/.ssh/')
    os.system('chown restricted:restricted /home/restricted/.ssh/')
    os.system('chmod 755 /home/restricted/.ssh/')
    os.system('ssh-keygen -f /tmp/restricted -P "" > /dev/null')
    os.system('cat /tmp/restricted.pub >> /home/restricted/.ssh/authorized_keys')
    os.system('chmod 644 /home/restricted/.ssh/authorized_keys')
    os.system('chown restricted:restricted /home/restricted/.ssh/authorized_keys')
    # Configure sudo on restricted for copy of 'su'
    os.system('mv /usr/bin/su /srv/su')
    os.system("echo 'restricted ALL=(ALL) NOPASSWD:/srv/su' > /etc/sudoers.d/restricted")


def configurelevel3():
    # Create calc user with a weak password ('password')
    os.system("useradd -ms /bin/bash calc -p '$6$lfoU2VJ1okMduMev$qWu/kdsNjIjvkZd7a1pqmgy0cKxIUB.T56DYjM7aHYh4iTa"
              "d/lsg5yWYDSJacbynwA76/JuCnNqp62IGwu6iG0'")
    # Prevent the use of CTRL+C within the 'calc' user profile, and run bc on login (but NOT as a login shell)
    os.system("echo -e \"stty intr \'\'\nbc\" >> /home/calc/.bash_profile")
    # Generate SSH keys for 'root', put in correct directory for login,
    # store in /keys/, and chown/chmod to read-only for calc
    os.system('mkdir /keys/')
    os.system('mkdir /root/.ssh/')
    os.system('chmod 755 /root/.ssh/')
    os.system('ssh-keygen -f /keys/root -P "" > /dev/null')
    os.system('cat /keys/root.pub >> /root/.ssh/authorized_keys')
    os.system('chmod 644 /root/.ssh/authorized_keys')
    os.system('chown calc:calc /keys/root*')
    os.system('chmod 400 /keys/root*')
    # Set the root login shell to awk
    os.system('chsh -s /usr/bin/awk > /dev/null 2> /dev/null')