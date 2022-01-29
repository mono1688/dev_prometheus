wget https://github.com/percona/mongodb_exporter/releases/download/v0.11.2/mongodb_exporter-0.11.2.linux-amd64.tar.gz -O /usr/local/src/mongodb_exporter.tar.gz
mkdir -p /opt/mongodb_exporter
tar zxvf /usr/local/src/mongodb_exporter.tar.gz -C /opt/mongodb_exporter
cat >/usr/lib/systemd/system/mongodb_exporter.service<<EOF
[Unit]
Description=mongodb_exporter
After=network.target
Documentation= https://github.com/percona/mongodb_exporter
[Service]
Type=simple
ExecStart=/opt/mongodb_exporter/mongodb_exporter --mongodb.uri=mongodb://172.17.0.1:27017
Restart=on-failure
[Install]
WantedBy=multi-user.target
EOF

systemctl start  mongodb_exporter.service && systemctl enable  mongodb_exporter.service
systemctl status  mongodb_exporter.service