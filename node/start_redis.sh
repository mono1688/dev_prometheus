wget https://github.com/oliver006/redis_exporter/releases/download/v1.32.0/redis_exporter-v1.32.0.linux-amd64.tar.gz -O /usr/local/src/redis_exporter.tar.gz
mkdir -p /opt/redis_exporter
tar zxvf /usr/local/src/redis_exporter.tar.gz -C /opt/redis_exporter

mv /opt/redis_exporter/redis_exporter-v1.32.0.linux-amd64/redis_exporter  /opt/redis_exporter/redis_exporter
rm -rf /opt/redis_exporter/redis_exporter-v1.32.0.linux-amd64
cat >/usr/lib/systemd/system/redis_exporter.service<<EOF
[Unit]
Description=redis_exporter
After=network.target
Documentation= https://github.com/oliver006/redis_exporter
[Service]
Type=simple
ExecStart=/opt/redis_exporter/redis_exporter -redis.addr 127.0.0.1:6379
Restart=on-failure
[Install]
WantedBy=multi-user.target
EOF

systemctl start  redis_exporter.service && systemctl enable  redis_exporter.service
systemctl status  redis_exporter.service