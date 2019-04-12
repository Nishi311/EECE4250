import unittest
from src.controller.Controller import Controller
from src.helper_classes.quiz_results import QuizResults
from src.helper_classes.city_data import CityData

class ControllerTester(unittest.TestCase):

    def setup(self):
        self.controller = Controller()

    def test_specific_city_query(self):
        self.setup()
        city_name = "Los Angeles"

        returned_object = self.controller.query_for_specific_city_data(city_name)

        self.assertEqual(city_name, returned_object.city_name)

    def test_all_city_query(self):
        self.setup()

        returned_city_list = self.controller.query_for_all_city_data()

        expected_num_cities = 25
        all_cities_found = True if len(returned_city_list) == expected_num_cities else False

        all_complete_city_objects = True
        for possible_city_name, possible_city_object in returned_city_list.items():
            if not isinstance(possible_city_object, CityData):
                all_complete_city_objects = False

        self.assertTrue(all_cities_found and all_complete_city_objects)

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
        mock_quiz_results.update_city_scores("Testing String: 0")
        mock_quiz_results.update_user_id(9999)
        success_bool = self.controller.store_in_database("results", mock_quiz_results.return_storage_parameter_names(),
                                                         mock_quiz_results.return_storage_parameter_values())

        self.assertTrue(success_bool)

    def test_full_workflow(self):
        self.setup()
        # Create mock user input weights
        mock_weights = {"walkability": 1, "bikeability": 2, "transit": 3, "traffic": 4,
                        "metro_pop": 5, "pop_density": 6, "prop_crime": 7, "violent_crime": 8,
                        "air_pollution": 9, "sunshine": 10}

        attributes = ["walkability", "bikeability", "transit", "traffic", "metro_pop", "pop_density",
                      "prop_crime", "violent_crime", "air_pollution", "sunshine"]

        # Create Mock city data for controlled calculation
        LA_attribute_scores = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        LA_data = CityData(1, "Los Angeles", attributes, LA_attribute_scores)

        SanFran_attribute_scores = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        SanFran_data = CityData(2, "San Francisco", attributes, SanFran_attribute_scores)

        Boston_attribute_scores = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
        Boston_data = CityData(3, "Boston", attributes, Boston_attribute_scores)

        New_York_attribute_scores = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        New_York_data = CityData(4, "New York", attributes, New_York_attribute_scores)

        Bethesda_attribute_scores = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
        Bethesda_data = CityData(5, "Bethesda", attributes, Bethesda_attribute_scores)

        Austin_attribute_scores = [6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
        Austin_data = CityData(6, "Austin", attributes, Austin_attribute_scores)

        mock_city_data = {"Los Angeles": LA_data, "San Francisco": SanFran_data, "Boston": Boston_data,
                          "New York": New_York_data, "Bethesda": Bethesda_data, "Austin": Austin_data}

        # create expected results
        expected_city_object_list = [Austin_data, Bethesda_data, New_York_data, Boston_data, SanFran_data]
        expected_returned_city_scores_dict = {"Austin": 330, "Bethesda": 275, "New York": 220,
                                              "Boston": 165, "San Francisco": 110}

        # Get the actual returned results
        returned_city_object_list, returned_city_scores_dict = self.controller.run_quiz_workflow(mock_weights, mock_city_data)

        # Check to see if object lists are identical
        object_list_same = set(expected_city_object_list) == set(returned_city_object_list)

        # Check to see if score dicts are identical
        common_key_value_pairs = expected_returned_city_scores_dict.items() & returned_city_scores_dict.items()
        score_dirs_same = False

        if len(common_key_value_pairs) == len(expected_returned_city_scores_dict) == len(returned_city_scores_dict):
            score_dirs_same = True

        # Check for two identical values
        self.assertTrue(object_list_same and score_dirs_same)
