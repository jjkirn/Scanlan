#!/bin/bash

# BASH script to create a web page of the SCAN_LAN data
# You can create a cron job (crontab -e) and put this script (scan_lan.sh) on a 5 or 10 minute interval
# JJK 7/18/20
sudo /usr/bin/python3 /opt/scanlan/scan_lan3.py > /dev/null 2>&1
sudo /usr/bin/python3 /opt/scanlan/text_table.py > /dev/null 2>&1
sudo /bin/rm /var/www/html/index2.html > /dev/null 2>&1
sudo /bin/cp /opt/scanlan/html-table.html /var/www/html/index2.html > /dev/null 2>&1
