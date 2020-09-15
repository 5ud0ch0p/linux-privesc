import os


def configurelevel1():
    # Back up /etc/shadow and /etc/passwd to facilitate rewind
    os.system("cp /etc/shadow /etc/shadow.bak")
    # Create 'highpriv' user
    os.system("useradd -ms /bin/bash highpriv -p '$5$IzvTeRpSWBYIoXpR$XpM2wFH01QgPbyhFigy4E9Zb60u5O7wtxtH2a5nCgA8'")
    # Echo password ('correcthorsebatterystaple') into file in /tmp/
    os.system("echo 'correcthorsebatterystaple' > /tmp/highpriv")
    # Set 'root' password to our chosen value, and store it in a file in the 'lowpriv' home directory
    os.system("echo \"ThomasAAnderson\" | passwd --stdin root 2>&1 >/dev/null")
    os.system("echo 'GubznfNNaqrefba' > /home/lowpriv/root13.txt")
    # Set the homepriv home directory to be executable by other users so highpriv can cat the file
    os.system("chmod o+x /home/lowpriv/")
    # Set the newly-created password file to only have read by highpriv
    os.system("chown highpriv:highpriv /home/lowpriv/root13.txt")
    os.system("chmod 400 /home/lowpriv/root13.txt")


def configurelevel2():
    os.system("mkdir -p /var/temporal-keys/")
    # Create root keypair with guessable passphrase
    os.system("ssh-keygen -b 2048 -t rsa -C \"Passphrase is 'supersecure'\" "
              "-N supersecure -f /var/temporal-keys/temp-key >/dev/null 2>/dev/null")
    # Make private key world-readable
    os.system("chmod o+rx /var/temporal-keys/")
    os.system("chmod o+r /var/temporal-keys/temp-key*")
    # Add to root SSH authorized_keys
    os.system("mkdir -p /root/.ssh/")
    os.system("chmod 755 /root/.ssh/")
    os.system("touch /root/.ssh/authorized_keys")
    os.system("chmod 644 /root/.ssh/authorized_keys")
    os.system("cat /var/temporal-keys/temp-key.pub >> /root/.ssh/authorized_keys")



def configurelevel3():
    os.system("useradd -ms /bin/bash highpriv -p '$1$ZRaXGLz7$lw1ILV3eoNwS4SRmcHrmQ1'")
    os.system("cp /etc/shadow /tmp/hashbackup")
    os.system("chmod 444 /tmp/hashbackup")
    os.system("cp /home/lowpriv/privesc/challenges/files/xor.core.34 /var/lib/systemd/coredump/")
    os.system("chown highpriv:highpriv /var/lib/systemd/coredump/xor.core.34")
    os.system("chmod 400 /var/lib/systemd/coredump/xor.core.34")
    os.system("echo \"professorfalken\" | passwd --stdin root 2>&1 >/dev/null")
