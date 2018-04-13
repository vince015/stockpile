# install redis
https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-redis-on-ubuntu-16-04

# install dependecies
sudo apt-get install mysql-server  -y
sudo apt-get install libmysqlclient-dev python3.6-dev -y
sudo apt-get install virtualenv -y

# prepare env
virtualenv env --python /usr/bin/python3.6
source env/bin/activate
pip install -r requirements.txt
mkdir logs

# check if working
python manage.py showmigrations