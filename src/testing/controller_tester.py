import unittest
from src.controller.Controller import Controller


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
