# Installation

Change `${INSTALL_URL}` in `watchdawg.service` to the installation path.

```sh
sudo cp watchdawg.service /lib/systemd/system/watchdawg.service
sudo chmod 644 /lib/systemd/system/watchdawg.service
sudo systemctl daemon-reload
sudo systemctl enable watchdawg.service
sudo systemctl start watchdawg.service
```

# Logs

```sh
sudo journalctl -f -u watchdawg.service
```
