#!/bin/bash
# pflint Tue 19 Feb 2013 07:46:49 AM EST 
# pbug debug environment
# sudo bash
# sudo ~flint/bin/fdbg.sh
# Make sure only root can run our script
# sudo cd /var/www/furmon
sudo cd /var/www/furmon
# cd /var/www/furmon
chmod 777 ~/.screenrc
# echo "Welcome to fdbg.sh"; sleep 1s
cp /home/flint/furmon/bin/fdbg.screen ~/.screenrc
sudo screen

