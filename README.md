# Scanlan
Python3 program to scan you LAN and allow you to map your MAC address to stored data

Must run this program as root (Linux) or administrator (Windows). For Linux run:
$ sudo python3 scan_lan2.py

The program assumes you create a text file (mac.txt) which contains detail information about each of your MAC addresses on your LAN.
You can run the program without this file to find all your MAC addresses, then place this list into the file (mac.txt) and add additional 
supplemental data for each MAC by seperating the MAC address data from the supplental data. Over time, you may have more MAC address data
in the file (mac.txt) as the program only finds those addresses that are active at the time the program is run.
