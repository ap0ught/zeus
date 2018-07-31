#!/usr/bin/env python3
# zeus.py ---POD format documentation is at the end of this file

#Used to decode the JSON
import json
#Used to create a temporary file and write the contents to it
import os, subprocess, tempfile
#Used to give system exit and error messages
import sys

# General defaults/declarations
version = "v0.7"
file_path = ""


#Used for colored error handling
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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





# Register signal handlers for SIGINT (^C) and SIGTERM.

# $SIG{'INT'} = sub { signal_handler('SIGINT'); };
# $SIG{'TERM'} = sub { signal_handler('SIGTERM'); };

# **** Need to do some research on the best way to handle these in python ****




##################
# Personal Notes #
##################

# -> This works for file editing
# subprocess.call(['vi', '/Users/liamjameson/Desktop/multiply-zeus/zeus/test_json.json'])

####################
# Project Overview #
####################

# zeus is just a 6 step process

# 1. take in json
# 2. have the ability to run it
# 3. report/save the return code
# 4. be able to edit the json w/versioning
# 5. stop if bad return codes
# well 5 steps

###################
# Project To Do's #
###################

# [X] Create error handling to replace AnsweRS:ErrorMaker
# [X] Process command line arguments and print help menu if needed
# [] Create & process signal handlers for python3
#     -> Ask Mayfield abot this one
# [] Create a similar Command dispatch table for Zeus execution
#     -> Ask Mayfield abot this one
# [] Create Prompt loop
# [] Take in JSON file from specified path
# [] Decode the JSON file to run deployment steps OR run straight from file
# [] Save the return code of each deployment step
#     -> Either do this by adding a sub number like "4.1":
#     -> Or creating a temp JSON file that will have sub sections
#     -> Maybe think about decoding the JSON into a hashset and then exec that
#     -> Ask Mayfield abot this one
# [] Edit the JSON deployment plan and version it
#     -> Either with versioning by diff file names or adding version headers
#     -> Ask Mayfield abot this one
# [] If a bad return code is recieved from the execution, then abort the deploy
# [] TBD
