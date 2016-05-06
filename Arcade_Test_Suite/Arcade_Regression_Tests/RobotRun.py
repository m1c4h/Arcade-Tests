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
browser=['FF','CHROME','SAFARI']

parser = argparse.ArgumentParser(description='Take values for running automation')

parser.add_argument('-e', '--ENV', nargs='?', type=str.upper, help='Any valid environment [Default: LOCAL]', default='LOCAL', metavar='')
parser.add_argument('-r', '--RUN', nargs='+', help='Space separated tags to run (ALL to run all batches in parallel) [Default: DEV]', default=['DEV'], metavar='')
parser.add_argument('-s', '--SAUCE', nargs='?', type=str.upper, choices=['TRUE','FALSE'], help='TRUE, FALSE [Default: TRUE]' , default='TRUE', metavar='')
parser.add_argument('-b', '--BROWSER', nargs='?', type=str.upper, choices=['FF','CHROME','SAFARI','IE','IPHONE','ALL'], help='FF, CHROME,IE ,SAFARI,IPHONE,ALL[Default: FF]' , default='Firefox', metavar='')
parser.add_argument('-u', '--USERNAME', nargs='?', help='Replace with your username if desired.' , default=defaultUserName, metavar='')
parser.add_argument('-p', '--PASSWORD', nargs='?', help='Replace with your password if desired.', metavar='')
parser.add_argument('-n', '--PROCESSES', nargs='?', help='Number of processes to run with [Default: ' + str(numCPUs) + ']', default=numCPUs, metavar='')

args = parser.parse_args()




#this feature will only run when if there are failures during first time of execution of ALL tests in parallel
def rerunFunction(processNum,curWorkDir):
    outputFilePath='output.xml';
    rerunFilePath='rerun.xml';
    print 'Failures in batch causing rerun of failed scripts second time'

    reruncommand='pabot --nostatusrc --rerunfailed' +' '+outputFilePath + ' --output'+' '+rerunFilePath+' '+ ' --variable RALLY_TEST_URL:' + args.ENV + \
                  ' --variable ON_DEMAND:' + args.SAUCE + \
                  ' --variable PROCESSES:' + args.PROCESSES + \
                  ' --variable RALLY_SUPER_USERNAME:' + args.USERNAME + \
                  ' --variable RALLY_SELENIUM_BROWSER:'+ args.BROWSER + \
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

if (args.BROWSER != 'ALL'):

    setVariableArgs = ' --processes ' + str(args.PROCESSES) + \
                      ' --variable RALLY_TEST_ENV:' + args.ENV + \
                      ' --variable ON_DEMAND:' + args.SAUCE + \
                      ' --variable RALLY_SELENIUM_BROWSER:'+ args.BROWSER+ \
                      ' --name ' + args.BROWSER


    if (len(args.RUN) > 0):
        currentDir= os.getcwd()
        dir = os.path.dirname(__file__)

        setIncludedTags = '--include ' + ' --include '.join(args.RUN)
        p1 = subprocess.Popen('pabot ' + setVariableArgs + ' ' + setIncludedTags + ' Tests/', shell=True)
        print 'pabot ' + setVariableArgs + ' ' + setIncludedTags + ' Tests'
        p1.wait()
elif(args.BROWSER == 'ALL'):
        for br in browser:
            setVariableArgs = ' --processes ' + str(args.PROCESSES) + \
                      ' --variable RALLY_TEST_ENV:' + args.ENV + \
                      ' --variable ON_DEMAND:' + args.SAUCE + \
                      ' --variable RALLY_SELENIUM_BROWSER:'+ br+ \
                      ' --name '  +br

            if (len(args.RUN) > 0):
                currentDir= os.getcwd()
                dir = os.path.dirname(__file__)
                setIncludedTags = '--include ' + ' --include '.join(args.RUN)
                p1 = subprocess.Popen('pabot ' + setVariableArgs + ' ' + setIncludedTags +' Tests/',shell=True)
                print 'pabot ' + setVariableArgs + ' ' + setIncludedTags + ' Tests'
                p1.wait()
                print br
                browserTests='rebot --output' ' '+ br +'.xml'  ' output.xml'
                print "*******" + browserTests
                p2 = subprocess.Popen(browserTests,shell=True)
                p2.wait()

        merge='rebot -N Cross_Browser_Compatibility  FF.xml  CHROME.xml SAFARI.xml '
        # merge='rebot output.xml'
        p3 = subprocess.Popen(merge,shell=True)

#Find out if any of the tags that should be rerun are in the rerun_tags list and then call the rerunFunction


print p1.returncode

if  (p1.returncode == 0 ):
    # we stop the script here if all the tests were OK
    print p1.returncode
    print("No tags to be rerun")
    exit(0)

elif (p1.returncode > 0 ) :
    rerun_tags=['REGRESSION','ALL']
    if any(args.RUN[0].upper() in s for s in rerun_tags):
      print(args.RUN[0].upper())
      rerunFunction(p1,currentDir)

print("done")