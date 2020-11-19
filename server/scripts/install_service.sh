#!/bin/bash
myPATH=`pwd`
SERVICEDATA="[Unit]
Description=API
After=network.target
StartLimitIntervalSec=0
[Service]
Type=simple
Restart=always
RestartSec=1
User=${whoami}
WorkingDirectory=${myPATH}
ExecStart=/bin/bash ${myPATH}/scripts/run.sh
[Install]
WantedBy=multi-user.target"
SERVICEFILE="todos.service"

sudo su -c "echo '${SERVICEDATA}' > /etc/systemd/system/${SERVICEFILE}"
sudo su -c "systemctl enable ${SERVICEFILE};systemctl start ${SERVICEFILE}"
