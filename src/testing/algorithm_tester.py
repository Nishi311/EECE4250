import unittest
from algorithm.algorithm import AlgorithmRunner
from helper_classes.city_data import CityData
from helper_classes.quiz_results import QuizResults


class AlgorithmTester(unittest.TestCase):

    def setup(self):
        self.algorithm_runner = AlgorithmRunner()
        self.algorithm_runner.num_cities_to_return = 3

    def test_compute_results(self):
        self.setup()
        mock_weights = {"walkability": 1, "sunshine": 10, "tech_jobs": 5}
        self.mock_quiz_results = QuizResults(mock_weights)

        attributes = ["walkability", "sunshine", "tech_jobs"]
        LA_attribute_scores = [3, 10, 6]
        LA_data = CityData("Los Angeles", attributes, LA_attribute_scores)

        SanFran_attribute_scores = [4, 7, 10]
        SanFran_data = CityData("San Fransisco", attributes, SanFran_attribute_scores)

        Boston_attribute_scores = [10, 5, 6]
        Boston_data = CityData("Boston", attributes, Boston_attribute_scores)

        mock_city_data = {"Los Angeles": LA_data, "San Fransisco": SanFran_data, "Boston": Boston_data}
        self.algorithm_runner.all_city_data = mock_city_data
        self.algorithm_runner.all_city_names = mock_city_data.keys()

        expected_results = [("Los Angeles", 133, LA_data), ("San Fransisco", 124, SanFran_data),
                            ("Boston", 90, Boston_data)]
        generated_results = self.algorithm_runner.compute_results(self.mock_quiz_results)
        self.assertEqual(generated_results, expected_results)

    def test_query(self):
        self.setup()
        self.algorithm_runner.query_database("city_index")
        self.assertTrue(self.algorithm_runner.all_city_data)

    def test_workflow(self):
        self.setup()
        mock_weights = {"walkability": 1, "transit": 10, "pop_density": 5, "bikeability": 1,
                        "metro_population": 10, "prop_crime": 5, "violent_crime": 1, "air_pollution": 10}
        mock_quiz_results = QuizResults(mock_weights)
        generated_results = self.algorithm_runner.run_module(mock_quiz_results)
        self.assertTrue(generated_results)

if __name__ == "__main__":
    AlgorithmTester()
    # AlgorithmTester.test_compute_results()
    AlgorithmTester.test_query()