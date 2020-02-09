# Scanlan
Python3 program to scan your LAN and provide details about each MAC address found.

Must run this program as root (Linux) or administrator (Windows). For Linux run:
$ sudo python3 scan_lan2.py

The program assumes you create a text file (mac.txt) which contains detail information about each of your MAC addresses on your LAN.
You can run the program without this file to find all your MAC addresses, then place this list into the file (mac.txt) and add additional 
supplemental data for each MAC by seperating the MAC address data from the supplental data. Over time, you may have more MAC address data
in the file (mac.txt) as the program only finds those addresses that are active at the time the program is run.

The file text_table.py together with a modified version of scan_lan2.py -> scan_lan3.py produce a an output file "html-table.html".
That file can easily be copied over to an web server and will display data similar to that shown from command line via scan_lan2.py
