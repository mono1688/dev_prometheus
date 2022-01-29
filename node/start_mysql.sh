wget https://github.com/prometheus/mysqld_exporter/releases/download/v0.13.0/mysqld_exporter-0.13.0.linux-amd64.tar.gz -O /usr/local/src/mysqld_exporter.tar.gz
mkdir -p /opt/mysqld_exporter
tar zxvf /usr/local/src/mysqld_exporter.tar.gz -C /opt/mysqld_exporter

mv /opt/mysqld_exporter/mysqld_exporter-0.13.0.linux-amd64/mysqld_exporter  /opt/mysqld_exporter/mysqld_exporter
rm -rf /opt/mysqld_exporter/mysqld_exporter-0.13.0.linux-amd64

cat >/opt/mysqld_exporter/.my.cnf<<EOF

[client]
host=127.0.0.1
port=3306
user=exporter
password=123456
EOF



cat >/usr/lib/systemd/system/mysqld_exporter.service<<EOF
[Unit]
Description=mysqld_exporter
After=network.target
Documentation= https://github.com/prometheus/mysqld_exporter
[Service]
Type=simple
ExecStart=/opt/mysqld_exporter/mysqld_exporter  --config.my-cnf=/opt/mysqld_exporter/.my.cnf
Restart=on-failure
[Install]
WantedBy=multi-user.target
EOF

systemctl start  mysqld_exporter.service && systemctl enable  mysqld_exporter.service
systemctl status  mysqld_exporter.service