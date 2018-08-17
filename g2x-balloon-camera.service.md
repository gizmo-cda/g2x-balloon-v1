[Unit]
Description=G2X Balloon Camera Service

[Service]
ExecStart=/usr/bin/python3 /home/pi/app/camera
WorkingDirectory=/home/pi/app
Restart=always
RestartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=g2x-balloon-service
#User=<alternate user>
#Group=<alternate group>

[Install]
WantedBy=multi-user.target