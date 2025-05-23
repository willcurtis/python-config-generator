# Config Generator (Python Version)

This Python-based tool generates configuration files from a template and a CSV file containing tagged values.

---

## 🚀 Basic Usage (Local CLI)

```bash
python3 config_generator_with_zip.py -t template.txt -c data.csv -f thirdoctet -z
```

### Parameters

| Flag             | Description                                                  |
|------------------|--------------------------------------------------------------|
| `-t`, `--template` | Path to your template file (with tags like `[hostname]`)     |
| `-c`, `--csv`       | Path to your CSV file with matching headers                |
| `-f`, `--filename-column` | Column name (no brackets) to use as output file name |
| `-o`, `--output-dir` | (Optional) Output folder (default: `./configs`)           |
| `-z`, `--zip`       | (Optional) Zip the generated files                         |

---

## 🌐 Web App Version (`app.py`)

This version launches a simple web form that allows users to upload a template and CSV, then download a ZIP of generated configs.

### Run It

```bash
python3 app.py
```

Then visit: `http://localhost:3000`

---

## 🌍 Reverse Proxy Version (`app-proxy.py`)

This version allows embedding under an existing site like `https://yourdomain.com/tools/config-generator/`.

### 🔁 Apache Reverse Proxy Config

Add this to your Apache site config:

```apache
ProxyPreserveHost On
ProxyPass /tools/config-generator/ http://127.0.0.1:3000/tools/config-generator/
ProxyPassReverse /tools/config-generator/ http://127.0.0.1:3000/tools/config-generator/
```

Enable modules and restart:

```bash
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo systemctl restart apache2
```

---

### 🧭 Run app-proxy.py

```bash
cd /var/www/home <or wherever the file is located>
python3 app-proxy.py
```

App runs at port 3000 and will be accessible via:
```
https://yourdomain.com/tools/config-generator/
```

---

## 🛠️ systemd Service

This assumes that the app-proxy.py file is located in the web root and you are using a Python venv from your home directory

Create `/etc/systemd/system/config-generator.service`:

```ini
[Unit]
Description=Flask Config Generator Service
After=network.target

[Service]
User=<user>
Group=www-data
WorkingDirectory=/var/www/home
ExecStart=/home/<user>/myenv/bin/python app-proxy.py
Restart=always
PrivateTmp=true
NoNewPrivileges=true
ProtectSystem=full
ProtectHome=true
ProtectKernelTunables=true
ProtectControlGroups=true
ProtectKernelModules=true
RestrictAddressFamilies=AF_INET AF_UNIX
RestrictRealtime=true
ReadWritePaths=/var/www/home
Environment=PYTHONUNBUFFERED=1
Environment=FLASK_ENV=production

[Install]
WantedBy=multi-user.target
```

Enable and run:

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable config-generator
sudo systemctl start config-generator
```

---

## 🔁 Journald Log Rotation

Edit `/etc/systemd/journald.conf`:

```ini
SystemMaxUse=100M
SystemKeepFree=50M
SystemMaxFileSize=10M
SystemMaxFiles=10
```

Apply:

```bash
sudo systemctl restart systemd-journald
```

---

## 🧾 Optional: Log to File

Redirect output:

```ini
ExecStart=/home/<user>/myenv/bin/python app-proxy.py >> /var/log/config-generator.log 2>&1
```

Logrotate file `/etc/logrotate.d/config-generator`:

```bash
/var/log/config-generator.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
    create 640 <user> adm
}
```

---

## ✨ Author

Maintained by The Tech Shed. Styling, branding, and UI match the design of [thetechshed.dev](https://thetechshed.dev)
