import os


def configurechall1():
    # Create our various intermediary users.
    # Passwords are:
    # route:    c1t1z3nr3n3g4d3
    # rewt:     n30n4w4k3n1ng
    # rhoot:    $41nt3n1gm4
    os.system("useradd -ms /bin/bash route -p '$5$hELUm/NcsFKtw0Uo$mhmHZg91ytJ2C4au5DWc98by5bkLLjN3oVhpXZ172p0'")
    os.system("useradd -ms /bin/bash rewt -p '$5$E..8jzBTPxT2GU30$7mAoA4IYtA/KRAoZAK2Q.NJy9BePFdCN3jlD3E.yP43'")
    os.system("useradd -ms /bin/bash rhoot -p '$5$dtZQ9TVvg63/YcZI$ka4GdgZSYMbxsZQu0p47JVxv.7leOmWPSvWOS2ty9L4'")
    # Set our root password appropriately
    os.system("echo 'u$34ft3rfr33' | passwd --stdin root 2>&1 >/dev/null")
    # Configure sudo for lowpriv with LD_PRELOAD, allowing execution of id as route
    os.system("echo 'Defaults env_keep += LD_PRELOAD' >> /etc/sudoers.d/lowpriv")
    os.system("echo 'lowpriv ALL=(route) /usr/bin/id' >> /etc/sudoers.d/lowpriv")
    # Create SSH key for rewt, write private key to /tmp/.keys/rewt,
    # and set the public key as a recognised login for rewt
    os.system("mkdir -p /home/rewt/.ssh/")
    os.system("chown rewt:rewt /home/rewt/.ssh")
    os.system("chmod 700 /home/rewt/.ssh")
    os.system("mkdir -p /tmp/.keys/")
    os.system("ssh-keygen -b 2048 -t rsa -f /tmp/.keys/rewt -q -N ''")
    os.system("cat /tmp/.keys/rewt.pub >> /home/rewt/.ssh/authorized_keys")
    os.system("chmod 600 /home/rewt/.ssh/authorized_keys")
    os.system("chown rewt:rewt /home/rewt/.ssh/authorized_keys")
    # Chown and chmod /tmp/.keys/rewt to read-only as route
    os.system("chown route:route /tmp/.keys/")
    os.system("chown route:route /tmp/.keys/rewt")
    os.system("chmod 700 /tmp/.keys")
    # Configure login shell for rewt using our custom binary
    loginscript = '''#!/usr/bin/env python3
    
from sys import stdin, exit
from os import system

def checkcommand(line):
    if line.startswith("ps") or line.startswith("df") or line.startswith("netstat"):
        return True
    return False

for line in stdin:
    if checkcommand(line):
        system(line)
    else:
        print("Incorrect command! Must be ps, df or netstat (with args!)")
'''
    loginfile = open("/home/rewt/login.py", "w")
    loginfile.write(loginscript)
    loginfile.close()
    os.system("chown rewt:rewt /home/rewt/login.py")
    os.system("chmod 755 /home/rewt/login.py")
    os.system("usermod --shell /home/rewt/login.py rewt")
    # Create our directory and config file, print some pseudo-config file-like contents to it, along with the plaintext
    # password for rhoot
    os.system("mkdir -p /etc/microsoft/")
    os.system("chown rewt:rewt /etc/microsoft")
    os.system("chmod 700 /etc/microsoft")
    os.system("touch /etc/microsoft/config.conf")
    os.system("echo 'Enabled=true\nUser=rhoot\nPassword=$41nt3n1gm4\nLicenced=True\n"
              "Backdoored=True' >> /etc/microsoft/config.conf")
    # Set the root password as an environment variable in .bash_profile for rhoot
    os.system("echo 'export RHO0O0O0O0OT=u\$34ft3rfr33' >> /home/rhoot/.bash_profile")


