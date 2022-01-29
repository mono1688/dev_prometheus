wget https://github.com/danielqsj/kafka_exporter/releases/download/v1.2.0/kafka_exporter-1.2.0.linux-amd64.tar.gz -O /usr/local/src/kafka_exporter.tar.gz
mkdir -p /opt/kafka_exporter
tar zxvf /usr/local/src/kafka_exporter.tar.gz -C /opt/kafka_exporter

mv /opt/kafka_exporter/kafka_exporter-1.2.0.linux-amd64/kafka_exporter  /opt/kafka_exporter/kafka_exporter
rm -rf /opt/kafka_exporter/kafka_exporter-1.2.0.linux-amd64
cat >/usr/lib/systemd/system/kafka_exporter.service<<EOF
[Unit]
Description=kafka_exporter
After=network.target
Documentation= https://github.com/danielqsj/kafka_exporter
[Service]
Type=simple
ExecStart=/opt/kafka_exporter/kafka_exporter --kafka.server=127.0.0.1:9092 --kafka.version=1.1.0 --log.level=info
Restart=on-failure
[Install]
WantedBy=multi-user.target
EOF

systemctl start  kafka_exporter.service && systemctl enable  kafka_exporter.service
systemctl status  kafka_exporter.service