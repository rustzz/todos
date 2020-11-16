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
User=root
WorkingDirectory=${myPATH}
ExecStart=/bin/bash ${myPATH}/scripts/run.sh
[Install]
WantedBy=multi-user.target"
SERVICEFILE="/etc/systemd/system/todos.service"
sudo su -c  "echo '${SERVICEDATA}' > ${SERVICEFILE}"
