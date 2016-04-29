from robot.api import logger

import inspect
import re

COMMON = {
    'FALSE': {
              'RALLY_SELENIUM_BROWSER': 'FF',
              'RALLY_REMOTE_URL': '',
              'RALLY_DESIRED_CAPABILITIES': 'none',
              'RALLY_SELENIUM_TIMEOUT': '10',
              'RALLY_SELENIUM_SPEED': '.2'
           },
    'TRUE': {'FF': {
        'RALLY_SELENIUM_BROWSER': 'FF',
        'RALLY_REMOTE_URL': 'http://rallytest:d2ae1b7f-4fcb-4f9e-b0d7-d2b735d25262@ondemand.saucelabs.com:80/wd/hub',
        'RALLY_DESIRED_CAPABILITIES': 'name:Rally Arcade FF Automated Test Suite,platform:Windows 7,browserName:FireFox,version:latest-1 ,javascriptEnabled:True',
        'RALLY_SELENIUM_TIMEOUT': '10',
        'RALLY_SELENIUM_SPEED': '.4'
            },
        'CHROME': {
        'RALLY_SELENIUM_BROWSER': 'CHROME',
        'RALLY_REMOTE_URL': 'http://rallytest:d2ae1b7f-4fcb-4f9e-b0d7-d2b735d25262@ondemand.saucelabs.com:80/wd/hub',
        'RALLY_DESIRED_CAPABILITIES': 'name:Rally Arcade CHROME Automated Test Suite,platform:Windows 7,browserName:Chrome,version:latest-1 ,javascriptEnabled:True',
        'RALLY_SELENIUM_TIMEOUT': '10',
        'RALLY_SELENIUM_SPEED': '.4'
            },
        'ALL' :{
        'RALLY_SELENIUM_BROWSER': 'ALL',
        'RALLY_REMOTE_URL': 'http://rallytest:d2ae1b7f-4fcb-4f9e-b0d7-d2b735d25262@ondemand.saucelabs.com:80/wd/hub',
        'RALLY_DESIRED_CAPABILITIES': 'name:Rally Arcade FF Automated Test Suite,platform:Windows 7,browserName:FireFox,version:latest-1 ,javascriptEnabled:True',
        'RALLY_SELENIUM_TIMEOUT': '10',
        'RALLY_SELENIUM_SPEED': '.4'
            }
    }
}
msg_prefix = inspect.getfile(inspect.currentframe()) + ': '
msg_prefix = msg_prefix.replace('\\', '/')


def get_variables(environment, on_demand, browser):
    variables = {"Environment": environment,
                 "On Demand": on_demand,
                 "Browser": browser
                 }

    passedENV = str(environment).upper()
    print passedENV
    ondem = str(on_demand).upper()
    # browser= str(browser).upper()
    print ondem
    print browser

    if (passedENV.upper() == 'LOCAL'):
        url = 'localhost:10088'
        adminurl = 'localhost:9090'

    elif(passedENV == 'PROD'):
         url = 'https://arcade.rally.com'

    else:
        url = 'https://' + passedENV.lower() + '-arcade.werally.in'

    print   url


    ENVS = {

        'RALLY_TEST_URL': url
    }

    print   url
    # Checks to see if the Environment and OnDemand variables are used
    if re.match('\\$\\{.*\\}', ondem) != None:
        env = COMMON.keys()[0]
        logger.info(msg_prefix + 'Unresolved variable passed in, defaulting to ' + ondem)
    if not COMMON.has_key(ondem):
        raise Exception(
            'Undefined on demand: ' + str(on_demand) + '. Try one of these: ' + ', '.join(
                sorted(COMMON.keys())))

    logger.info(msg_prefix + 'Defining arcade web variables for environment ' + passedENV)
    logger.console(msg_prefix + 'Defining arcade web variables for environment ' + passedENV)

    if  ondem == 'FALSE':
       print        dict(list(COMMON[ondem].items()))
       return  dict(list(COMMON[ondem].items()) +list(ENVS.items()))
    else:
         print       dict(list(COMMON[ondem][browser].items()) +list(ENVS.items()))
         return  dict(list(COMMON[ondem][browser].items()) +list(ENVS.items()))





