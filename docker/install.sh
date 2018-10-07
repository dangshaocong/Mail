#!/bin/bash

# docker pull mysql:5.7
# docker pull nginx
# docker pull redis:3.2
# docker pull delron/fastdfs
# docker pull delron/elasticsearch-ik:2.4.6-1.0


echo "MySQL"
docker run \
--name mall_mysql \
-p 3306:3306 \
-v $PWD/mysql/conf:/etc/mysql/conf.d \
-v $PWD/mysql/logs:/logs \
-v $PWD/mysql/data:/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=mysql \
-d mysql:5.7


echo "Nginx"
docker run \
--name mall_nginx \
-p 80:80 \
-v $PWD/../front_end:/www \
-v $PWD/nginx/conf/nginx.conf:/etc/nginx/nginx.conf \
-v $PWD/nginx/logs:/wwwlogs \
-d nginx


echo "Redis"
docker run \
--name mall_redis \
-p 6379:6379 \
-v $PWD/redis/data:/data \
-d redis:3.2 redis-server --appendonly yes




echo "FastDFS"
docker run \
--name mall_tracker \
--network=host \
-v $PWD/fastdfs/tracker:/var/fdfs \
-dti delron/fastdfs tracker

docker run \
--name mall_storage \
--network=host \
-e TRACKER_SERVER=`hostname -I |awk -F " " '{print $1}'`:22122 \
-v $PWD/fastdfs/storage:/var/fdfs \
-dti delron/fastdfs storage


echo "ElasticSearch"
docker run \
--name=mall_elasticsearch \
--network=host \
-v $PWD/elasticsearch/config:/usr/share/elasticsearch/config \
-dti delron/elasticsearch-ik:2.4.6-1.0

