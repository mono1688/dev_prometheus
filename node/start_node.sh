wget https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz -O /usr/local/src/node_exporter.tar.gz
mkdir -p /opt/node_exporter
tar zxvf /usr/local/src/node_exporter.tar.gz -C /opt/node_exporter

mv /opt/node_exporter/node_exporter-1.3.1.linux-amd64/node_exporter  /opt/node_exporter/node_exporter
rm -rf /opt/node_exporter/node_exporter-1.3.1.linux-amd64
cat >/usr/lib/systemd/system/node_exporter.service<<EOF
[Unit]
Description=node_exporter
After=network.target
Documentation= https://github.com/prometheus/node_exporter/
[Service]
Type=simple
ExecStart=/opt/node_exporter/node_exporter
Restart=on-failure
[Install]
WantedBy=multi-user.target
EOF

systemctl start  node_exporter.service && systemctl enable  node_exporter.service
systemctl status  node_exporter.service