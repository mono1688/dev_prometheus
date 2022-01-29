#!/bin/bash
docker_stats=`docker --version`

if [ $? != 0 ]
then
  sudo yum install -y yum-utils device-mapper-persistent-data lvm2
  sudo yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
  sudo yum makecache fast
  sudo yum list docker-ce --showduplicates | sort -r
  sudo yum install -y docker-ce-19.03.9-3.el7
  sudo systemctl enable docker && sudo systemctl start  docker
fi

echo $docker_stats


docker_compose_stats=`docker-compose --version`


if [ $? != 0 ]
then
  sudo curl -L "https://github.com/docker/compose/releases/download/v2.2.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
  sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
fi

echo $docker_compose_stats


is_running=`docker ps|grep prometheus|awk '{print $1}'|wc -L`

if [ $is_running != 0 ]
then
    down_cotainer=`docker-compose -f docker-compose.yml down`
fi


current_path=`pwd`

FIND_FILE=$current_path"/telegram_warn/Dockerfile"
FIND_STR="xxx"

if [ `grep -c "$FIND_STR" $FIND_FILE` -ne '0' ];then
    echo "must edit "$FIND_FILE" CHATID and TOKEN value"
    exit 0
fi

cd $current_path/telegram_warn && docker build -t telegram-warn .
cd $current_path && docker-compose -f docker-compose.yml  up -d

