import unittest
import json
from scenario_builder import ScenarioBuilder

class ScenarioBuilderTest(unittest.TestCase):
    
    def test_builder_from_json(self):
        json_file = open("./scenario-test.json")
        conf = json.load(json_file)
        benchmark = ScenarioBuilder.build_scenario_from_json(conf)
        self.assertIsNotNone(benchmark)
        self.assertEquals(benchmark.rounds, 10)