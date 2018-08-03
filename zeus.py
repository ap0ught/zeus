#!/usr/bin/env python3
# zeus.py

# Author: Liam Jameson
#         Release Engineer Intern
#         Multiply 2018

#Used to decode the JSON
import json
#Used for OS calls and dictionary functions
import os
import subprocess
import io
import collections
#Used to give system exit
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

help_list = """
Commands:
	exit			exit the program
	help			print this help menu
	edit			edit the deplotment plan
	load <file>		load the json deployment plan from the specified path
	run [lines]		execute all OR execute specified commands, eg. \"1-3,5-10\"
	walk [lines]		same as run, but prompts before each command
	show			show the current deployment plan and any return codes
"""
################################################################################
#                            Function Declarations                             #
################################################################################

#Exit zeus.py program as a whole
def exit_program():
    print(bcolors.WARNING + "WARNING: Exiting Program" + bcolors.ENDC)
    exit(0)

#Edit the deployment JSON using 'vi'
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
        print(bcolors.WARNING + "Please Load A Deployment Plan" + bcolors.ENDC)

#Print the help list
def help():
    print(bcolors.OKGREEN + help_list + bcolors.ENDC)

#Load the deployment plan into the dictionary from the specified JSON file path
def load(path):
    global file_path
    global deploy_dict
    file_path = path
    try:
        deploy_dict = json.loads(io.open(file_path, mode="r", encoding="utf-8").read())
    except ValueError:
        print(bcolors.WARNING + "EXCEPTION: Please Check JSON File Syntax" + bcolors.ENDC)
    except IOError:
        print(bcolors.WARNING + "EXCEPTION: Bad File Path Given" + bcolors.ENDC)
    except:
        print(bcolors.WARNING + "EXCEPTION: Unkown Exception" + bcolors.ENDC)
        print(sys.exc_info()[0])

#Reset the deployment dictionary
def reset():
    global deploy_dict
    deploy_dict = {}
    print(bcolors.WARNING + "Deployment Plan Reset" + bcolors.ENDC)

#Run the deployment plan without a walkthrough
def run(lines):
    global deploy_dict
    global dep_res_dict
    dep_res_dict = {}
    #If deployment dictionary is empty
    if not bool(deploy_dict):
        print(bcolors.WARNING + "Please Load A Deployment Plan" + bcolors.ENDC)
    else:
        # If there are no specified lines to run, then run them all!
        if not lines:
            for k, v in collections.OrderedDict(sorted(deploy_dict.items())).items():
                print(bcolors.OKGREEN+ "INFO: Running Command #"+ k +bcolors.ENDC)
                return_code = subprocess.call(v, shell=True)
                #If the return_code is not 0 (Meaning a bad execution)
                #Then report the error and add the result to the result dictionary
                if return_code:
                    print(bcolors.FAIL + "ERROR: Command #"+ k +" Failed"+bcolors.ENDC)
                dep_res_dict[str(k)]=return_code
            #Show the deployment return codes
            show_return()
        #Since there are lines specified, run them
        else:
            #Use the findRange() helper function to decode the specified lines
            line_range = findRange(lines)
            for x in line_range:
                #If the specified line is not apart of the deployment plan,
                #Simply throw a warning message and return the code 127 for that command number
                if str(x) not in deploy_dict:
                    print(bcolors.WARNING+ "WARNING: Command #"+ str(x) +" does not exist"+bcolors.ENDC)
                    dep_res_dict[str(x)]=127
                #If it is apart of the deployment plan, run the commnand
                else:
                    print(bcolors.OKGREEN+ "INFO: Running Command #"+ str(x) +bcolors.ENDC)
                    return_code = subprocess.call(deploy_dict.get(str(x)), shell=True)
                    #If the return_code is not 0 (Meaning a bad execution)
                    #Then report the error and add the result to the result dictionary
                    if return_code:
                        print(bcolors.FAIL + "ERROR: Command #"+ str(x) +" Failed"+bcolors.ENDC)
                    dep_res_dict[str(x)]=return_code
            #Show the deployment return codes
            show_return()

