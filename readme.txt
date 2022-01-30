1.node为agent端用来监控主机,cd到node目录sh satrt_node.sh即可
其他mysql监控的需要修改配置文件的密码
mysql redis mongodb kafka 需要自行修改Prometheus配置文件
curl -X POST  http://172.17.0.1:9090/-/reload 重载Prometheus 


2.server为Prometheus服务端,cd到server目录sh start_server.sh.sh即可

3.动态添加node节点curl 127.0.0.1:9119/add_node?node=192.168.1.1(ip自行修改)
4.动态删除node节点curl 127.0.0.1:9119/delete_node?node=192.168.1.1(ip自行修改)

5.动态添加tcp节点curl 127.0.0.1:9119/add_tcp?node=192.168.1.1:8080(ip自行修改,一定要带端口)
6.动态删除tcp节点curl 127.0.0.1:9119/delete_tcp?node=192.168.1.1:8080(ip自行修改,一定要带端口)


