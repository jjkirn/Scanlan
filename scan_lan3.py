#!usr/bin/python3
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
import time

myMAC = {}	## Global empty dictionary
version = "3.3"
subnet = "192.168.1.0/24"  ## subnet to scan - change this to match your subnet

# Create a dictionary of my MAC Address to Descriptions
# Read MAC address supplementary data file (mac.txt) to populate the dictionary (change mac.txt to match your system)
# Format of the file is MACaddress, Detail supplementary info for that MAC, optional company
def read_mac_file(fpath):
	cnt = 1

	# print('fpath = {}'.format(fpath))	## Debug

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

	print('{0} MAC addresses read in from detail data File ({1})' .format(cnt, fpath) )

	# disable scapy promiscuous mode (not sure this is needed)
	# scapyconf.sniff_promisc = 0

	return(True)

# Mac address to vendor (company) lookup - REF: https://www.youtube.com/watch?v=nhC3paE_YPk -> vendor=company
def get_co(macaddr):
	# print('macaddr: {}'.format(macaddr))  ## Debug

	# MAC vendor API base url, you can also use https if you need
	#url = f'http://www.macvendorlookup.com/api/v2/{macaddr}'   ## kept timing out 502 error - I think they have daily limits
	url = f'https://api.maclookup.app/v2/macs/{macaddr}'  ## this site is rate limited, doesnt look like daily limits

	# print('Request: {}'.format(url)) ## Debug

	try:
		# rate limited, try 1 sec, for site https://api.maclookup.app/
		time.sleep(1) # Wait for 1 sec

		r = requests.get(url, timeout=(2)).json()
		# print('r = {}'.format(r))  ## Debug

		# Below is dependent on the values (JSON) returned from the url. If you change the url, you may need to change the below
		company = r['company']
		# print('company = {}'.format(company)) ## Debug

		if company == '':
			company = 'none found'

		if r['success'] == False:
			print('Site is rate limiting - Too Many Requests: {}'.format(url) )

	except requests.exceptions.Timeout:
		print('HTTP Connection Error to site {} timed out'.format(url))
		company = 'none'

	# except requests.exceptions.ConnectionError as errh:
	except requests.exceptions.ConnectionError:
		print('HTTP Connection Error to site {} timed out'.format(url))
		company = 'none'

	# print("company = {}".format(company)) ## Debug
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

# Use arping to collect all tha MAC addresses on the LAN
def do_arping(co):

	my_list = []
	print("Processing...")

	# change this to match your subnet
	mysub = subnet
	ans,unans = arping(mysub, verbose=0, timeout=15)

	cnt = 1

	# append data from arping to my_list
	for s,r in ans:

		if co == True:
			print('Getting company information from site for item {}'.format(cnt))
			try:
				#print('{0}\t{1}\t== {2}\t** {3}' .format( r[Ether].src,s[ARP].pdst,myMAC[r[Ether].src],get_co(r[Ether].src)) )
				my_list.append( (ip2long(s[ARP].pdst), r[Ether].src, myMAC[r[Ether].src], get_co(r[Ether].src)) )
				# below is a debug print
				# print('{}, {}, {}, {}'.format(ip2long(s[ARP].pdst), r[Ether].src, myMAC[r[Ether].src], get_co(r[Ether].src)))

			except KeyError:
				print('{0}\t{1}\t== MAC Address not found in MAC Table, Please add!' .format(r[Ether].src,s[ARP].pdst) )
		else:
			try:
				#print('{0}\t{1}\t== {2}' .format( r[Ether].src,s[ARP].pdst,myMAC[r[Ether].src] ) )
				my_list.append( (ip2long(s[ARP].pdst), r[Ether].src, myMAC[r[Ether].src]) )

			except KeyError:
				print('{0}\t{1}\t== MAC Address not found in MAC Table, Please add!' .format(r[Ether].src,s[ARP].pdst) )
		cnt += 1

   	# sort my_list by IP address
	for aTuple in my_list:
		my_list.sort(key=lambda tup:tup[0])

	# convert long IP address to dotted decimal (done in above for loop)

	# print my_list sorted results
	cnt = 0
	myString = ''
	print("----------------------------------------------------------------------------------------------")

	# Print the column headers
	t1 = "IP Address"
	t2 = "MAC Address"
	t3 = "Description"
	t4 = "Company"

	if co == True:
		myString = "IP Address" + "," + "MAC Address" + "," + "Description" + "," + "Company\n"
	else:
		myString = "IP Address" + "," + "MAC Address" + "," + "Description\n"

	# print the row data
	for aTuple in my_list:
		if co == True:
			myString += ('{0},{1},{2},{3}\n' .format(long2ip(aTuple[0]),aTuple[1],aTuple[2],aTuple[3].replace(',', '')) )
		else:
			myString += ('{0},{1},{2}\n' .format(long2ip(aTuple[0]),aTuple[1],aTuple[2]) )

		cnt += 1

	print(myString)
	# Write data to file in comma seperated format
	write_string(myString)
	print('{0} Hosts found!' .format(cnt) )

	#print('*******************************')  ## Debug
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
	print('Wrote data to file: {}'.format(mystrpath))
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
			print('Version {}'.format(version))
			sys.exit(2)

	read_mac_file(fpath)
	do_arping(co)

if __name__ == "__main__":
	main(sys.argv[1:])