#Helper function to decode the range of the specified lines
def findRange(lines):
    rangeArr = []
    #Replace the commas with spaces then split the lines into a list
    splitLines = lines.replace(',', ' ').split()
    for x in splitLines:
        #If split number range contains a '-', then split that and use the range()
        #Function to decode the range and append it to the rangeArr list
        if '-' in x:
            rangeArr = rangeArr + range(int(x.split('-')[0]), int(x.split('-')[1])+1)
        #Otherwise just append that number to the rangeArr list
        else:
            rangeArr.append(int(x))
    return rangeArr

#Run the deployment plan WITH a walkthrough
def walk(lines):
    global deploy_dict
    global dep_res_dict
    dep_res_dict = {}
    #If deployment dictionary is empty
    if not bool(deploy_dict):
        print(bcolors.WARNING + "Please Load A Deployment Plan" + bcolors.ENDC)
    else:
        # If there are no specified lines to run, then run them all!
        if not lines:
            for k, v in collections.OrderedDict(sorted(deploy_dict.items())).items():
                print(bcolors.OKGREEN+ "The next command to run is #"+ k +bcolors.ENDC)
                print("--> "+v)
                #Loop for walking through the deployment plan
                while True:
                    var = raw_input(bcolors.WARNING+ "Shall we abort, skip, or continue? [a|s|c]: "+bcolors.ENDC)
                    if(var == "a" or var == "A"):
                        #Go back to the main menu
                        prompt_loop()
                    elif(var == "s" or var == "S"):
                        break
                    elif(var == "c" or var == "C"):
                        print(bcolors.OKGREEN+ "INFO: Running Command #"+ v +bcolors.ENDC)
                        return_code = subprocess.call(v, shell=True)
                        #If the return_code is not 0 (Meaning a bad execution)
                        #Then report the error and add the result to the result dictionary
                        if return_code:
                            print(bcolors.FAIL + "ERROR: Command #"+ k +" Failed. Exiting deployment..."+bcolors.ENDC)
                        dep_res_dict[str(k)]=return_code
                        #Go back to the main menu
                        prompt_loop()
                        break
                    else:
                        print(bcolors.WARNING+ "Invalid input... Please try again."+bcolors.ENDC)
            #Show the deployment return codes
            show_return()
        else:
            #Use the findRange() helper function to decode the specified lines
            line_range = findRange(lines)
            for x in line_range:
                #If the specified line is not apart of the deployment plan,
                #Simply throw a warning message and return the code 127 for that command number
                if str(x) not in deploy_dict:
                    print(bcolors.WARNING+ "WARNING: Command #"+ str(x) +" does not exist... Skipping"+bcolors.ENDC)
                    dep_res_dict[str(x)]=127
                #If it is apart of the deployment plan, run the commnand
                else:
                    print(bcolors.OKGREEN+ "The next command to run is #"+ str(x) +bcolors.ENDC)
                    print("--> "+deploy_dict.get(str(x)))
                    #Loop for walking through the deployment plan
                    while True:
                        var = raw_input(bcolors.WARNING+ "Shall we abort, skip, or continue? [a|s|c]: "+bcolors.ENDC)
                        if(var == "a" or var == "A"):
                            #Go back to the main menu
                            prompt_loop()
                        elif(var == "s" or var == "S"):
                            break
                        elif(var == "c" or var == "C"):
                            print(bcolors.OKGREEN+ "INFO: Running Command #"+ str(x) +bcolors.ENDC)
                            return_code = subprocess.call(deploy_dict.get(str(x)), shell=True)
                            #If the return_code is not 0 (Meaning a bad execution)
                            #Then report the error and add the result to the result dictionary
                            if return_code:
                                print(bcolors.FAIL + "ERROR: Command #"+ str(x) +" Failed. Exiting deployment..."+bcolors.ENDC)
                            dep_res_dict[str(x)]=return_code
                            #Go back to the main menu
                            prompt_loop()
                            break
                        else:
                            print(bcolors.WARNING+ "Invalid input... Please try again."+bcolors.ENDC)
            #Show the deployment return codes
            show_return()

