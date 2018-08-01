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
    #Temp Testing filepath
file_path = '/Users/liamjameson/Desktop/multiply-zeus/zeus/test_json.json'


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
    plan-json       alias for 'load plan_deployment -j'
"""

# Command dispatch table/functions

def cancel():
    print(bcolors.WARNING + "WARNING: Aborting Program" + bcolors.ENDC)
    exit(0)

#TODO
def edit():
    print("This is where I would edit the File")
    subprocess.call(['vi', file_path])

def help():
    print(bcolors.OKGREEN + help_list_new + bcolors.ENDC)

# TODO
def load(call):
    print "This is where i would call plan_deployment.pl and get the JSON file"
    print "This could also be simply loaded from a JSON specified path"
    print "I would need to change plan_deployment.pl -j to return the file path"
    print "and not the crazy mess output that it currently is"
    print call
    pass # load the command list with the output from call

# TODO
def reset():
    print "This is where I would reset the depoloyment plan"
    print "Not sure if I really need this, since the JSON will get overwritten"
    pass # reload the command list

# TODO
def run(lines):
    print "This is where i would exec run(lines)"
    print lines
    pass # execute the indicated commands, eg. \"1-3,5-10\"

# TODO
def walk(lines):
    print "This is where i would exec walk(lines)"
    print lines
    pass # same as run, but prompts before each command

# TODO
def show():
    print "This is where I would show the JSON file"
    pass # show the command list AKA the JSON FILE

# TODO
def plan_json():
    print "This is where I would plan the deployment with a JSON file"
    pass # show the command list AKA the JSON FILE

# TODO
# Register signal handlers for SIGINT (^C) and SIGTERM.

# $SIG{'INT'} = sub { signal_handler('SIGINT'); };
# $SIG{'TERM'} = sub { signal_handler('SIGTERM'); };

# **** Need to do some research on the best way to handle these in python ****


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


# Begin Prompt Loop

while True:
    # This is a temporary for testing purposes
    var = raw_input(bcolors.OKGREEN + "zeus--> "+ bcolors.ENDC+" ").split()
    if(var[0] == "help"):
        help()
    elif(var[0] == "edit"):
        edit()
    elif(var[0] == "abort"):
        cancel()
    elif(var[0] == "load"):
        load(var[1])
    elif(var[0] == "reset"):
        reset()
    elif(var[0] == "run"):
        run(var[1])
    elif(var[0] == "walk"):
        walk(var[1])
    elif(var[0] == "show"):
        show()
    elif(var[0] == "plan-json"):
        plan_json()
        print var[1:]
    else:
        print(bcolors.FAIL + "Invalid command: '"+var+"' (try 'help')."+ bcolors.ENDC)




##################
# Personal Notes #
##################

# -> This works for file editing
# subprocess.call(['vi', '/Users/liamjameson/Desktop/multiply-zeus/zeus/test_json.json'])

# -> This works for splitting the JSON calls into an array for the subprocess
# print subprocess.call("ls -lx".split())
# print subprocess.check_output("ls -l".split())


# July 31st, 2018
#   Things to Ask Mayfield
#       -> An example output from zeus so i can get a general overview of what happens
#       -> How mayfield would like the return codes completed in JSON
#       -> JSON versioning... Either with a header or new file alltogether

####################
# Project Overview #
####################

# zeus is just a 5 step process

# 1. take in json
# 2. have the ability to run it
# 3. report/save the return code
# 4. be able to edit the json w/versioning
# 5. stop if bad return codes

###################
# Project To Do's #
###################

# [X] Create error handling to replace AnsweRS:ErrorMaker
# [X] Process command line arguments and print help menu if needed
# [] Create & process signal handlers for python3
#     -> Ask Mayfield abot this one
# [] Create a similar Command dispatch table for Zeus execution
#     -> Ask Mayfield abot this one
#     [] Finish edit()
#     [] Finish load(call)
#     [] Finish reset()
#     [] Finish run(lines)
#     [] Finish walk(lines)
#     [] Finish show()
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
