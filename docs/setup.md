# [Setup Service](#setup-service)

---

# Setup Service

Run the following to initialize the service and make it start automatically when the system boots:

```bash
cd /etc/systemd/system
sudo chmod 755 g2x-camera.service
sudo systemctl enable g2x-camera
```

You can start/stop/restart the service using the following commands:

```bash
sudo systemctl start g2x-camera
sudo systemctl stop g2x-camera
sudo systemctl restart g2x-camera
```

If you make changes to the service file, you will need to reload the service daemon and restart the service

```bash
sudo systemctl daemon-reload
sudo systemctl restart g2x-camera
```

You can check the status of your service:

```bash
systemctl status g2x-camera
```
