#!/usr/bin/python3
#
#  Program scans your local LAN and provides a web page of the results
#
#  JJK 7.16.20 update
#

import urllib.request as urllib

from builtins import *

from scapy.all import *
#from scapy.all import conf as scapyconf
from socket import inet_aton,inet_ntoa
import struct
#import requests
import json
import codecs
import pprint
import getopt,sys

# Create dictionary  of my MAC Address to Descriptions (change this to match your system)
myMAC = {}
# Read file data to populate the dictionary
myMAC = {}
fpath = '/opt/scanlan/mac.txt'

MACcnt = 0
# Read the MAC address data
try:
   with open (fpath) as f:
      for line in f:
         # print('line = {0}' .format(line) )

         try:
            MACcnt += 1
            (key, val) = line.split(",")
            val = val.rstrip()
            # print('key={0} val={1}' .format(key, val) )
            myMAC[key]=[val]

         except ValueError:
            print('Bad Line - {0} in file {1}' .format(MACcnt, fpath) )

except IOError:
   print('File {0} not accessible' .format(fpath) )
#
#
print('Number of MAC addresses read in = {0}' .format(MACcnt) )

# disable scapy promiscuous mode (not sure this is needed)
# scapyconf.sniff_promisc = 0

# default to no company infomation being displayed
co = False

# MAC vendor API base url, you can also use https if you need
url = 'http://macvendors.co/api/'
mactest = ""

# Mac address to lookup vendor
def get_co(macaddr):
    request = urllib.Request(url+macaddr, headers={'User-Agent' : "API Browser"})
    response = urllib.urlopen( request )
    reader = codecs.getreader("utf-8")
    obj = json.load(reader(response))

    #print(obj['result']['company'])
    company = str(obj['result']['company'])
    #print company
    return company

# Convert dotted decimal IP to long - ex:ip2long('192.168.1.1'):
def ip2long(ip):
    packed = inet_aton(ip)
    lng = struct.unpack("!L", packed)[0]
    return lng

# Convert the long IP back into an dotted decimal IP:
def long2ip(lng):
    packed = struct.pack("!L", lng)
    ip=inet_ntoa(packed)
    return ip

# Write string to file
def write_string(my_str):
   mystrpath = './data.txt'
   try:
      with open (mystrpath,'w') as f2:
         f2.write(my_str)
      myret = 1

   except IOError:
      myret = 0

   f2.close
   return myret

def do_arping():
   global co
   my_list = []
   print("Processing...")

   # change this to match your subnet
   ans,unans = arping("192.168.1.0/24", verbose=0)

   # cnt = 0

   #print("----------------------------------------------------------------------------------------------")
   #print("MAC Address" + "\t\t" + "IP Address" + "\t" + "Description" )
   for s,r in ans:
      if co == True:
         try:
            #print('{0}\t{1}\t== {2}\t** {3}' .format( r[Ether].src,s[ARP].pdst,myMAC[r[Ether].src],get_co(r[Ether].src)) )
            my_list.append( (ip2long(s[ARP].pdst), r[Ether].src, myMAC[r[Ether].src], get_co(r[Ether].src)) )
         except KeyError:
            print('{0}\t{1}\t== MAC Address not found in MAC Table, Please add!' .format(r[Ether].src,s[ARP].pdst) )
      else:
         try:
            #print('{0}\t{1}\t== {2}' .format( r[Ether].src,s[ARP].pdst,myMAC[r[Ether].src] ) )
            my_list.append( (ip2long(s[ARP].pdst), r[Ether].src, myMAC[r[Ether].src]) )
         except KeyError:
            print('{0}\t{1}\t== MAC Address not found in MAC Table, Please add!' .format(r[Ether].src,s[ARP].pdst) )
      # cnt += 1

   # sort by IP address
   for aTuple in my_list:
      my_list.sort(key=lambda tup:tup[0])

   # convert long IP address to dotted decimal (done in above for loop)

   # print results
   # --------------------
   cnt = 0
   myString = ''
   print("----------------------------------------------------------------------------------------------")
   myString = "IP Address" + "," + "MAC Address" + "," + "Description\n" 

   for aTuple in my_list:
      if co == True:
         myString += '{0},{1},{2},{3}\n' .format(long2ip(aTuple[0]),aTuple[1],aTuple[2],aTuple[3])
      else:
         myString += ('{0},{1},{2}\n' .format(long2ip(aTuple[0]),aTuple[1],aTuple[2]) )

      cnt += 1
   print(myString)
   write_string(myString)
   print('{0} Hosts found!' .format(cnt) )

   #print('*******************************')
   return True


def usage():
   print ('scan_lan.py [ \n\
              -c|--company  -> adds MAC address Company info to output \n\
              -h|--help     -> prints this help info \n\
              -v|--version  -> print version number \n\
            ]')

def main(argv):

   global co

   try:
      opts, args = getopt.getopt(argv,'hcv',['help','company','version'])

   except getopt.GetoptError:
      print('Error!')
      usage()
      sys.exit(2)

   for opt, arg in opts:
      if opt in ('-h', '--help'):
         print('Help:')
         usage()
         sys.exit(2)

      elif opt in ('-c','--company'):
         print('Manufacturer company will be displayed')
         co = True

      elif opt in ('-v','--version'):
         print('Version 3.0')
         sys.exit(2)

      else:
         co = False

   do_arping()

if __name__ == "__main__":
   main(sys.argv[1:])
