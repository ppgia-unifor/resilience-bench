from utils import expand_config_template
from models import Workload, Benchmark, Scenario, Fault, FaultType, ClientSpec


class BenchmarkBuilder:
    @staticmethod
    def expand_fault(fault_spec):
        return [
            Fault(
                FaultType(fault_spec["type"]),
                fault_percentage,
                fault_spec.get("duration", 0),
                fault_spec.get("status", 0),
            )
            for fault_percentage in fault_spec["percentage"]
        ]

    @staticmethod
    def expand_workloads(workload_spec):
        return [
            Workload(users, workload_spec["rate"], workload_spec["duration"])
            for users in workload_spec["users"]
        ]

    @staticmethod
    def build_scenario_from_json(conf) -> Benchmark:
        fault_spec = conf["fault"]
        clients_spec = conf["clientSpecs"]
        benchmark = Benchmark()
        benchmark.rounds = conf["rounds"]

        for fault in ScenarioBuilder.expand_fault(fault_spec):
            for workload in ScenarioBuilder.expand_workloads(conf["workload"]):
                for client_spec in clients_spec:
                    pattern_configs = expand_config_template(
                        client_spec.get("patternConfig", {})
                    )
                    for pattern_config in pattern_configs:
                        benchmark.scenarios.append(
                            Scenario(
                                fault,
                                workload,
                                spec=ClientSpec(
                                    client_spec["strategy"],
                                    client_spec["platform"],
                                    client_spec["lib"],
                                    "",
                                    pattern_config,
                                ),
                            )
                        )

        return benchmark
