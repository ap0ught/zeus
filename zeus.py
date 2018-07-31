#!/usr/bin/env python3
# zeus.py ---POD format documentation is at the end of this file

#Used to decode the JSON
import json
#Used to create a temporary file and write the contents to it
import os, subprocess, tempfile


version = "v0.7"





# Boastful startup message
print ('zeus ' + version)
print ('\t \"Release the Kraken!\"\n')




##############################################
# Personal Notes #

# One way to edit the file
# import subprocess
# subprocess.call(['vi', 'filename.txt'])
