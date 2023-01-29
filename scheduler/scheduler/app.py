import os
from os import environ
import json
from urllib.parse import urlparse
import jstyleson
import requests
import concurrent.futures
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from datetime import datetime
from pytz import timezone
from utils import expand_config_template
from storage import save_to_file, copy_file
from logger import get_logger
from toxiproxy import Toxiproxy

logger = get_logger('app')

requestsSesstion = requests.Session()
retries = Retry(total=10,
                backoff_factor=0.1,
                status_forcelist=[ 500, 502, 503, 504 ])
requestsSesstion.mount('http://', HTTPAdapter(max_retries=retries, pool_maxsize=500))

TIME_ZONE = environ.get('TIME_ZONE')

def get_current_time():
    return datetime.now().astimezone(timezone(TIME_ZONE)) if TIME_ZONE else datetime.now()

def build_scenarios(conf, test_id):
    fault_spec = conf['fault']
    fault_percentages = fault_spec['percentage']
    del fault_spec['percentage']
    patterns = conf['clientSpecs']
    users = conf['users']
    rounds = conf['rounds'] + 1
    max_requests = conf['maxRequests']
    successful_requests = conf['succRequests']
    target_url = conf['targetUrl']
    all_scenarios = []
    scenario_groups = {}
    

    for fault_percentage in fault_percentages:
        for user in users:
            scenarios = []
            for pattern_template in patterns:
                pattern_configs = expand_config_template(pattern_template['patternConfig'])
                for pattern_config in pattern_configs:
                    for idx_round in range(1, rounds):
                        scenarios.append({
                            'patternConfig': pattern_config,
                            'patternTemplate': pattern_template,
                            'users': user,
                            'round': idx_round,
                            'faultPercentage': fault_percentage,
                            'faultSpec': fault_spec,
                            'maxRequests': max_requests,
                            'successfulRequests': successful_requests,
                            'targetUrl': target_url
                        })
            scenario_group_id = 'f'+str(fault_percentage)+'u'+str(user)
            scenario_groups[scenario_group_id] = scenarios
            all_scenarios += scenarios

    total_scenarios = len(fault_percentages) * len(users) * len(all_scenarios)
    logger.info(f'{total_scenarios} scenarios generated')
    save_to_file(f'{test_id}/scenarios', all_scenarios, 'json')
    return scenario_groups

def main():
    conf_file = open(os.environ.get('CONFIG_FILE'), 'r')
    conf = jstyleson.load(conf_file)
    
    test_id = conf['testId'] if 'testId' in conf else get_current_time().strftime('%a %b %d %Hh%Mm%Ss %Y')
    copy_file(os.environ.get('CONFIG_FILE'), f'{test_id}/scenarios-original.json')

    scenario_groups = build_scenarios(conf, test_id)
    all_results = []
    toxiproxy = Toxiproxy()
    upstream = scenario['targetUrl']
    url_parsed = urlparse(scenario['targetUrl'])

    proxy = toxiproxy.create(upstream, listen='{url_parsed.schema}://{url_parsed.hostname}:9008/{url_parsed.path}', enabled=True)

    for scenario_group in scenario_groups.keys():
        total_group_scenarios = len(scenario_groups[scenario_group])
        logger.info(f'group[{scenario_group}] starting processing {total_group_scenarios} scenarios')
        results = []
        scenario_group_count = 0

        for scenario in scenario_groups[scenario_group]:
            scenario_group_count += 1
            
            logger.info(f'group[{scenario_group}] processing scenario {scenario_group_count}/{total_group_scenarios}')
            users = scenario['users'] + 1

            proxy.add_toxic(scenario['faultSpec'])
            
            
            #envoy.setup_fault(scenario['faultSpec'], int(scenario['faultPercentage']))
    
            with concurrent.futures.ThreadPoolExecutor(max_workers=users) as executor:
                futures = []
                for user_id in range(1, users):
                    futures.append(executor.submit(do_test, scenario=scenario, user_id=user_id))
                
                index_result = 0
                for future in concurrent.futures.as_completed(futures):
                    results.append(future.result())
                    index_result += 1
                    logger.info(f'group[{scenario_group}] collecting user results {index_result}/{users-1}')

        all_results += results
        save_to_file(f'{test_id}/results_{scenario_group}', results, 'csv')
            
    save_to_file(f'{test_id}/results', all_results, 'csv')

def do_test(scenario, user_id):
    start_time = datetime.now()
    users = scenario['users']
    pattern_template = scenario['patternTemplate']
    fault_percentage = scenario['faultPercentage']
    fault_spec = scenario['faultSpec']
    pattern_config = scenario['patternConfig']
    idx_round = scenario['round']
    max_requests = scenario['maxRequests']
    successful_requests = scenario['successfulRequests']
    target_url = scenario['targetUrl']

    payload = json.dumps({
        'maxRequests': max_requests,
        'successfulRequests': successful_requests,
        'targetUrl': target_url,
        'patternParams': pattern_config
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
        result['strategy'] = pattern_template['strategy']
        result['faultPercentage'] = fault_percentage
        for fault_key in fault_spec.keys():
            result[f'fault{fault_key.capitalize()}'] = fault_spec[fault_key]        
        for config_key in pattern_config.keys():
            result[config_key] = pattern_config[config_key]
    else:
        result['error'] = True
        result['errorMessage'] = response.text
        result['statusCode'] = response.status_code
    
    return result
    
main()