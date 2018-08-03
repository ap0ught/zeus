#!/usr/bin/env python3
# zeus.py ---POD format documentation is at the end of this file

#Used to decode the JSON
import json
#Used to create a temporary file and write the contents to it
import os
import subprocess
import tempfile
import io
import collections
#Used to give system exit and error messages
import sys

# General defaults/declarations
version = "v0.7"
#Gobal variables
file_path = ""
deploy_dict = dict()
dep_res_dict = dict()

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
	edit			edit the deplotment plan
	help			print this help menu
	load <file>		load the json deployment plan from the specified path
	run [lines]		execute the indicated commands, eg. \"1-3,5-10\"
	walk [lines]		same as run, but prompts before each command
	show			show the command list
"""

# Function Declarations
def cancel():
    print(bcolors.WARNING + "WARNING: Aborting Program" + bcolors.ENDC)
    exit(0)
#End of Function

def edit():
    global file_path
    if file_path:
        try:
            subprocess.call(['vi', file_path])
            load(file_path)
        except:
            print(bcolors.WARNING + "EXCEPTION: Unkown Exception" + bcolors.ENDC)
            print(sys.exc_info()[0])
    else:
        print(bcolors.WARNING + "Please Load A File First" + bcolors.ENDC)
#End of Function

def help():
    print(bcolors.OKGREEN + help_list_new + bcolors.ENDC)
#End of Function

def load(path):
    global file_path
    global deploy_dict
    file_path = path
    try:
        deploy_dict = json.loads(io.open(file_path, mode="r", encoding="utf-8").read())
        #For testing purposes only to show that the dict is sucessfully created
        # print json.dumps(deploy_dict, sort_keys=True, indent=4)
    except ValueError:
        print(bcolors.WARNING + "EXCEPTION: Please Check JSON File Syntax" + bcolors.ENDC)
    except IOError:
        print(bcolors.WARNING + "EXCEPTION: Bad File Path Given" + bcolors.ENDC)
    except:
        print(bcolors.WARNING + "EXCEPTION: Unkown Exception" + bcolors.ENDC)
        print(sys.exc_info()[0])
#End of Function

def reset():
    global deploy_dict
    deploy_dict = {}
    print(bcolors.WARNING + "Deployment Plan Reset" + bcolors.ENDC)
#End of Function

# TODO
def run(lines): # execute the indicated commands, eg. \"1-3,5-10\"
    global deploy_dict
    global dep_res_dict
    if not lines:
        # If there are no specified lines to run, then run them all!
        # for k,v in deploy_dict.items():
        for k, v in collections.OrderedDict(sorted(deploy_dict.items())).items():
            print(bcolors.OKGREEN+ "INFO: Running Command #"+ k +bcolors.ENDC)
            return_code = subprocess.call(v, shell=True)
            #If the return_code is not 0 (Meaning a good execution)
            #Then report the error and add the result to the dep_res_dict
            if return_code:
                print(bcolors.FAIL + "ERROR: Command #"+ k +" Failed"+bcolors.ENDC)
            dep_res_dict[str(k)]=return_code
        show_return()
    else:
        print lines # <type 'str'>
        print type(lines)
#End of Function

# TODO
def walk(lines):
    print "This is where i would exec walk(lines)"
    print lines
    pass # same as run, but prompts before each command
#End of Function

def show():
    global file_path
    global deploy_dict
    global dep_res_dict
    if not file_path:
        print(bcolors.WARNING + "Please Load A File First" + bcolors.ENDC)
    else:
        # print io.open(file_path, mode="r", encoding="utf-8").read()
        for k, v in collections.OrderedDict(sorted(deploy_dict.items())).items():
            print "   "+k +" : "+ v
#End of Function

def show_return():
    global dep_res_dict
    print(bcolors.OKGREEN+ "Deployment Return Codes:"+bcolors.ENDC)
    for k, v in collections.OrderedDict(sorted(dep_res_dict.items())).items():
        if v:
            print "   "+k+"R : "+ (bcolors.FAIL+str(v)+bcolors.ENDC)
        else:
            print "   "+k+"R : "+ (bcolors.OKGREEN+str(v)+bcolors.ENDC)
#End of Function

# Dev function for checking the contents of the deploy dictionary
def print_dict():
    global deploy_dict
    print list(iter(deploy_dict))

    for k,v in deploy_dict.items():
        print k +" : "+ v

    print json.dumps(deploy_dict, sort_keys=True, indent=4)
#End of Function

################################################################################
#                                 Main Program                                 #
################################################################################

# Boastful startup message
print ('\t\t       Zeus ' + version)
print ('\t\t \"Release the Kraken!\"\n')


# Process the command line arguments...
for x in sys.argv[1:]:
    if(x == '-h' or x == '--help'):
        sys.exit(bcolors.OKGREEN + help_list_new + bcolors.ENDC)
    elif(x == '-d' or x == '--debug'):
        print(bcolors.WARNING + "WARNING: Debugging Currently Not Available" + bcolors.ENDC)
    else:
        sys.exit(bcolors.FAIL + "ERROR: Unrecognized Argument: "+ x + bcolors.ENDC)


# Begin Prompt Loop
while True:
    var = raw_input(bcolors.OKGREEN + "zeus--> "+ bcolors.ENDC+" ").split()
    if(not var):
        print(bcolors.WARNING + "No Arguments Given, Please Try Again Or Try 'help'" + bcolors.ENDC)
    elif(var[0] == "help"):
        help()
    elif(var[0] == "edit"):
        edit()
    elif(var[0] == "abort"):
        cancel()
    elif(var[0] == "load"):
        if(len(var) == 1):
            print(bcolors.WARNING + "No Filepath Given" + bcolors.ENDC)
        else:
            load(var[1])
    elif(var[0] == "reset"):
        reset()
    elif(var[0] == "run"):
        if(len(var) == 1):
            run('')
        else:
            run(var[1])
    elif(var[0] == "walk"): #TODO
        walk(var[1])
    elif(var[0] == "show"):
        show()
    #Dev function for checking the contents of deployment dictionary
    elif(var[0] == "test"):
        print_dict()
    else:
        print(bcolors.FAIL + "Invalid Command: Please Try Again Or Try 'help'"+ bcolors.ENDC)

#------------------------------------------------------------------------------#

##################
# Personal Notes #
##################

# -> This works for file editing
# subprocess.call(['vi', '/Users/liamjameson/Desktop/multiply-zeus/zeus/test_json.json'])

# -> This works for splitting the JSON calls into an array for the subprocess
# print subprocess.call("ls -lx".split())
# print subprocess.check_output("ls -l".split())

# Aug 2nd, 2018
#   Things for future reference
#       -> This program does NOT run plan_deployment.pl due to the fact that I
#           would need to change a few small things in that program in order for
#           zeus.py to behave identically to zeus.pl, and since it was determined
#           that I would not have access to that code while working remote I am
#           unable to fix it at this time. Maybe sometime soon in the future
#           (It's a simple fix in what it outputs with 'plan_deployment.pl -j')
#       -> Didn't get a final determination from Mayfield about how he would like
#           the versioning of the edited JSON files to be done so I am just going
#           to implement a temporary solution by adding the Version header to the
#           JSON files. Again this would require a change of plan_deployment.pl
#           for full implementation
#       ->

# July 31st, 2018
#   Things to Ask Mayfield
#       -> An example output from zeus so i can get a general overview of what happens
#       -> How mayfield would like the return codes completed in JSON
#       -> JSON versioning... Either with a header or new file alltogether

####################
# Project Overview #
####################

# --> Maybe think about doing a MVP that loads a json file from a specified path
#     and then runs everything it needs too. Then think about having differen't
#     Branches that incorporate the previous zeus.pl features
# zeus is just a 5 step process

# 1. take in json
# 2. have the ability to run it
# 3. report/save the return code
# 4. be able to edit the json w/versioning
# 5. stop if bad return codes

# no zeus py will just take in a json file

###################
# Project To Do's #
###################

#TODO
# [] implement run()
#   [X] implement run() W/O specified lines
#   [] implement run() W/ specified lines
#   [X] implement the return of execution codes
#   [X] implement the addition of returned execution codes to dictionary
# ? [] implement the overwrite of the JSON file once everything has been exec
# ? [] Show the overall JSON file once everything has been ran
# [] implement walk()
#   [] implement the Similar things to the above function w/ asking next steps
# [] implement 'Versioning'
#   [] implement versioning of different files either by header of new file





# [X] Create error handling to replace AnsweRS:ErrorMaker
# [X] Process command line arguments and print help menu if needed
# [] Create & process signal handlers for python3
#     -> Ask Mayfield about this one
# [] Create a similar Command dispatch table for Zeus execution
#     [X] Finish edit()
#     [X] Finish load(path)
#     [X] Finish reset()
#     [] Finish run(lines)
#     [] Finish walk(lines)
#     [X] Finish show()
# [X] Create Prompt loop
# [X] Take in JSON file from specified path
# [] Decode the JSON file to run deployment steps OR run straight from file
# [] Save the return code of each deployment step
#     -> Either do this by adding a sub number like "4.1":
#     -> Or creating a temp JSON file that will have sub sections
#     -> Maybe think about decoding the JSON into a hashset and then exec that
#     -> Ask Mayfield about this one
# [X] Edit the JSON deployment plan
#     -> Either with versioning by diff file names or adding version headers
#     -> Ask Mayfield about this one
# [] Version the JSON Deployment plan after editing
#     -> Still waiting on a reply from Mayfield about this one
# [] If a bad return code is recieved from the execution, then abort the deploy
# [] TBD
