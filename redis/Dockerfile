FROM redis

RUN echo 'vm.overcommit_memory = 1' >> /etc/sysctl.conf
ADD rc.local /etc/