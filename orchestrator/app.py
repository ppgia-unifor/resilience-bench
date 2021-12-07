import os
import json
import requests
import concurrent
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import logging
from datetime import datetime
from utils import expand_config_template
from storage import save_file
from notifier import notify

logger = logging.getLogger()
logger.setLevel(logging.INFO)

requestsSesstion = requests.Session()
retries = Retry(total=10,
                backoff_factor=0.1,
                status_forcelist=[ 500, 502, 503, 504 ])
requestsSesstion.mount('http://', HTTPAdapter(max_retries=retries))

test_id = datetime.now().strftime('%c')

def build_scenarios():
    conf_file = open(os.environ.get('CONFIG_FILE'), 'r')
    conf = json.load(conf_file)

    failure_rate = conf['failureRate']
    patterns = conf['patterns']
    users = conf['concurrentUsers']
    rounds = conf['rounds'] + 1
    envoy_host = conf['envoyHost']
    scenarios = []

    for failure in failure_rate:
        for pattern_template in patterns:
            config_templates = expand_config_template(pattern_template['configTemplate'])
            for config_template in config_templates:
                for user in users:
                    for idx_round in range(1, rounds):
                        scenarios.append({
                            'configTemplate': config_template,
                            'patternTemplate': pattern_template,
                            'users': user,
                            'round': idx_round,
                            'failure': failure,
                            'envoyHost': envoy_host
                        })
    logger.info(f'{len(scenarios)} scenarios generated')
    save_file(f'{test_id}/scenarios', scenarios, 'json')
    return scenarios

def main():
    scenarios = build_scenarios()
    results = []
    for scenario in scenarios:
        users = scenario['users'] + 1
        with concurrent.futures.ThreadPoolExecutor(max_workers=users) as executor:
            futures = []
            for user_id in range(1, users):
                futures.append(executor.submit(do_test, scenario=scenario, user_id=user_id))
            
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
            
    save_file(f'{test_id}/total', results, 'csv')
    notify(f'{test_id} - teste finalizado')

def update_env(server_host, failure):
    pass

def do_test(scenario, user_id):
    start_time = datetime.now()
    users = scenario['users']
    pattern_template = scenario['patternTemplate']
    failure = scenario['failure']
    config_template = scenario['configTemplate']
    round = scenario['round']

    payload = json.dumps({
        'concurrentUsers': users,
        'maxRequestsAllowed': 1000,
        'targetSuccessfulRequests': 25,
        'params': config_template
    })
    response = requestsSesstion.post(
        pattern_template['url'], 
        data=payload, 
        headers={'Content-Type': 'application/json'}
    )
    result = {}
    if response.status_code == 200:
        result = response.json()
        result['userId'] = user_id
        result['startTime'] = start_time
        result['endTime'] = datetime.now()
        result['users'] = users
        result['round'] = round
        result['lib'] = pattern_template['lib']
        result['name'] = pattern_template['name']
        result['failureRate'] = failure
        for config_key in config_template.keys():
            result[config_key] = config_template[config_key]
    else:
        result['error'] = True
        result['errorMessage'] = response.text
        result['statusCode'] = response.status_code
    
    return result
    
main()
