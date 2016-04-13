from robot.api import logger

import inspect
import re

COMMON = {
    'FALSE': {'RALLY_SELENIUM_BROWSER': 'FireFox',
              'RALLY_REMOTE_URL': '',
              'RALLY_DESIRED_CAPABILITIES': 'none',
              'RALLY_SELENIUM_TIMEOUT': '10',
              'RALLY_SELENIUM_SPEED': '.2'
              },
    'TRUE': {
        'RALLY_SELENIUM_BROWSER': 'FF',
        'RALLY_REMOTE_URL': 'http://rallytest:d2ae1b7f-4fcb-4f9e-b0d7-d2b735d25262@ondemand.saucelabs.com:80/wd/hub',
        'RALLY_DESIRED_CAPABILITIES': 'name:RallyAracade Automated Test Suite,platform:Windows 7,browserName:FireFox,version:37.0,javascriptEnabled:True',
        'RALLY_SELENIUM_TIMEOUT': '10',
        'RALLY_SELENIUM_SPEED': '.4'
    }
}

msg_prefix = inspect.getfile(inspect.currentframe()) + ': '
msg_prefix = msg_prefix.replace('\\', '/')


def get_variables(environment, on_demand):
    variables = {"Environment": environment,
                 "On Demand": on_demand
                 }

    passedENV = str(environment).upper()
    ondem = str(on_demand).upper()

    if (passedENV.upper() == 'LOCAL'):
        url = 'localhost:10088'
        adminurl = 'localhost:9090'

    elif(passedENV == 'PROD'):
         url = 'https://arcade.rally.com'

    else:
        url = 'https://' + passedENV.lower() + '-arcade.werally.in'


    ENVS = {

        'RALLY_TEST_URL': url
    }

    # Checks to see if the Environment and OnDemand variables are used
    if re.match('\\$\\{.*\\}', ondem) != None:
        env = COMMON.keys()[0]
        logger.info(msg_prefix + 'Unresolved variable passed in, defaulting to ' + ondem)
    if not COMMON.has_key(ondem):
        raise Exception(
            'Undefined on demand: ' + str(on_demand) + '. Try one of these: ' + ', '.join(
                sorted(COMMON.keys())))

    logger.info(msg_prefix + 'Defining connect web variables for environment ' + passedENV)
    logger.console(msg_prefix + 'Defining connect web variables for environment ' + passedENV)

    return dict(list(COMMON[ondem].items()) + list(ENVS.items()))
