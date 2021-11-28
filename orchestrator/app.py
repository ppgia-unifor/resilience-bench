import pandas as pd
import json
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import logging
import os
from utils import expand_config_template
from storage import save_file
from notifier import notify
from uuid import uuid4

logger = logging.getLogger()

requestsSesstion = requests.Session()

retries = Retry(total=10,
                backoff_factor=0.1,
                status_forcelist=[ 500, 502, 503, 504 ])
requestsSesstion.mount('http://', HTTPAdapter(max_retries=retries))

def build_scenarios():
    conf_file = open(os.environ.get('CONFIG_FILE'), 'r')
    conf = json.load(conf_file)

    failure_rate = conf['failure_rate']
    patterns = conf['patterns']
    users = conf['concurrentUsers']
    rounds = conf['rounds'] + 1
    envoy_host = conf['envoy_host']
    scenarios = []

    for failure in failure_rate:
        for pattern_template in patterns:
            config_templates = expand_config_template(pattern_template['config_template'])
            for config_template in config_templates:
                for user in users:
                    for idx_round in range(1, rounds):
                        scenarios.append({
                            'config_template': config_template,
                            'pattern_template': pattern_template,
                            'user': user,
                            'round': idx_round,
                            'failure': failure,
                            'envoy_host': envoy_host
                        })
    return scenarios


def main():
    test_id = uuid4()
    scenarios = build_scenarios()
    results = []
    total_scenarios = len(scenarios)
    for idx, scenario in enumerate(scenarios):
        user = scenario['user']
        pattern_template = scenario['pattern_template']
        failure = scenario['failure']
        config_template = scenario['config_template']
        round = scenario['round']
        
        logger.info(f'Round [{idx}/{total_scenarios}] Users {user} Pattern {pattern_template["name"]}')

        status_code, result = do_test(config_template, pattern_template, user)
        if status_code != 200:
            result = [{
                'error': True,
                'error_message': result
            }]
        
        for item_result in result:
            item_result['users'] = user
            item_result['round'] = round
            item_result['lib'] = pattern_template['lib']
            item_result['name'] = pattern_template['name']
            item_result['failure_rate'] = failure
            for config_key in config_template.keys():
                item_result[config_key] = config_template[config_key]
        
        results += result

        if idx % 100 == 0:
            save_file(f'{test_id}/{idx}', results)
    save_file(f'{test_id}/total', results)
    notify(f'{test_id} - teste finalizado')

def update_env(server_host, failure):
    pass

def do_test(config_template, pattern, users):
    payload = {
            'concurrentUsers': users,
            'maxRequestsAllowed': 1000,
            'targetSuccessfulRequests': 25,
            'params': config_template
        }
    response = requestsSesstion.post(pattern['url'], data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    result = response.text
    if response.status_code == 200:
        result = response.json()

    return response.status_code, result

main()
