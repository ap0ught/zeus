#!/usr/bin/env python3
# zeus.py ---POD format documentation is at the end of this file

#Used to decode the JSON
import json
#Used to create a temporary file and write the contents to it
import os, subprocess, tempfile
#Used to give system exit and error messages
import sys


#Used for warning messages
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



version = "v0.7"
file_path = ""

help_list_old = """
Commands:
	abort			quit, exit, etc.
	edit			edit the command list
	help			print this help menu
	load <call>		load the command list with the output from call
	reset			reload the command list
	run [lines]		execute the indicated commands, eg. \"1-3,5-10\"
	walk [lines]		same as run, but prompts before each command
	show			show the command list
Aliases:
	plan			alias for 'load plan_deployment'
"""

help_list_new = """
Commands:
	edit			edit the command list
	help			print this help menu
	load <call>		load the command list with the output from call
	reset			reload the command list
	run [lines]		execute the indicated commands, eg. \"1-3,5-10\"
	walk [lines]		same as run, but prompts before each command
	show			show the command list
Aliases:
	plan			alias for 'load plan_deployment'
"""

# Command dispatch table



# Boastful startup message
print ('\t\t       Zeus ' + version)
print ('\t\t \"Release the Kraken!\"\n')


# Process the command line arguments...
for x in sys.argv[1:]:
    if(x == '-h' or x == '--help'):
        sys.exit(bcolors.OKGREEN + help_list_new + bcolors.ENDC)
    elif(x == '-d' or x == '--debug'):
        print(bcolors.WARNING + "WARNING: Debugging currently not available" + bcolors.ENDC)
    else:
        sys.exit(bcolors.FAIL + "ERROR: Unrecognized argument: "+ x + bcolors.ENDC)













##############################################
# Personal Notes #

# One way to edit the file
# import subprocess
# subprocess.call(['vi', 'filename.txt'])


# This works
# subprocess.call(['vi', '/Users/liamjameson/Desktop/multiply-zeus/zeus/test_json.json'])
