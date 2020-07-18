#!/usr/bin/python3

# Run as: html-table.py
# The script requires file data.txt which is created by scan_lan3.py
# It expects a comma-separated input file to parse into an html table base web page.
# It assumes that the column headers are located in the first row.
# 

import sys
import time

infile = '/opt/scanlan/data.txt'
outfile = '/opt/scanlan/html-table.html'

# Process open of input file
try:
   with open(infile,'r') as filein:
      # read all the data from the input file
      data = filein.readlines()

except IOError:
   print('File {0} not accessible' .format(infile) )
   exit()
#
# Start creating the Output file data
# Create top of Page
table = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n'
table += '<html xmlns="http://www.w3.org/1999/xhtml">\n'
table += '<head>\n'
table += '<title>SCAN_LAN REPORT</title>\n'
# Create table CSS
table += '<style>\n'
table += 'table {\n'
table += '\ttable-layout: auto;\n'
table += '\twidth: 700px;\n'
table += '}\n'
table += '</style>\n'
table += '</head>\n'
# Start the Body
table += '<body>\n'
# Start the Table
table += "<table>\n"
# Create the table's column headers
header = data[0].split(",")
# Create all header row data
table += "  <tr>\n"
for column in header:
    table += "    <th>{0}</th>\n".format(column.strip())
table += "  </tr>\n"
# Create the table's row data
mycnt = 0
for line in data[1:]:
    mycnt += 1
    row = line.split(",")
    table += "  <tr>\n"
    for column in row:
        table += "    <td>{0}</td>\n".format(column.strip())
    table += "  </tr>\n"
table += "</table>\n"
# Show total number of MAC addresses found
table += '<br>\n'
table += '<b>Total MAC addesses found {0}</b>\n' .format(mycnt)

# Put in a Report date
localtime = time.asctime( time.localtime(time.time()) )

table += '<br>\n<br>\n'
table += '<b>{0}</b>\n' .format(localtime)
table += '</body>'

# Write output data to file!
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
