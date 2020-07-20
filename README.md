
pip3 install -r requirements.txt

install.sh installs the script , sets permissions, installs systemd service file, and blank options file.

example prometheus job:

```
  - job_name: 'pi-htu21d'
    static_configs:
    - targets: ['10.23.45.3:8000']
      labels:
        name: pi
        device: htu21d

```

exports two metrics: temperature and relative_humidity
