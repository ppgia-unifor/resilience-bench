import unittest
import json
from benchmark_builder import BenchmarkBuilder

class BenchmarkBuilderTest(unittest.TestCase):
    
    def test_builder_from_json(self):
        json_file = open("./scenario-test.json")
        conf = json.load(json_file)
        benchmark = BenchmarkBuilder.build_scenario_from_dict(conf)
        self.assertIsNotNone(benchmark)
        self.assertEquals(benchmark.rounds, 10)