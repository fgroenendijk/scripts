import re
import subprocess

try:
        partition = subprocess.check_output(["parted", "/dev/xvdf", "print"], stderr=subprocess.STDOUT)

        startOfPartition = None
        for line in partition.split( '\n' ):
                if re.match( '^ 1', line ):
                        row = re.split( ' +', line.strip() )
                        if len( row ) > 1:
                                startOfPartition = row[1]
                                print startOfPartition

        if startOfPartition != None:
                partition = subprocess.check_output(["parted", "/dev/xvdf", "rm", "1"], stderr=subprocess.STDOUT)
                print partition
                partition = subprocess.check_output(["parted", "/dev/xvdf", "mkpart", "primary", "ext2", startOfPartition, "-1"], stderr=subprocess.STDOUT)
                print partition
                partition = subprocess.check_output(["parted", "/dev/xvdf", "print"], stderr=subprocess.STDOUT)
                print partition

except subprocess.CalledProcessError as e:
        print e.output
