import os


def configurelevel1():
    # Create our sudoers file in the right place
    os.system("touch /etc/sudoers.d/10-lowpriv")
    # Write sudoers policy for the lowpriv user to be able to create the correct directory path
    os.system("echo 'lowpriv ALL = (ALL) NOPASSWD:/home/lowpriv/a/b/c/*/' > /etc/sudoers.d/10-lowpriv")


def configurelevel2():
    # Create our highpriv user with the correct password ('th3R34lm')
    os.system("useradd -ms /bin/bash highpriv -p '$6$WNoVE3bATs7RF55t$.S6qT/b7.Zul1Vks/tAz7gcOK/Hb4oL1JAzOewnjkU5d/4"
              "WFPDWaJpLWgtFP.cxPJbLhIEeP/6ZZgwwjCF5OI0'")
    # Lowpriv is nopasswd to /home/lowpriv/access/check, to execute as highpriv
    os.system("echo 'lowpriv ALL=(highpriv) NOPASSWD:/home/lowpriv/access/check' > /etc/sudoers.d/lowpriv")
    # Highpriv is passwd to /home/highpriv/a*a/b/*/C/*.cfm, but requires password
    os.system("echo 'highpriv ALL=(ALL) /home/highpriv/a*a/b/*/C/*.cfm' > /etc/sudoers.d/highpriv")
    # Leave password for highpriv in /home/highpriv/.creds/pass for people to find
    os.system("mkdir -p /home/highpriv/.creds/")
    os.system("echo th3R34lm > /home/highpriv/.creds/pass")


def configurelevel3():
    # Create our highpriv user with a weak password ('Password1')
    os.system("useradd -ms /bin/bash highpriv -p '$1$clI2uTwV$B1uDZSzyFBFuk2eiVzzTx/'")
    # Lowpriv is passwd to /bin/cat as root
    os.system("echo 'lowpriv ALL=(ALL) /usr/bin/cat' > /etc/sudoers.d/lowpriv")
    # Highpriv is passwd to /bin/find as root
    os.system("echo 'highpriv ALL=(ALL) /usr/bin/find' > /etc/sudoers.d/highpriv")


def rewindlevel1():
    # Remove the sudoers file we created
    os.system("rm /etc/sudoers.d/10-lowpriv")


def rewindlevel2():
    # Remove our newly-created directory and all files
    os.system("rm -r /home/highpriv/.creds/")
    # De-configure sudoers
    os.system("rm /etc/sudoers.d/*")
    # Remove our highpriv user
    os.system("userdel -r highpriv")


def rewindlevel3():
    # Remove our created user
    os.system("userdel -r highpriv")
    # Remove our sudo configs
    os.system("rm /etc/sudoers.d/*")