#Show the deployment dictionary that holds all of the deployment information
def show():
    global file_path
    global deploy_dict
    global dep_res_dict
    if not file_path:
        print(bcolors.WARNING + "Please Load A Deployment Plan" + bcolors.ENDC)
    else:
        for k, v in collections.OrderedDict(sorted(deploy_dict.items())).items():
            print "   "+k +" : "+ v
        if bool(dep_res_dict):
            show_return()

#Helper Function to show the deployment plan execution return codes
def show_return():
    global dep_res_dict
    if bool(dep_res_dict):
        print(bcolors.OKGREEN+ "Deployment Return Codes:"+bcolors.ENDC)
        for k, v in collections.OrderedDict(sorted(dep_res_dict.items())).items():
            if v:
                print "   "+k+"R : "+ (bcolors.FAIL+str(v)+bcolors.ENDC)
            else:
                print "   "+k+"R : "+ (bcolors.OKGREEN+str(v)+bcolors.ENDC)

#Main Menu loop
def prompt_loop():
    while True:
        var = raw_input(bcolors.OKGREEN + "zeus--> "+ bcolors.ENDC+" ").split()
        if(not var):
            print(bcolors.WARNING + "No Arguments Given, Please Try Again Or Try 'help'" + bcolors.ENDC)
        elif(var[0] == "help"):
            help()
        elif(var[0] == "edit"):
            edit()
        elif(var[0] == "exit"):
            exit_program()
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
        elif(var[0] == "walk"):
            if(len(var) == 1):
                walk('')
            else:
                walk(var[1])
        elif(var[0] == "show"):
            show()
        #Dev function for checking the contents of deployment dictionary
        elif(var[0] == "test"):
            print_dict()
        else:
            print(bcolors.FAIL + "Invalid Command: Please Try Again Or Try 'help'"+ bcolors.ENDC)


# Dev function for checking the contents of the deploy dictionary
def print_dict():
    global deploy_dict
    print list(iter(deploy_dict))
    for k,v in deploy_dict.items():
        print k +" : "+ v
    print json.dumps(deploy_dict, sort_keys=True, indent=4)


################################################################################
#                                 Main Program                                 #
################################################################################

# Boastful startup message
print ('\t\t       Zeus ' + version)
print ('\t\t \"Release the Kraken!\"\n')

# Process the command line arguments...
for x in sys.argv[1:]:
    if(x == '-h' or x == '--help'):
        sys.exit(bcolors.OKGREEN + help_list + bcolors.ENDC)
    elif(x == '-d' or x == '--debug'):
        print(bcolors.WARNING + "WARNING: Debugging Currently Not Available" + bcolors.ENDC)
    else:
        sys.exit(bcolors.FAIL + "ERROR: Unrecognized Argument: "+ x + bcolors.ENDC)

# Begin Main Menu Prompt Loop
prompt_loop()

################################################################################
#                               Project Notes                                  #
################################################################################


#################
# Project Notes #
#################

# Future Project Notes
# --> For future intergrations with plan_deployment.pl the following must be changed
#       - The Plan alias function in zeus.py needs to be added so it will call
#           plan_deployment.pl -j with the respective flags and recieve the
#           the deployment plan JSON file path which will then be assigned to the
#           file_path global variable in zeus.py. From there, the load() function
#           can be called with the recieved path and the program will execute
#           much like its parent program zeus.pl
#       - In plan_deployment.pl, the switch -j needs slight editing to ONLY output
#           the specifed file path to the deployment plan JSON