def configurechall2():
    # Create two users, trinity and admin. Passwords are not important here, but are 'LKAJFHLKIA13441' and
    # 'NHB189hu{)HJ(O' respectively
    os.system("useradd -ms /bin/bash trinity -p '$6$9OhHpBzx1AqxbBUg$4tmOOATOnIie9Fj4hrubIOQRUTEID4buRUV0NEvaq1kvJOB4S."
              "OjY43bTohw4CqpRC7R43rkZn.VoPNIrZMJy0'")
    os.system("useradd -ms /bin/bash admin -p '$6$xONsuDO.h6iAmDQP$JYZbHTNeua5pFyt6YjNjlyxYIDU2NLyyceiyuM9aRZy9ArIj/l"
              "b8Aa7dFmbdGqnR.KC9CI6YMG1aq4k/3E/Ko.'")
    # Add lowpriv to sudoers to allow execution as trinity
    os.system("echo 'lowpriv ALL=(trinity) NOPASSWD:/*/high' >> /etc/sudoers.d/lowpriv")
    # Add lowpriv to sudoers to allow execution of cp as admin
    os.system("echo 'lowpriv ALL=(admin) /bin/cp' >> /etc/sudoers.d/lowpriv")
    # Add trinity to sudoers to allow execution of non-existent binary as 'admin'
    os.system("echo 'trinity ALL=(admin) NOPASSWD:/home/admin/shellz/spawn' >> /etc/sudoers.d/trinity")
    # Create /home/admin/shellz/ and chmod/chown appropriately
    os.system("mkdir -p /home/admin/shellz")
    os.system("chown admin:admin /home/admin/shellz")
    # Set 'root' password appropriately ('tu$k1ngt0n')
    os.system("echo 'tu$k1ngt0n' | passwd --stdin root 2>&1 >/dev/null")
    # Create file containing root password
    os.system("echo 'tu$k1ngt0n' >> /home/trinity/password.txt")
    # Create GPG key pair, store private key in trinity home directory
    os.system('cat >/home/trinity/keygen <<EOF\n'
              'Key-Type: DSA\n'
              'Key-Length: 2048\n'
              'Subkey-Type: ELG-E\n'
              'Subkey-Length: 2048\n'
              'Name-Real: root\n'
              'Name-Comment: root\n'
              'Name-Email: root@localhost\n'
              'Expire-Date: 0\n'
              'Passphrase: root\n'
              'EOF')
    os.system('su -c \'gpg --batch  --gen-key /home/trinity/keygen 2>/dev/null >/dev/null\' trinity')
    os.system('rm /home/trinity/keygen')
    # Encrypt root password file and move file to directory where only admin has access
    os.system('mkdir -p /var/keys/gpg/')
    os.system('chown admin:admin /var/keys/gpg')
    os.system('chmod 700 /var/keys/gpg/')
    os.system('su -c \'gpg --output /home/trinity/password.gpg --encrypt --recipient root@localhost '
              '/home/trinity/password.txt 2>/dev/null >/dev/null\' trinity')
    os.system('mv /home/trinity/password.gpg /var/keys/gpg/password.gpg')
    os.system('chown admin:admin /var/keys/gpg/password.gpg')
    os.system('chmod 700 /var/keys/gpg/password.gpg')
    # Remove original root password file
    os.system('rm /home/trinity/password.txt')
    # NOTE: Be careful of GPG flags during decryption; remember, we aren't in a true TTY!


