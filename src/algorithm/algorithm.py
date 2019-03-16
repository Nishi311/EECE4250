import sqlite3
from ..helper_classes.quiz_results import QuizResults


class AlgorithmRunner(object):

    def __init__(self):
        self.result_cities = {}
        self.all_city_data = {}
        self.all_city_names = []
        self.database_name = ""
        self.db_city_table_name = ""
        self.num_cities_to_return = 5

    def run_module(self, current_quiz):
        if isinstance(current_quiz, QuizResults):
            self.query_database()
            current_quiz.set_city_scores(self.compute_results(current_quiz))
        else:
            self.exit_with_error("algorithm, run_module(): object passed as current_quiz is NOT of class Quiz "
                                 "Answers.")
        return current_quiz

    def query_database(self, database_name, table_name):
        """
        Quick query function to get all the city data from the SQL database.
        :param database_name: Name of the SQL database to query.
        :param table_name: Name of the table to query in the SQL database.
        :return: bool: True -> Successfully acquired data from database.
                       False -> Failed to acquire data from database.
        """
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM {0}",format(table_name))
        self.all_city_data = cursor.fetchall()

        if self.all_city_data:
            self.all_city_names = list(self.all_city_data.keys())
            return True
        else:
            self.exit_with_error("algorithm, query_database(): Failed to acquire data from database {0} in table "
                                 "{1}".format(database_name, table_name))
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
            # Sort the cities by total score from greatest to least
            ordered_cities = sorted(total_city_scores.items(), key=lambda kv: kv[1], reverse=True)
            # Return the top X number of cities, as designated by algorithm parameters.
            return ordered_cities[:self.num_cities_to_return]
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
