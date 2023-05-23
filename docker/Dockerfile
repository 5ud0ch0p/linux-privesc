# Build from OEL
FROM oraclelinux:8
# Create our standard login user creds (lowpriv:lowpriv)
RUN useradd -ms /bin/bash lowpriv -p '$1$FyHfpz/Q$gNjsHMDd3GsjPew.51zfq/'

# === SSH ===
# Install SSH
RUN yum install -y openssh-server openssh-clients
# Configure the SSH service, generate keys, etc.
RUN ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N ''
RUN ssh-keygen -t dsa -f /etc/ssh/ssh_host_dsa_key -N ''
RUN ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key -N ''
RUN ssh-keygen -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key -N ''
# Allow public-key authentication
RUN echo 'PubkeyAuthentication   yes' >> /etc/ssh/sshd_config 
# Daemonise sshd
#CMD ["/usr/sbin/sshd", "-D"]

# Expose the SSH port to the network
EXPOSE 22

# Install sudo, crontab, vim, less, netstat/ip to aid in challenges. File, which for usability
RUN yum install -y sudo cronie vim less net-tools file which gcc python3 telnet gdb bc tcpdump vsftpd ftp nc util-linux-user

# Copy over the practical configuration script, and set its permissions appropriately
COPY ./privesc/ /home/lowpriv/privesc/

# Prevent unintended privesc vectors for some challenges
RUN chmod 700 /home/lowpriv/privesc/challenges/files/logcleaner
RUN chmod 700 /home/lowpriv/privesc/challenges/files/usercounter
RUN chmod 700 /home/lowpriv/privesc/challenges/files/utils

# Install the python script requirements with pip
RUN pip3 install -r /home/lowpriv/privesc/requirements.txt

# Compile our wrapper for the privesc script, chmod it to suid. We need this as we cannot chmod scripts (i.e. those which start with #!)
RUN gcc /home/lowpriv/privesc/suid-wrapper/wrapper.c -o /home/lowpriv/config-privescs
RUN chmod u+s /home/lowpriv/config-privescs

RUN chmod 700 /home/lowpriv/privesc/service-starter/start.sh
CMD ["/home/lowpriv/privesc/service-starter/start.sh"]
