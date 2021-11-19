import json

# recursively generates config instances from given 
# config template and given key expansion list
def generate_config(config_template, key_expansion_list):
    config_list = []

    if key_expansion_list:
        (key, val_list) = key_expansion_list[0]

        if key in config_template.keys():
            # generate config instances for each key value
            for val in val_list:
                config = config_template.copy() 
                config[key] = val

                # check whether there are still keys to expand
                if key_expansion_list[1:]:
                    # recursively generate new config instances using current (expanded) config instance as templace 
                    config_list += generate_config(config, key_expansion_list[1:])
                else:
                    # add fully expanded config instance to config list
                    config_list.append(config)
    
    return config_list

# expand given config_template by replacing all list values with 
# their individual elements combination  
def expand_config_template (config_template):
    key_expansion_list = []

    # find all template keys that need to be expanded 
    # (i.e., have a list as their values)
    for (key, val) in config_template.items():
        if type(val) is list:
           key_expansion_list.append((key, val))

    # check whether config template has keys to expand
    if key_expansion_list:
        # generate all possible config instance combinations from 
        # the given config template and key expansion list
        return generate_config(config_template, key_expansion_list)
    else:
        # no template expansion needed
        return [config_template]


# config_template = {
#     'name': 'retry',
#     'duration': [10, 20, 30],
#     'platform': 'java8',
#     'failure_threshold': [2, 3]
# }


config_template = {
    "envoy_host": "http://envoy:9100",
    "failure_rate": [0, 25, 50, 75],
    "concurrentUsers": [1, 25, 50, 75, 100],
    "rounds": 10,
    "patterns": [
        {
            "name": "polly-retry",
            "platform": "dotnet",
            "lib": "polly",
            "url": "http://polly:5000/retry",
            "config_template": {
                "count": 3,
                "sleepDurationType": "EXPONENTIAL_BACKOFF",
                "exponentialBackoffPow": 1.5,
                "sleepDuration": [50, 75, 100, 200]
            }
        },
        {
            "name": "r4j",
            "platform": "java",
            "lib": "resilience4j",
            "url": "http://localhost:8080/retry",
            "config_template": {
                "maxAttempts": 3,
                "waitDuration": [50, 75, 100, 200],
                "intervalFunction": "EXPONENTIAL_BACKOFF",
                "initialIntervalMillis": 500,
                "multiplier": 1.5
            }
        }
    ]
}
# config_instances = expand_config_template(config_template)

# print(len(config_instances), 'config instance(s) generated!')
# print(json.dumps(config_instances))

print(json.dumps(expand_config_template(config_template)))

