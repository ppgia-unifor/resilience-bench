import pandas as pd
import json
import requests

from utils import expand_config_template

def main(conf_file_path):
    conf_file = open(conf_file_path, 'r')
    conf = json.load(conf_file)

    failure_rate = conf['failure_rate']
    patterns = conf['patterns']
    users = conf['concurrentUsers']
    rounds = conf['rounds']
    envoy_host = conf['envoy_host']

    for failure in failure_rate:
        update_env(envoy_host, failure)
        results = []
        for pattern_template in patterns:
            config_templates = expand_config_template(pattern_template['config_template'])
            for config_template in config_templates:
                do_test(config_template, pattern_template, 1) # warm up application
                for user in users:
                    for round in range(1, rounds + 1):
                        result = do_test(config_template, pattern_template, user)
                        if result is None:
                            break
                        for r in result:
                            r['users'] = user
                            r['round'] = round
                            r['lib'] = pattern_template['lib']
                            r['failure_rate'] = failure
                            for config_key in config_template.keys():
                                r[config_key] = config_template[config_key]
                        results += result
  
    df = pd.DataFrame(results)
    df.to_csv('./test.csv', index=False)

def update_env(server_host, failure):
    pass

def do_test(config_template, pattern, users):
    payload = {
            'concurrentUsers': users,
            'maxRequestsAllowed': 1000,
            'targetSuccessfulRequests': 25,
            'params': config_template
        }
    response = requests.post(pattern['url'], data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        return response.json()
    print('an error occurred ' + response.text)
    return None

main('./sample-conf.json')
