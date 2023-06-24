import os
from os import environ
from os import path
import json
import requests
import concurrent.futures
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from datetime import datetime
from pytz import timezone
from storage import save_to_file, copy_file
from logger import get_logger
from models import Scenario
from benchmark_builder import BenchmarkBuilder
from k8s import K8s

logger = get_logger("app")

requestsSession = requests.Session()
retries = Retry(total=10, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
requestsSession.mount("http://", HTTPAdapter(max_retries=retries, pool_maxsize=500))

TIME_ZONE = environ.get("TIME_ZONE")

k8s = K8s()

def get_current_time():
    return (
        datetime.now().astimezone(timezone(TIME_ZONE)) if TIME_ZONE else datetime.now()
    )


def build_scenarios(conf, test_id):
    benchmark = BenchmarkBuilder.build_scenario_from_dict(conf)
    # logger.info(f"{benchmark.len} scenarios generated")
    # save_to_file(f"{test_id}/scenarios", benchmark.to_list(), "json")
    return benchmark


def main():
    # config_file_path = path.join(
    #     os.environ.get("CONFIG_ROOT_PATH"), os.environ.get("CONFIG_FILE")
    # )
    # conf_file = open(config_file_path, "r")
    # conf = json.load(conf_file)
    test_id = ""
    # copy_file(config_file_path, f"{test_id}/scenarios-original.json")

    conf = k8s.get_benchmark("my-new-benchmark-object")
    benchmark = build_scenarios(conf, test_id)
    
    for scenario in benchmark.scenarios:
        data = {}
        for prop in scenario.spec.pattern_config.keys():
            data[prop] = str(scenario.spec.pattern_config[prop])
        k8s.update_config_map(name="resilience-bench-current-config", data=data)
        do_test(scenario)
    

def do_test(scenario: Scenario):
    start_time = datetime.now()
    print("running test", scenario)
    # set confimap
    
    # result = {}
    # if response.status_code == 200:
    #     result = extract_successful_response(response, user_id, start_time, scenario)
    # else:
    #     result["error"] = True
    #     result["errorMessage"] = response.text
    #     result["statusCode"] = response.status_code

    # return result


def start_client(scenario: Scenario):
    payload = json.dumps(
        {
            "maxRequests": scenario.maxRequests,
            "successfulRequests": scenario.successfulRequests,
            "targetUrl": scenario.targetUrl,
            "patternParams": scenario.patternTemplate.patternConfig,
        }
    )
    return requestsSession.post(
        scenario.patternTemplate.url,
        data=payload,
        headers={"Content-Type": "application/json"},
    )


def extract_successful_response(response, user_id, start_time, scenario):
    result = response.json()
    result["userId"] = user_id
    result["startTime"] = start_time
    result["endTime"] = datetime.now()
    result["users"] = scenario.user
    result["round"] = scenario.round
    result["lib"] = scenario.patternTemplate.lib
    result["strategy"] = scenario.patternTemplate.strategy
    result["faultPercentage"] = scenario.fault.percentage
    result["faultDuration"] = scenario.fault.duration
    result["faultStatus"] = scenario.fault.status
    result["faultType"] = scenario.fault.type

    for config_key in scenario.patternTemplate.patternConfig.keys():
        result[config_key] = scenario.patternTemplate.patternConfig[config_key]
    return result


main()
