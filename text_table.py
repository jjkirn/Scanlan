#!/usr/bin/python3

# Run as: python3 html-table.py
# The script requires file 'data.txt' which is created by 'scan_lan3.py'
# It expects a comma-separated input file (data.txt) which it parses into a html web page file (html-table.html).
# It assumes that the column headers are located in the first row of the 'data.txt' file.
# General web page formating from example: https://www.geeksforgeeks.org/how-to-fix-the-width-of-columns-in-the-table/

import sys
import time

infile = '/dev/shm/data.txt'
outfile = '/dev/shm/html-table.html'

# Process opening of input file (data.txt)
try:
   with open(infile,'r') as filein:
      # read all the data from the input file
      data = filein.readlines()

except IOError:
   print('File {0} not accessible' .format(infile) )
   exit()
#
# Start creating the HTML Output file data (html-table.html)
## Create top of Page
table = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n'
table += '<html xmlns="http://www.w3.org/1999/xhtml">\n'
table += '<title>SCAN_LAN REPORT</title>\n'

## Create table CSS
table += '<head>\n'
table += '\t<style>\n'
table += '\t\ttable {\n'
table += '\t\t\tmargin=left: auto;\n'
table += '\t\t\tmargin=right: auto;\n'
table += '\t\t\tfont-size: 20px;\n'
table += '\t\t\theight: 100%;\n'
table += '\t\t\ttable-layout: fixed;\n'
table += '\t\t}\n'
#
table += '\t\ttd {\n'
table += '\t\t\tborder: 1px solid black;\n'
table += '\t\t\ttext-align: center;\n'
table += '\t\t\tpadding: 10px;\n'
table += '\t\t}\n'
#
table += '\t\ttr:nth-child(even) {\n'
table += '\t\t\tbackground-color: #00cf45;\n'
table += '\t\t}\n'
# 
table += '\t\th1 {\n'
table += '\t\t\tcolor: green;\n'
table += '\t\t}\n'
#
table += '\t</style>\n'
table += '</head>\n'

## Start the Body
table += '<body>\n'
table += '\t<center>\n'
table += '\t\t<h1>ScanLan Report</h1>\n'

## Put in a Report date+time
localtime = time.asctime( time.localtime(time.time()) )
table += '\t\t<h2>{0}\n'.format(localtime)
table += '\t\t</h2>\n'

## Start the Table
table += "\t\t<table>\n"
## Create the table's column headers
header = data[0].split(",")

## Create the header row data
table += "\t\t\t<tr>\n"
for column in header:
    table += "\t\t\t\t<td>{0}</td>\n".format(column.strip())
table += "\t\t\t</tr>\n"

## Create the table's row data
mycnt = 0
for line in data[1:]:
    mycnt += 1
    row = line.split(",")
    table += "\t\t\t<tr>\n"
    for column in row:
        table += "\t\t\t\t<td>{0}</td>\n".format(column.strip())
    table += "\t\t\t</tr>\n"
table += "\t\t</table>\n"
table += "\t</center>\n"
table += '</body>\n'

## Show total number of MAC addresses found, end the html
table += '<br>\n'
table += '<b>Total MAC addesses found {0}</b>\n' .format(mycnt)
table += '</html>'

## Write output data to webpage file (html-table.html)!
try:
   with open (outfile,'w') as fileout:
      fileout.writelines(table)

except IOError:
   print('File {0} not accessible' .format(outfile) )
   filein.close()
   exit()

# Normal Exit
fileout.close()
filein.close()
