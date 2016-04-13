import subprocess
import argparse
from getpass import getpass
import multiprocessing
import os



numCPUs = str(multiprocessing.cpu_count())

defaultUserName = 'ezeffery@spotlite.com'
defaultPassword = 'T3st123!'
userPassword = ''
setIncludedTags = ''

parser = argparse.ArgumentParser(description='Take values for running automation')

parser.add_argument('-e', '--ENV', nargs='?', type=str.upper, help='Any valid environment [Default: LOCAL]', default='LOCAL', metavar='')
parser.add_argument('-r', '--RUN', nargs='+', help='Space separated tags to run (ALL to run all batches in parallel) [Default: DEV]', default=['DEV'], metavar='')
parser.add_argument('-s', '--SAUCE', nargs='?', type=str.upper, choices=['TRUE','FALSE'], help='TRUE, FALSE [Default: FALSE]' , default='FALSE', metavar='')
parser.add_argument('-u', '--USERNAME', nargs='?', help='Replace with your username if desired.' , default=defaultUserName, metavar='')
parser.add_argument('-p', '--PASSWORD', nargs='?', help='Replace with your password if desired.', metavar='')
parser.add_argument('-n', '--PROCESSES', nargs='?', help='Number of processes to run with [Default: ' + str(numCPUs) + ']', default=numCPUs, metavar='')

args = parser.parse_args()




#this feature will only run when if there are failures during first time of execution of ALL tests in parallel
def rerunFunction(processNum,curWorkDir):
    outputFilePath='output.xml';
    rerunFilePath='rerun.xml';
    print 'Failures in batch causing rerun of failed scripts second time'

    reruncommand='pabot --nostatusrc --rerunfailed' +' '+outputFilePath + ' --output'+' '+rerunFilePath+' '+ ' --variable SPOT_TEST_ENV:' + args.ENV + \
                  ' --variable ON_DEMAND:' + args.SAUCE + \
                  ' --variable PROCESSES:' + args.PROCESSES + \
                  ' --variable RALLY_SUPER_USERNAME:' + args.USERNAME + \
                  ' --variable RALLY_SUPER_PASSWORD:' + userPassword + ' ' + 'Tests'
    print 'merging and creating final output.xml'

    mergecommand='rebot --nostatusrc --output output.xml --merge output.xml rerun.xml'

    p8 = subprocess.Popen(reruncommand,shell=True)
    p8.wait()
    p9=subprocess.Popen(mergecommand,shell=True)
    p9.wait()
    print 'function completed'


if(args.USERNAME != defaultUserName and args.PASSWORD == None):
    userPassword = getpass('Password: ')
elif(args.USERNAME != defaultUserName and args.PASSWORD != None):
    userPassword = args.PASSWORD
elif(args.USERNAME == defaultUserName):
    userPassword = defaultPassword

setVariableArgs = ' --processes ' + str(args.PROCESSES) + \
                  ' --variable RALLY_TEST_ENV:' + args.ENV + \
                  ' --variable ON_DEMAND:' + args.SAUCE + \
                  ' --variable RALLY_SUPER_USERNAME:' + args.USERNAME + \
                  ' --variable RALLY_SUPER_PASSWORD:' + userPassword + \
                  ' --nostatusrc'

if (len(args.RUN) > 0):
    currentDir= os.getcwd()
    dir = os.path.dirname(__file__)

    setIncludedTags = '--include ' + ' --include '.join(args.RUN)
    p1 = subprocess.Popen('pabot ' + setVariableArgs + ' ' + setIncludedTags + ' Tests/', shell=True)
    print 'pabot ' + setVariableArgs + ' ' + setIncludedTags + ' Tests'
    p1.wait()

#Find out if any of the tags that should be rerun are in the rerun_tags list and then call the rerunFunction
rerun_tags=['ALL','SMOKE','ALEXBOT_LONGCHECK','ALEXBOT_CHOICELOGIN']

if any(args.RUN[0].upper() in s for s in rerun_tags):
      print(args.RUN[0].upper())
      rerunFunction(p1,currentDir)
else:
    print("No tags to be rerun")


print("done")