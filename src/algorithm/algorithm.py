import mysql.connector
import sys
import os
sys.path.append(os.path.abspath('../helper_classes'))
from helper_classes.quiz_results import QuizResults
from helper_classes.city_data import CityData

class AlgorithmRunner(object):

    def __init__(self):
        self.result_cities = {}
        self.all_city_data = {}
        self.all_city_names = []
        self.db_city_table_name = "city_index"
        self.num_cities_to_return = 5

    def run_module(self, current_quiz):
        if isinstance(current_quiz, QuizResults):
            self.query_database(self.db_city_table_name)
            current_quiz.set_city_scores(self.compute_results(current_quiz))
        else:
            self.exit_with_error("algorithm, run_module(): object passed as current_quiz is NOT of class Quiz "
                                 "Answers.")
        return current_quiz

    def query_database(self, table_name):
        """
        Quick query function to get all the city data from the SQL database.
        :param database_name: Name of the SQL database to query.
        :param table_name: Name of the table to query in the SQL database.
        :return: bool: True -> Successfully acquired data from database.
                       False -> Failed to acquire data from database.
        """
        connection = mysql.connector.connect(host="yuppie-city-simulator-db.cohu57vlr7rd.us-east-2.rds.amazonaws.com",
                                             user="MeanderingArma",
                                             passwd="Dillos1999",
                                             database="YCS")
        cursor = connection.cursor()
        cursor.execute("describe {0}".format(table_name))
        # Gets the whole list of tuples related to table values. We only care about the first position in each tuple
        # of the list, which is the name of a variable associated with a table entry.
        # e.g: [('city_id', 'int(11)', 'NO', 'PRI', None, 'auto_increment'),
        #       ('city_name', 'varchar(32)', 'NO', '', None, '')
        #       ('walkability', 'double', 'YES', '', None, ''),
        #       ...]
        attribute_list_bloated = cursor.fetchall()

        # Cut out the fat and make a list of only the names of attributes. Index values 0 and 1 are city name and ID,
        # which we don't care about right now.
        attribute_list_min = []
        for index, tuple in enumerate(attribute_list_bloated):
            if index > 1:
                attribute_list_min.append(tuple[0])

        # Gets the whole list of table entries in the following format (city index, name, attribute scores...):
        # e.g: [(1, 'New York', 89.2, 84.3, 28317.0, 67.7, 20320876.0, 1448.59, 538.9, 57.08),
        #       (2, 'Los Angeles', 67.4, 52.6, 8484.0, 55.1, 13353907.0, 2535.92, 761.31, 60.35),
        #       (3, 'Chicago', 77.8, 65.3, 11900.0, 71.5, 9533040.0, 3263.8, 1098.86, 41.03),
        #       ...]
        cursor.execute("SELECT * FROM {0}".format(table_name))
        raw_city_score_list = cursor.fetchall()

        if raw_city_score_list:
            # Create proper city data structures for each city using the list of table entries and attribute names
            for index, tuple in enumerate(raw_city_score_list):
                city_name = tuple[1]
                attribute_scores = tuple[2:]
                self.all_city_data[city_name] = CityData(city_name, attribute_list_min, attribute_scores)
                self.all_city_names.append(city_name)
            return True
        else:
            self.exit_with_error("algorithm, query_database(): No data acquired from database in table "
                                 "{0}".format(table_name))
            return False

    def compute_results(self, current_quiz):
        if isinstance(current_quiz, QuizResults):

            # Initialize total city scores to 0.
            total_city_scores = {}
            for city_name in self.all_city_names:
                total_city_scores[city_name] = 0

            # Get the list of all the attributes that the quiz used.
            attribute_weights = current_quiz.return_attribute_weights()

            for attribute_name in attribute_weights.keys():
                # For each attribute used in the quiz, get the dict with every city's score for that attribute
                attribute_scores_for_all_cities = self.get_attribute_scores_for_all_cities(attribute_name)
                # Update each cities score with simple formula:
                # city score = (existing score) + (weight of current attribute) * (score for the city in current attribute)
                # TODO: Get more fancy with this scoring system in the future.
                for city_name in self.all_city_names:
                    total_city_scores[city_name] += attribute_weights[attribute_name] * \
                                                    attribute_scores_for_all_cities[city_name]
            # Sort the cities by total score from greatest to least and cut down to top X number of cities
            ordered_cities = sorted(total_city_scores.items(), key=lambda kv: kv[1], reverse=True)
            ordered_cities = ordered_cities[:self.num_cities_to_return]

            # The final returned list of cities will actually be a tuple consisting of (city name, final city score, and
            # The original city object complete with all its attribute values)
            return_list = []
            for city_name, city_value in ordered_cities:
                value_bundle = (city_name, city_value, self.all_city_data[city_name])
                return_list.append(value_bundle)
            return return_list
        else:
            self.exit_with_error("algorithm, compute_result(): object passed as current_quiz is NOT of class Quiz "
                                 "Answers.")

    def get_attribute_scores_for_all_cities(self, attribute_name):
        """
        Generates a dict keyed by city names and with values corresponding to the city's score for the given attribute.
        :param attribute_name: The attribute that will be pulled for each city.
        :return: dict -> (key, value) = (city name, city score for attribute "attribute_name")
        """
        city_attribute_dict = {}

        for city_name in self.all_city_names:
            # get the attribute score for every city.
            found_attribute, city_score = self.all_city_data.get(city_name).return_attribute_data(attribute_name)
            # If a score for the attribute is found in the city, use that value. Otherwise, use a default value of 0.
            if found_attribute:
                city_attribute_dict[city_name] = city_score
            else:
                city_attribute_dict[city_name] = 0
                print("WARNING: algorithm, get_attribute_scores_for_all_cities(): Could not find value for"
                      "attribute: {0} in city: {1}. Will default to a score of 0.".format(attribute_name, city_name))
        return city_attribute_dict

    @staticmethod
    def exit_with_error(error):
        print("Error. Exiting with message:\n{0}\n".format(error))
        exit(0)
