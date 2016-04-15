import subprocess
import argparse
from getpass import getpass
import multiprocessing
import os
numCPUs = str(multiprocessing.cpu_count())


defaultUserName = 'rallyhealth'
defaultPassword = ''
userPassword = 'rallyw1ns!'
setIncludedTags = ''

parser = argparse.ArgumentParser(description='Take values for running automation')

parser.add_argument('-e', '--ENV', nargs='?', type=str.upper, help='Any valid environment [Default: LOCAL]', default='LOCAL', metavar='')
parser.add_argument('-r', '--RUN', nargs='+', help='Space separated tags to run (ALL to run all batches in parallel) [Default: API]', default=['API'], metavar='')
parser.add_argument('-u', '--USERNAME', nargs='?', help='Replace with your username if desired.' , default=defaultUserName, metavar='')
parser.add_argument('-p', '--PASSWORD', nargs='?', help='Replace with your password if desired.', default=userPassword, metavar='')

args = parser.parse_args()

setVariableArgs = ' --variable RALLY_TEST_ENV:' + args.ENV + \
                  ' --variable RALLY_SUPER_USERNAME:' + args.USERNAME + \
                  ' --variable RALLY_SUPER_PASSWORD:' + 'rallyw1ns!'

if (len(args.RUN) > 0):
    currentDir= os.getcwd()
    dir = os.path.dirname(__file__)

    setIncludedTags = '--include ' + ' --include '.join(args.RUN)
    p1 = subprocess.Popen('pybot ' + setVariableArgs + ' ' + setIncludedTags + ' APITests/', shell=True)

    p1.wait()

else:
    print("No tags specified")

print("done")
