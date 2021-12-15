import os
import json
import requests
import concurrent.futures
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import logging
from datetime import datetime
from pytz import timezone
from utils import expand_config_template
from storage import save_file
from notifier import notify
from envoy import update_percentage_fault, update_duration_fault

logger = logging.getLogger('app')
logger.setLevel(logging.INFO)

requestsSesstion = requests.Session()
retries = Retry(total=10,
                backoff_factor=0.1,
                status_forcelist=[ 500, 502, 503, 504 ])
requestsSesstion.mount('http://', HTTPAdapter(max_retries=retries))

test_id = datetime.now().astimezone(timezone('America/Sao_Paulo')).strftime('%c')

def build_scenarios():
    conf_file = open(os.environ.get('CONFIG_FILE'), 'r')
    conf = json.load(conf_file)

    fault_percentages = conf['fault']['percentage']
    fault_duration = conf['fault']['duration']
    patterns = conf['patterns']
    users = conf['concurrentUsers']
    rounds = conf['rounds'] + 1
    max_requests_allowed = conf['maxRequestsAllowed']
    target_successful_requests = conf['targetSuccessfulRequests']
    scenarios = []

    for fault_percentage in fault_percentages:
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
                            'faultPercentage': fault_percentage,
                            'faultDuration': fault_duration,
                            'maxRequestsAllowed': max_requests_allowed,
                            'targetSuccessfulRequests': target_successful_requests
                        })
    logger.info(f'{len(scenarios)} scenarios generated')
    save_file(f'{test_id}/scenarios', scenarios, 'json')
    return scenarios

def main():
    scenarios = build_scenarios()
    results = []
    for scenario in scenarios:
        users = scenario['users'] + 1
        update_percentage_fault(int(scenario['faultPercentage']))
        update_duration_fault(int(scenario['faultDuration']))
        with concurrent.futures.ThreadPoolExecutor(max_workers=users) as executor:
            futures = []
            for user_id in range(1, users):
                futures.append(executor.submit(do_test, scenario=scenario, user_id=user_id))
            
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
            
    save_file(f'{test_id}/total', results, 'csv')
    notify(f'{test_id} - teste finalizado')


def do_test(scenario, user_id):
    start_time = datetime.now()
    users = scenario['users']
    pattern_template = scenario['patternTemplate']
    fault_percentage = scenario['faultPercentage']
    fault_duration = scenario['faultDuration']
    config_template = scenario['configTemplate']
    idx_round = scenario['round']
    maxRequestsAllowed = scenario['maxRequestsAllowed']
    targetSuccessfulRequests = scenario['targetSuccessfulRequests']

    payload = json.dumps({
        'maxRequestsAllowed': maxRequestsAllowed,
        'targetSuccessfulRequests': targetSuccessfulRequests,
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
        result['round'] = idx_round
        result['lib'] = pattern_template['lib']
        result['pattern'] = pattern_template['pattern']
        result['faultPercentage'] = fault_percentage
        result['faultDuration'] = fault_duration
        for config_key in config_template.keys():
            result[config_key] = config_template[config_key]
    else:
        result['error'] = True
        result['errorMessage'] = response.text
        result['statusCode'] = response.status_code
    
    return result
    
main()
