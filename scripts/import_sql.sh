#!/bin/bash
mysql -uroot -pmysql -h127.0.0.1 -P3306 < ./user.sql

python ../back_end
# 导入全国省市区数据
mysql -umall -pmall -h127.0.0.1 -P3306 mall < ./areas.sql

# 导入测试数据
mysql -umall -pmall -h127.0.0.1 -P3306 mall < ./goods_data.sql