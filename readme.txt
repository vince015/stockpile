install:
python==3.6.1
mysql
redis

create database:
echo "create database stockpiledb;show databases" | mysql -uroot -proot

create logs folder:
mkdir logs