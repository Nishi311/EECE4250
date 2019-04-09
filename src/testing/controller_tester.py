import unittest
from src.controller.Controller import Controller
from src.helper_classes.quiz_results import QuizResults
from src.helper_classes.city_data import CityData

from src.algorithm.algorithm import AlgorithmRunner
class ControllerTester(unittest.TestCase):

    def setup(self):
        self.controller = Controller()

    def test_specific_city_query(self):
        self.setup()
        city_name = "New York"

        returned_object = self.controller.query_for_specific_city_data(city_name)

        self.assertEqual(city_name, returned_object.city_name)

    def test_all_user_query(self):
        self.setup()

        returned_user_objects = self.controller.query_for_all_user_data()
        self.assertTrue(returned_user_objects)

    def test_specific_user_query(self):
        self.setup()
        user_id = 10000
        username = "Yeezy"

        returned_object = self.controller.query_for_specific_user_data(user_id)
        self.assertEqual(username, returned_object.username)

    def test_quiz_insert(self):
        self.setup()

        mock_weights = {"walkability": 1, "bikeability": 2, "transit": 3, "traffic": 4,
                        "metro_pop": 5, "pop_density": 6, "prop_crime": 7, "violent_crime": 8,
                        "air_pollution": 9, "sunshine": 10}

        mock_quiz_results = QuizResults(mock_weights)

        attributes = ["walkability", "bikeability", "transit", "traffic", "metro_pop", "pop_density",
                      "prop_crime", "violent_crime", "air_pollution", "sunshine"]

        LA_attribute_scores = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        LA_data = CityData("Los Angeles", attributes, LA_attribute_scores)

        SanFran_attribute_scores = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        SanFran_data = CityData("San Fransisco", attributes, SanFran_attribute_scores)

        Boston_attribute_scores = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
        Boston_data = CityData("Boston", attributes, Boston_attribute_scores)

        mock_city_data = {"Los Angeles": LA_data, "San Francisco": SanFran_data, "Boston": Boston_data}
        algorithm_runner = AlgorithmRunner()
        algorithm_runner.all_city_data = mock_city_data
        algorithm_runner.all_city_names = mock_city_data.keys()

        mock_quiz_results.update_city_scores(algorithm_runner.compute_results(mock_quiz_results))
        mock_quiz_results.update_user_id(15)
        mock_quiz_results.update_quiz_id(16)


        self.controller.store_in_database("results", mock_quiz_results.return_storage_parameter_names(),
                                          mock_quiz_results.return_storage_parameter_values())
