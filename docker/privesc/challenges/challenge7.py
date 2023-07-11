import os


def configurelevel1():
    # Create highpriv and configure with a password ("YouShouldn'tNeedThis!")
    os.system("useradd -ms /bin/bash highpriv -p '$6$XX8bQeKYZJrg/czP$tmcMf6bVXnNHdh.Ccoe8ROxhsISUTO"
              "JAbllLqgOWLggeTqcoO0Ke8VICAZzW5aeK4ZI2H2XV4cHNw7eQFkpp2/'")
    # Create our cron file directory
    os.system("mkdir -p /var/spool/cron/")
    # Create relevant crontab file for highpriv, chown appropriately, and weaken permissions
    os.system("echo '* * * * * /tmp/jobs/cleanup' > /var/spool/cron/highpriv")
    os.system("chown highpriv:highpriv /var/spool/cron/highpriv")
    os.system("chmod 644 /var/spool/cron/highpriv")
    # Create a location to require our initial privesc to achieve privesc to root
    os.system("mkdir -p /srv/logs")
    os.system("chown highpriv:highpriv /srv/logs")
    os.system("chmod 700 /srv/logs")
    # Create relevant crontab file for root, chmod appropriately, and create "backup" for attendees to find
    os.system("echo '* * * * * /srv/logs/backup_logs.sh' > /var/spool/cron/root")
    os.system("chmod 600 /var/spool/cron/root")
    os.system("cp /var/spool/cron/root /srv/logs/root_crontab")
    # Make our "backup" crontab readable by our intermediary user
    os.system("chown highpriv:highpriv /srv/logs/root_crontab")
    os.system("chmod 400 /srv/logs/root_crontab")
    # Make /var/spool/cron readable to give attendees a chance at this difficulty
    os.system("chmod o+rx /var/spool/cron/")


def configurelevel2():
    # Change the 'root' password to our desired value ('n0pn0pn0pjmp')
    os.system("echo 'n0pn0pn0pjmp' | passwd --stdin root 2>&1 >/dev/null")
    # Provide tcpdump access to lowpriv
    os.system("echo 'lowpriv ALL=(root) /usr/sbin/tcpdump' > /etc/sudoers.d/lowpriv")
    # Run an FTP server for us to authenticate against
    os.system("vsftpd")
    # Set up a cronjob to authenticate to our mock service on local loopback - "login" runs once every minute
    os.system("mkdir -p /var/spool/cron/")
    os.system("echo '* * * * * (sleep 2; echo -e \"USER admin\"; sleep 1; echo -e \"PASS n0pn0pn0pjmp\") |"
              " nc localhost 21' > /var/spool/cron/root")
    os.system("chmod 600 /var/spool/cron/root")


def configurelevel3():
    #
    # Create our 'hint' file
    os.system("echo 'Our devices are all monitored for suspicious activity.' >> /home/lowpriv/warning.txt")
    os.system("echo 'Do not try and interfere with this process.' >> /home/lowpriv/warning.txt")
    os.system("echo 'We regularly retrieve the script from a trusted source, so do not even try!'"
              " >> /home/lowpriv/warning.txt")
    # Create our first cron job, which overwrites the /etc/hosts file every minute with a
    # file from a world-writeable location. This directory should be identifiable using find -perm.
    os.system("mkdir -p /var/reset")
    os.system("chmod 777 /var/reset")
    os.system("echo '192.168.13.37 scriptrepo' >> /etc/hosts")
    os.system("cp /etc/hosts /var/reset/hosts")
    os.system("echo '*/2 * * * * cp /var/reset/hosts /etc/hosts' > /var/spool/cron/root")
    os.system("chmod 600 /var/spool/cron/root")
    # Create our second cron job, which pulls a script from a location controllable via the first cron job and pipes it
    # straight to bash as root
    os.system("echo '* * * * * curl http://scriptrepo:1337/monitor.sh | bash' >> /var/spool/cron/root")
