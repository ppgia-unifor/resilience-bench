import pandas as pd
import requests

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
        for pattern in patterns:
            for user in users:
                for round in range(1, rounds + 1):
                    result = do_test(pattern, user)
                    for r in result:
                        r['users'] = user
                        r['round'] = round
                        r['lib'] = pattern['lib']
                        r['failure_rate'] = failure
                    results += result
  
    df = pd.DataFrame(results)
    df.to_csv('./test.csv')

def update_env(server_host, failure):
    pass

def do_test(pattern, users):
    payload = {
            'concurrentUsers': users,
            'maxRequestsAllowed': 1000,
            'targetSuccessfulRequests': 25,
            'params': pattern['config_template']
        }
    response = requests.post(pattern['url'], data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    return response.json()


main('./sample-conf.json')

# [{"userId":1,"successfulRequests":25,"unsuccessfulRequests":79,"totalRequests":104,"successTime":567,"errorTime":1339,"totalContentionTime":1906,"totalExecutionTime":9737}]