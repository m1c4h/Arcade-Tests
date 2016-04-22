COMMON = {
    'FALSE': {'RALLY_SELENIUM_BROWSER': 'FireFox',
              'RALLY_REMOTE_URL': '',
              'RALLY_DESIRED_CAPABILITIES': 'none',
              'RALLY_SELENIUM_TIMEOUT': '10',
              'RALLY_SELENIUM_SPEED': '.2'
              },
    }


def get_variables(environment):
    variables = {"Environment": environment
                 }
    passedENV = str(environment)

    if(passedENV.upper() == 'LOCAL'):
        url = 'localhost:10088'
        adminurl = 'localhost:9090'

    else:
        setParamsUrl = 'https://doppelganger-arcade-' + passedENV + '.consul.werally.in/'

        benefitsPlanApi= setParamsUrl+'benefits/plans/v3.6/plandetails.json'
        print setParamsUrl
        print benefitsPlanApi

    ENVS = {
            'Rally_Set_Param': setParamsUrl,
            'RALLY_BenefitPlan_API': benefitsPlanApi

    }
    # env = COMMON.keys()[0]
    # print env
    return dict(list(COMMON['FALSE'].items()) + list(ENVS.items()))

