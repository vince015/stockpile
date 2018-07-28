#!/bin/bash

#write out current crontab
crontab -l > backupcron
#echo new cron into cron file
echo "0 13 * * * /home/matthew/src/stockpile/scripts/backup.sh" >> backupcron
#install new cron file
crontab backupcron
rm backupcron