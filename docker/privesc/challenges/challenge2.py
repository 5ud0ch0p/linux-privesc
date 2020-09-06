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
    rewindlevel1();
    rewindlevel3();
    # Create the SSH pubkey-based authentication folder/file structure
    os.system("mkdir /root/.ssh")
    os.system("touch /root/.ssh/authorized_keys")
    # Allow global write on /root/.ssh/authorized_keys
    os.system("chmod o+rx /root/")
    os.system("chmod o+wx /root/.ssh/authorized_keys")
    # Candidates need to be careful with how they enter their public keys into this file.
    # Echo with double quotes (") will cause bash to evaluate special characters in their public keys!


def configurelevel3():
    # Force rewind after each challenge
    rewindlevel1();
    rewindlevel2();
    os.system("useradd -ms /bin/bash highpriv -p '$1$ZRaXGLz7$lw1ILV3eoNwS4SRmcHrmQ1'")
    os.system("cp /etc/shadow /tmp/hashbackup")
    os.system("chmod 444 /tmp/hashbackup")
    os.system("cp /home/lowpriv/privesc/challenges/files/xor.core.34 /var/lib/systemd/coredump/")
    os.system("chown highpriv:highpriv /var/lib/systemd/coredump/xor.core.34")
    os.system("chmod 400 /var/lib/systemd/coredump/xor.core.34")


def rewindlevel1():
    print("Rewinding level 1")
    # Delete the 'highpriv' user
    os.system("userdel -r highpriv")
    # Restore the shadow file
    os.system("mv /etc/shadow.bak /etc/shadow")
    # Delete the files created in /tmp/ and lowpriv home
    os.system("rm /tmp/highpriv")
    os.system("rm /home/lowpriv/root13.txt")


def rewindlevel2():
    # Delete the previously-created /root/.ssh/ directory, and the files within
    os.system("rm -r /root/.ssh/")


def rewindlevel3():
    print("Rewinding level 3")
    # Delete the 'highpriv' user
    os.system("userdel -r highpriv")
    # Delete the /tmp/hashbackup/ file
    os.system("rm /tmp/hashbackup")
    # Remove the coredump file
    os.system("rm /var/lib/systemd/coredump/xor.core.34")

