import os


def configurelevel1():
    # Add LD_PRELOAD to sudoers
    os.system("echo 'Defaults env_keep += LD_PRELOAD' >> /etc/sudoers")
    # Allow lowpriv to run 'ls' as ALL
    os.system("echo 'lowpriv ALL=(ALL) /usr/bin/ls' > /etc/sudoers.d/lowpriv")


def configurelevel2():
    # Create highpriv user with appropriate password ('aleph1')
    os.system("useradd -ms /bin/bash highpriv -p '$5$rtD9RvwwvG4H4q3D$f2GEszRv18RDOhXttalKfatZcCyCQz..oBOOBLVjVU8'")
    # Create binary location
    os.system("mkdir -p /srv/bins/spicy/")
    # Chown and chmod for highpriv
    os.system("chown highpriv:highpriv /srv/bins/spicy")
    os.system("chmod 750 /srv/bins/spicy")
    # Move binary and header with missing SO to /srv/bins/spicy
    os.system("cp /home/lowpriv/privesc/challenges/files/utils /srv/bins/spicy/")
    os.system("cp /home/lowpriv/privesc/challenges/files/disk.h /srv/bins/spicy/")
    os.system("chmod 755 /srv/bins/spicy/utils")
    os.system("chown root:root /srv/bins/spicy/utils")
    os.system("chmod u+s /srv/bins/spicy/utils")
    # Set the highpriv password as an environment variable for lowpriv
    os.system("echo 'HIGHPRIVPWD=\'aleph1\'' >> /home/lowpriv/.bash_profile")
    os.system("echo 'export HIGHPRIVPWD' >> /home/lowpriv/.bash_profile")


def configurelevel3():
    # Create highpriv user with password ('JLKHDAFL5136IUHBSN'), but password shouldn't be necessary
    os.system("useradd -ms /bin/bash highpriv -p '$5$FI6fe83ALOUWcTfO$dda1Sl3YiniQihQyGxJWnuo5Z.ZgVMx.4W7zG086jOA'")
    # Copy binary to correct location and give correct perms
    os.system("cp /home/lowpriv/privesc/challenges/files/usercounter /usr/bin/")
    os.system("chmod 755 /usr/bin/usercounter")
    # Set suid to allow first binary as highpriv
    os.system("echo 'lowpriv ALL=(highpriv) /usr/bin/usercounter' > /etc/sudoers.d/lowpriv")
    os.system("echo 'Defaults env_keep += LD_LIBRARY_PATH' >> /etc/sudoers")
    # Create location for second binary, and chmod such that only highpriv has access
    os.system("mkdir -p /home/highpriv/.bins-backup/")
    os.system("chown highpriv:highpriv /home/highpriv/.bins-backup/")
    os.system("chmod 600 /home/highpriv/.bins-backup/")
    # Copy second privesc binary to correct location (/home/highpriv/.bins-backup/logcleaner)
    # chown binary to root for suid, and give correct perms
    os.system("cp /home/lowpriv/privesc/challenges/files/logcleaner /home/highpriv/.bins-backup/logcleaner")
    os.system("chmod 755 /home/highpriv/.bins-backup/logcleaner")
    os.system("chown root:root /home/highpriv/.bins-backup/logcleaner")
    # Set suid on second binary
    os.system("chmod u+s /home/highpriv/.bins-backup/logcleaner")
    # Create link to address shared object requirement for second binary to non-existent SO
    # (rpath is set to /usr/lib/cleaner/libclean.so)
    os.system("mkdir -p /usr/lib/cleaner/")
    os.system("mkdir -p /home/highpriv/.libs-backup/")
    os.system("chown highpriv:highpriv /home/highpriv/.libs-backup/")
    os.system("ln -s /home/highpriv/.libs-backup/libclean.so /usr/lib/cleaner/libclean.so")
