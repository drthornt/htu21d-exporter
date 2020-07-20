#!/bin/sh -x

# copy files into place
cp ./systemd/htu21d-exporter.service /lib/systemd/system/htu21d-exporter.service
cp ./htu21d-exporter.py  /usr/bin/htu21d-exporter.py

chown root:root /usr/bin/htu21d-exporter.py
chmod 755       /usr/bin/htu21d-exporter.py

echo "OPTIONS=\"\"" > /etc/default/htu21d_exporter

# reatart services

systemctl daemon-reload
