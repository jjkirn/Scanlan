#!/usr/bin/python3
#
# JJKirn 2/8/2020, updated 6/1/2024
#

from builtins import *
from scapy.all import *
from socket import inet_aton,inet_ntoa
import struct
import json
import codecs
import getopt,sys
import requests

myMAC = {}

# Create dictionary  of my MAC Address to Descriptions (change this to match your system)
#
# Read MAC address supplementary data file (mac.txt) to populate the dictionary
# Format of file is MACaddress,Detail supplementary info for that MAC, optional company 

def read_mac_file(fpath):
	cnt = 1

	# print('fpath = {}'.format(fpath))

	try:
		with open (fpath) as f:
			for line in f:
				# print('line = {0}' .format(line) )

				try:
					(key, val) = line.split(",")
					val = val.rstrip()
					# print('key={0} val={1}' .format(key, val) )
					myMAC[key]=[val]

				except ValueError:
					print('MAC address local detail data File ({0}) - Bad Line - {1}' .format(fpath, cnt) )
				
				cnt = cnt + 1
				
	except IOError:
		print('File {0} not accessible' .format(fpath) )

	#
	print('{0} MAC addresses read in from detail data File ({1})' .format(cnt, fpath) )

	# disable scapy promiscuous mode (not sure this is needed)
	# scapyconf.sniff_promisc = 0

	return(True)

# Mac address to lookup vendor - REF: https://www.youtube.com/watch?v=nhC3paE_YPk,  vendor=company
def get_co(macaddr):
	# print('macaddr: {}'.format(macaddr))

	# MAC vendor API base url, you can also use https if you need
	url = f'https://www.macvendorlookup.com/api/v2/{macaddr}'
	
	# print('Request: {}'.format(url))
	
	try:
		vendor = requests.get(url).json()
		vendor = vendor[0]['company']
		
	except:
		vendor = 'none'

	# print("vendor = {}".format(vendor))
	
	return vendor

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

# Use arping to collect all tha MAC addresses on the LAN
def do_arping(co):
	
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
	cnt = 0
	myString = ''
	print("----------------------------------------------------------------------------------------------")
	# Print the column headers
	if co == True:
		myString = "IP Address" + "," + "MAC Address" + "," + "Description" + "," + "** Company Info\n"
	else:
		myString = "IP Address" + "," + "MAC Address" + "," + "Description\n"

	# Print the row data
	for aTuple in my_list:
		if co == True:
			myString += ('{0},{1},{2},{3}\n' .format(long2ip(aTuple[0]),aTuple[1],aTuple[2],aTuple[3]) )
		else:
			myString += ('{0},{1},{2}\n' .format(long2ip(aTuple[0]),aTuple[1],aTuple[2]) )

		cnt += 1
	print(myString)
	write_string(myString)
	print('{0} Hosts found!' .format(cnt) )

	#print('*******************************')
	return True

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

def usage():
	print ('scan_lan.py [ \n\
		-c|--company  -> adds MAC address Company info to output \n\
		-h|--help     -> prints this help info \n\
		-v|--version  -> print version number \n\
	]')

def main(argv):
	co = False
	fpath = 'mac.txt'
	
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

		if opt in ('-c','--company'):
			print('Manufacturer company will be displayed')
			co = True

		if opt in ('-v','--version'):
			print('Version 3.1')
			sys.exit(2)

	read_mac_file(fpath)
	do_arping(co)

if __name__ == "__main__":
	main(sys.argv[1:])
