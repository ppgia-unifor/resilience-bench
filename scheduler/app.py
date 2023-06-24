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
        print(scenario)

    # for scenario_key in benchmark.keys():
    #     scenarios = benchmark.get(scenario_key)
    #     total_scenarios = len(scenarios)
    #     logger.info(
    #         f"group[{scenario_key}] starting processing {total_scenarios} scenarios"
    #     )
    #     results = []
    #     for scenario_index, scenario in enumerate(scenarios, start=1):
    #         logger.info(
    #             f"group[{scenario_key}] processing scenario {scenario_index}/{total_scenarios}"
    #         )
    #         users = scenario.user + 1

    #         with concurrent.futures.ThreadPoolExecutor(max_workers=users) as executor:
    #             futures = [
    #                 executor.submit(do_test, scenario=scenario, user_id=user_id)
    #                 for user_id in range(1, users)
    #             ]
    #             for index_result, future in enumerate(
    #                 concurrent.futures.as_completed(futures), start=1
    #             ):
    #                 results.append(future.result())
    #                 logger.info(
    #                     f"group[{scenario_key}] collecting user results {index_result}/{scenario.user}"
    #                 )

    #     all_results += results
    #     save_to_file(f"{test_id}/results_{scenario_key}", results, "csv")

    # save_to_file(f"{test_id}/results", all_results, "csv")


def do_test(scenario: Scenario, user_id: int):
    start_time = datetime.now()
    response = start_client(scenario)
    result = {}
    if response.status_code == 200:
        result = extract_successful_response(response, user_id, start_time, scenario)
    else:
        result["error"] = True
        result["errorMessage"] = response.text
        result["statusCode"] = response.status_code

    return result


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
