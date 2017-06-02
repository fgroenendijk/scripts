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
		# Fix GPT disk, place GPT index at end of disk
		pipes = subprocess.Popen( ["gdisk", diskname], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE )
		stdout, stderr = pipes.communicate( "x\ne\nw\nY\n" )
		print stdout

	        partition = subprocess.check_output(["parted", "-s", diskname, "print"], stderr=subprocess.STDOUT)

		startOfPartition = None
		diskSize = None
		for line in partition.split( '\n' ):
			if re.match( '^ 1', line ):
				row = re.split( ' +', line.strip() )
				if len( row ) > 1:
					startOfPartition = row[1]
					print startOfPartition
                        elif re.match( '^Disk ' + diskname + ':', line ):
				row = re.split( ': +', line.strip() )
				if len( row ) > 1:
					diskSize = row[1]
					print "Disk size is: " + diskSize

		if startOfPartition != None and diskSize != None:
			# Remove first partition
			pipes = subprocess.Popen( ["gdisk", diskname], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE )
			stdout, stderr = pipes.communicate( "d\nw\nY\n" )
			print stdout
			# Create partition based on disk size
			partition = subprocess.check_output(["parted", "-s", diskname, "mkpart", "primary", "ext2", startOfPartition, diskSize], stderr=subprocess.STDOUT)
			print partition
			partition = subprocess.check_output(["parted", "-s", diskname, "print"], stderr=subprocess.STDOUT)
			print partition

	except subprocess.CalledProcessError as e:
	        print "ERROR Caught: " + e.output

if __name__ == "__main__":
	main(sys.argv[1:])
