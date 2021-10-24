import json

def main(conf_file_path):
    conf_file = open(conf_file_path, 'r')
    conf = json.load(conf_file)

    server_failures = conf['failure_rate']
    patterns = conf['patterns']
    users = conf['users']
    rounds = conf['rounds']
    envoy_host = conf['envoy_host']

    for server_failure in server_failures:
        update_env(envoy_host, server_failure)
        for pattern in patterns:
            for user in users:
                for round in range(1, rounds + 1):
                    do_test(round, pattern, user)


def update_env(server_host, hostserver_failure_rate):
    pass

def do_test(round, pattern, users):
    print(f"running round [{round}] for pattern [{pattern['name']}] and [{users}] users")


main('./sample-conf.json')