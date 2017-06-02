#!/usr/bin/env python
import re
import getopt
import subprocess
import sys

def main( argv = None ):
        if argv == None:
		print 'resizeXfsPartition.py /dev/sda'
		sys.exit()
	try:
		opts, args = getopt.getopt(argv,"h:")
	except getopt.GetoptError:
		print 'resizeXfsPartition.py /dev/sda'
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print 'resizeXfsPartition.py /dev/sda'
			sys.exit()
	for arg in args:
		diskname = arg

	try:
	        partition = subprocess.check_output(["parted", "-s", diskname, "print"], stderr=subprocess.STDOUT)

		startOfPartition = None
		for line in partition.split( '\n' ):
			if re.match( '^ 1', line ):
				row = re.split( ' +', line.strip() )
				if len( row ) > 1:
					startOfPartition = row[1]
					print startOfPartition

		if startOfPartition != None:
			partition = subprocess.check_output(["parted", "-s", diskname, "rm", "1"], stderr=subprocess.STDOUT)
			print partition
			partition = subprocess.check_output(["parted", "-s", diskname, "mkpart", "primary", "ext2", startOfPartition, "-1"], stderr=subprocess.STDOUT)
			print partition
			partition = subprocess.check_output(["parted", "-s", diskname, "print"], stderr=subprocess.STDOUT)
			print partition

	except subprocess.CalledProcessError as e:
	        print e.output

if __name__ == "__main__":
	main(sys.argv[1:])
