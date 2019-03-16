import unittest
from algorithm.algorithm import AlgorithmRunner
from helper_classes.city_data import CityData
from helper_classes.quiz_results import QuizResults


class AlgorithmTester(unittest.TestCase):

    def setup(self):

        LA_attributes = {"walkability": 3, "sunshine": 10, "tech_jobs": 6}
        LA_data = CityData("Los Angeles", LA_attributes)

        SanFran_attributes = {"walkability": 4, "sunshine": 7, "tech_jobs": 10}
        SanFran_data = CityData("San Fransisco", SanFran_attributes)

        Boston_attributes = {"walkability": 10, "sunshine": 5, "tech_jobs": 6}
        Boston_data = CityData("Boston", Boston_attributes)

        mock_city_data = {"Los Angeles": LA_data, "San Fransisco": SanFran_data, "Boston": Boston_data}

        mock_weights = {"walkability": 1, "sunshine": 10, "tech_jobs": 5}
        self.mock_quiz_results = QuizResults(mock_weights)

        self.algorithm_runner = AlgorithmRunner()
        self.algorithm_runner.all_city_data = mock_city_data
        self.algorithm_runner.all_city_names = mock_city_data.keys()
        self.algorithm_runner.num_cities_to_return = 3

    def test_compute_results(self):
        self.setup()
        expected_results = [("Los Angeles", 133), ("San Fransisco", 124), ("Boston", 90)]
        generated_results = self.algorithm_runner.compute_results(self.mock_quiz_results)
        self.assertEqual(generated_results, expected_results)


if __name__ == "__main__":
    AlgorithmTester()
    AlgorithmTester.test_compute_results()