def configurechall3():
    # Create our three intermediary users, passwords are (most of which aren't necessary):
    # zc = NullR3n3g4d3
    # ab = hoijuawbyo4ab
    # ck = thanksforplaying!
    os.system("useradd -ms /bin/bash zc -p '$6$CU0onL4IkkbB1xso$IPaXwNNfUn6QLB2ahD1T2.3y46vpTFdBvgOGGMhGeowaqqi1g/j"
              "4Lz6cSt.X.hlimUeZTSm7kjUDuWYo8hsVP.'")
    os.system("useradd -ms /bin/bash ab -p '$6$bmcFfNy7XCOauRTj$oYxbOyy.O2npv8pudYx.TrjoGwmD9d6gOk2t.JxMty6EwLGjdhr"
              "liDIM.bm9KWpVcC6U66csPkR6z4xrpow4T1'")
    os.system("useradd -ms /bin/bash ck -p '$6$qk7UCiczzp7kh.G0$uiekZzxCsBJ1kDILtiOJ/HU5kvk/.Ra80T0D8l/YEUROiF98Yo/"
              "ojrXMKQYZS1aOgaEekTvsfmjNwbw4pcP5W.'")
    # Create process to run with password as command-line argument, and run and background
    backgroundprog = '''#include <unistd.h>

int main() {
        while(1) {
                sleep(100);
        }
}
'''
    bgfile = open("/home/zc/monitor.c", "w")
    bgfile.write(backgroundprog)
    bgfile.close()
    os.system("gcc /home/zc/monitor.c -o /home/zc/monitor")
    os.system("rm /home/zc/monitor.c")
    os.system("su -c '/home/zc/monitor --password NullR3n3g4d3 &' zc")
    # Create our locally-writeable directory for our binary rpath
    os.system("mkdir -p /home/zc/libs/")
    os.system("chown zc:zc /home/zc/libs")
    os.system("chmod 775 /home/zc/libs")
    # Make zc home directory read/execute for all so cronjob can run
    os.system("chmod o+rx /home/zc/")
    # Copy our binary and library to the correct location
    os.system("mv /home/lowpriv/privesc/challenges/files/zipbackup /home/zc/zipbackup")
    os.system("chown zc:zc /home/zc/zipbackup")
    os.system("chmod o+rx /home/zc/zipbackup")
    os.system("mv /home/lowpriv/privesc/challenges/files/libzipper.so /home/zc/libs/libzipper.so")
    os.system("chown zc:zc /home/zc/libs/libzipper.so")
    os.system("chmod o+rx /home/zc/libs/libzipper.so")
    # and create our cronjob
    os.system("mkdir -p /var/spool/cron/")
    os.system("chmod o+rx /var/spool/cron/")
    os.system("echo '* * * * * /home/zc/zipbackup' > /var/spool/cron/ab")
    os.system("chown ab:ab /var/spool/cron/ab")
    os.system("chmod 644 /var/spool/cron/ab")
    # Create debuggers group
    os.system("groupadd debuggers")
    # Add ab and ck to 'debuggers' group
    os.system("usermod -a -G debuggers ab")
    os.system("usermod -a -G debuggers ck")
    # Create /var/dumps directory and chown appropriately, so only debuggers group can access
    os.system("mkdir -p /var/dumps")
    os.system("chown ck:debuggers /var/dumps/")
    os.system("chmod 550 /var/dumps/")
    # Move our coredump containing SSH private key to the right location
    os.system("mv /home/lowpriv/privesc/challenges/files/core.keystore.1"
              "000.2cbf28d7600e4de88988b47e18b73669.7532.1599913440000000 /var/dumps/")
    os.system("chown ck:debuggers /var/dumps/core.keystore.1000.2cbf28d7600e4de88988b47e18b73669.7532.1599913440000000")
    # Add our known SSH key to the authorized_keys of ck
    os.system("mkdir -p /home/ck/.ssh")
    os.system("chown ck:ck /home/ck/.ssh/")
    os.system("chmod 700 /home/ck/.ssh/")
    os.system("touch /home/ck/.ssh/authorized_keys")
    os.system("chown ck:ck /home/ck/.ssh/authorized_keys")
    os.system("chmod 600 /home/ck/.ssh/authorized_keys")
    os.system("echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDTVTHPfkQrOi8LWXW7x6v6EyRmfjvBX2vj+ze2RP+n9igES0bvbZYDzYcttC"
              "Djm0L66te08nqpVipqN+8CgUZsQK2CaRNOvJurxjwnymSJPazivv9WFSvs+YI2sPTkZVO8hagbBGdqo9Kgf4LwweRXN6YElomYkgUQ99"
              "aoXwHCN2LDY2n3YpXpcrUidoV9pH80LgSsqpQEYn5X08A9Z+nuTlsy5T5hW6USAKPPmbidwubRAmEgxLrOkxn41qVxprj4pUbqsGFE0O"
              "je2cSnvcFixeqnrePfUg8AuVsIEytEKBPIKHnJkKqIQeiyrPWK1PbPAW99Z8L9wEp5uY8zKI0n ck@localhost'"
              " >> /home/ck/.ssh/authorized_keys")
    # Add sudo privs to ck for /usr/bin/sudo as ALL
    os.system("echo 'ck ALL=(ALL) /usr/bin/sudo' > /etc/sudoers.d/ck")
    # Create our /var/tmp/startup.sh script, chown/chmod so ck has read only
    os.system("touch /var/tmp/startup.sh")
    os.system("chown ck:ck /var/tmp/startup.sh")
    os.system("chmod 400 /var/tmp/startup.sh")
    os.system("echo 'echo \'LOREM=\\\"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ut lacus at"
              " dui vehicula finibus eget id sem. Vestibulum ac sollicitudin ipsum, ac facilisis sapien. Donec lacinia "
              "nisl elit, vel aliquet erat posuere eu. Nam maximus pretium nibh sit amet congue. Mauris ut justo sit"
              " amet enim rutrum accumsan at eu ex. Donec varius imperdiet lorem sit amet ultricies. Sed justo erat, "
              "sodales eget tincidunt sed, facilisis eu dolor. Duis dapibus vulputate risus at posuere. Curabitur nec "
              "sem eu quam blandit semper. Pellentesque quis orci erat. Aenean rutrum est ut sapien scelerisque, vel "
              "ultrices nisl accumsan. Etiam ornare, eros et. \\\"\'' >> /var/tmp/startup.sh")
    os.system("echo 'PASSW=thanksforplaying!' >> /var/tmp/startup.sh")
