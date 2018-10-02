docker pull mysql:5.7

mkdir -p /docker/mysql/data
mkdir -p /docker/mysql/logs
mkdir -p /docker/mysql/conf
# data目录将映射为mysql容器配置的数据文件存放路径
# logs目录将映射为mysql容器的日志目录
# conf目录里的配置文件将映射为mysql容器的配置文件

docker run -p 3306:3306 --name mall_mysql -v /docker/mysql/conf:/etc/mysql/conf.d -v /docker/mysql/logs:/logs -v /docker/mysql/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7

mysql -uroot -p123456 -h127.0.0.1 -P3306
create database mall default charset=utf8;
create user mall identified by 'mall';
grant all on mall.* to 'mall'@'%';
flush privileges;

################################################################
docker pull nginx
mkdir -p /docker/nginx/www
mkdir -p /docker/nginx/logs
mkdir -p /docker/nginx/conf
# www: 目录将映射为 nginx 容器配置的虚拟目录。
# logs: 目录将映射为 nginx 容器的日志目录。
# conf: 目录里的配置文件将映射为 nginx 容器的配置文件。

docker run -p 80:8888 --name mall_nginx -v /docker/nginx/www:/www -v /docker/nginx/nginx/nginx.conf:/etc/nginx/nginx.conf -v /docker/nginx/logs/wwwlogs -d nginx

-p 80:80：将容器的80端口映射到主机的80端口
-v $PWD/www:/www：将主机中当前目录下的www挂载到容器的/www
-v $PWD/conf/nginx.conf:/etc/nginx/nginx.conf：将主机中当前目录下的nginx.conf挂载到容器的/etc/nginx/nginx.conf
-v $PWD/logs:/wwwlogs：将主机中当前目录下的logs挂载到容器的/wwwlogs


################################################################
docker pull redis:3.2
mkdir -p /docker/redis/data
# data 目录将映射为redis容器配置的/data目录,作为redis数据持久化的存储目录

docker run -p 6379:6379 --name mall_redis -v /docker/redis/data:/data  -d redis:3.2 redis-server --appendonly yes
# -p 6379:6379 : 将容器的6379端口映射到主机的6379端口
# -v /docker/redis/data:/data : 将主机中当前目录下的data挂载到容器的/data
# redis-server --appendonly yes : 在容器执行redis-server启动命令，并打开redis持久化配置


##############################################################

docker run -dti --network=host --name tracker -v /var/fdfs/tracker:/var/fdfs delron/fastdfs tracker

docker run -dti --network=host --name storage -e TRACKER_SERVER=10.211.55.5:22122 -v /var/fdfs/storage:/var/fdfs delron/fastdfs storage
