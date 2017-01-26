#!/usr/bin/python

"""
Output lines selected randomly from a file

Copyright 2005, 2007 Paul Eggert.
Copyright 2010 Darrell Benjamin Carbajal.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Please see <http://www.gnu.org/licenses/> for a copy of the license.

$Id: randline.py,v 1.4 2010/04/05 20:04:43 eggert Exp $
"""

import random, sys
from optparse import OptionParser

class comm:
	def __init__(self, filename1, filename2, options):
		self.options = options
		if filename1 == "-":
			#Read from stdin
			self.lines1 = sys.stdin.readlines()
		else:
			#Open the file and make a list of its lines
			f1 = open(filename1, 'r')
			self.lines1 = f1.readlines()
			f1.close()
		if filename2 == "-":
			self.lines2 = sys.stdin.readlines()
		else:
			f2 = open(filename2, 'r')
			self.lines2 = f2.readlines()
			f2.close()
		self.numlines1 = len(self.lines1)
		self.numlines2 = len(self.lines2)
		#Make a list of booleans that will indicate whether we find duplicates of the lines in file 2
		self.f2dups = []
		for i in range(self.numlines2):
			self.f2dups.append(False)


	#Check if the user chose the option to suppress a column before printing a line
	def printText(self, string, col):
		text = ""
		if col == 1:
			if self.options.hideCol1 == False:
				sys.stdout.write(string)
		elif col == 2:
			if self.options.hideCol2 == False:
				text = "\t"+string
				sys.stdout.write(text)
		elif col == 3:
			if self.options.hideCol3 == False:
				text = "\t\t"+string
				sys.stdout.write(text)


	#If -u option wasn't selected, then compare the two sorted files
	def cmpSorted(self):	
		i = 0
		j = 0
		#Iterate through both lists and look for common lines
		while i < self.numlines1 and j < self.numlines2:
			if self.lines1[i] == self.lines2[j]:
				self.printText(self.lines1[i], 3)
				i = i + 1
				j = j + 1
			elif self.lines1[i] < self.lines2[j]:
				self.printText(self.lines1[i], 1)
				i = i + 1
			elif self.lines1[i] > self.lines2[j]:
				self.printText(self.lines2[j], 2)
				j = j + 1
		#If we didn't finish iterating through file 1's list, then print the remaining lines
		if i < self.numlines1:
			while i < self.numlines1:
				self.printText(self.lines1[i], 1)
				i = i + 1
		#If we didn't finish iterating through file 2's list, then print the remaining lines
		elif j < self.numlines2:
			while j < self.numlines2:
				self.printText(self.lines2[j], 2)
				j = j + 1	


	#If the -u option was selected, then compare the two unsorted files
	def cmpUnsorted(self):
		#Compare every line in file 1 with every line in file 2
		for i in range(self.numlines1):
			#Declare a boolean to indicate whether a line in file 1 is also in file 2
			foundDup = False
			for j in range(self.numlines2):
				if self.lines1[i] == self.lines2[j]:
					#A line in file 1 was also found in file 2
					self.printText(self.lines1[i], 3)
					#Modify the list of booleans to indicate #a line in file 2 was in file 1 as well
					self.f2dups[j] = True
					foundDup = True
					break
			if foundDup == False:
				#A line in file 1 was never found in file 2
				self.printText(self.lines1[i], 1)
		#Loop through list of booleans to find all  the lines in file 2 that #were also in file 1
		for k in range(len(self.f2dups)):
			if self.f2dups[k] == False:
				self.printText(self.lines2[k], 2)


def main():
	version_msg = "%prog 2.0"
	usage_msg = """%prog [OPTION]... FILE1 FILE2

Compare FILE1 and FILE2 line by line."""

	parser = OptionParser(version=version_msg,
		usage=usage_msg)
	parser.add_option("-u",
			action="store_true", dest="unsorted", default=False,
			help="Use -u to compare unsorted files (default = sorted)")
	parser.add_option("-1", action="store_true", dest="hideCol1", default=False, help="Use -1 to hide output of column 1")
	parser.add_option("-2", action="store_true", dest="hideCol2", default=False, help="Use -2 to hide output of column 2")
	parser.add_option("-3", action="store_true", dest="hideCol3", default=False, help="Use -3 to hide output of column 3")
	options, args = parser.parse_args(sys.argv[1:])

	#Write error message if comm.py doesn't get exactly two operands
	if len(args) != 2:
		parser.error("Wrong number of operands")

	c = comm(args[0], args[1], options)
	#If -u was added, then run the compare function for unsorted files
	if options.unsorted == True:
		c.cmpUnsorted()
	#-u was not added so run the compare function for sorted files
	else:
		c.cmpSorted()


if __name__ == "__main__":
	main()
