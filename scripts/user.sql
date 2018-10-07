create database mall default charset=utf8;
create user mall identified by 'mall';
grant all on mall.* to 'mall'@'%';
flush privileges;
exit
EOF