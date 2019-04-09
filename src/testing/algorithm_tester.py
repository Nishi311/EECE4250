import unittest
from src.algorithm.algorithm import AlgorithmRunner
from src.helper_classes.city_data import CityData
from src.helper_classes.quiz_results import QuizResults


class AlgorithmTester(unittest.TestCase):

    def setup(self):
        self.algorithm_runner = AlgorithmRunner()
        self.algorithm_runner.num_cities_to_return = 3

    def test_calculation(self):
        self.setup()
        mock_weights = {"walkability": 1, "sunshine": 10, "tech_jobs": 5}
        self.mock_quiz_results = QuizResults(mock_weights)

        attributes = ["walkability", "sunshine", "tech_jobs"]
        LA_attribute_scores = [3, 10, 6]
        LA_data = CityData(1, "Los Angeles", attributes, LA_attribute_scores)

        SanFran_attribute_scores = [4, 7, 10]
        SanFran_data = CityData(2, "San Fransisco", attributes, SanFran_attribute_scores)

        Boston_attribute_scores = [10, 5, 6]
        Boston_data = CityData(3, "Boston", attributes, Boston_attribute_scores)

        mock_city_data = {"Los Angeles": LA_data, "San Francisco": SanFran_data, "Boston": Boston_data}

        expected_results = "Los Angeles:133.0, San Francisco:124.0, Boston:90.0"
        generated_results_object = self.algorithm_runner.run_module(self.mock_quiz_results, mock_city_data)
        self.assertEqual(expected_results, generated_results_object.print_cities())

