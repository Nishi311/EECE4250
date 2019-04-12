import mysql.connector

from src.helper_classes.user_profile import UserProfile
from src.helper_classes.city_data import CityData
from src.helper_classes.quiz_results import QuizResults
from src.algorithm.algorithm import AlgorithmRunner


class Controller(object):

    def __init__(self):
        self.db_city_table_name = "city_index"

    @staticmethod
    def query_database(table_name, object_info=None):
        """
        Quick query function to get all the data a given SQL database table.
        :param table_name: Name of the table to query in the SQL database.
        :param object_info: (list): List of info necessary to query an object from the given table.. If none given, will
                                    return all table entries in table. Otherwise, will search for an entry in the table
                                    with the matching values and return only that entry.
        :return: {list<String>, list<Map>) ->  Tuple of the list of table labels and their values.
                       False -> Failed to acquire data from database.
        """
        connection = mysql.connector.connect(host="yuppie-city-simulator-db.cohu57vlr7rd.us-east-2.rds.amazonaws.com",
                                             user="MeanderingArma",
                                             passwd="Dillos1999",
                                             database="YCS")
        cursor = connection.cursor()
        cursor.execute("describe {0}".format(table_name))
        # Gets the whole list of tuples related to table values.
        # e.g: [('city_id', 'int(11)', 'NO', 'PRI', None, 'auto_increment'),
        #       ('city_name', 'varchar(32)', 'NO', '', None, '')
        #       ('walkability', 'double', 'YES', '', None, ''),
        #       ...]
        table_labels_full = cursor.fetchall()

        # Cut out the fat and make a list of only the names of attributes.
        table_labels_min = []
        for index, tuple in enumerate(table_labels_full):
            table_labels_min.append(tuple[0])

        # If object_info designated, search for case insensitive string matches in correct column for the table.
        if table_name == "city_index" and object_info:
            cursor.execute(
                "SELECT * FROM {0} WHERE city_name LIKE '{1}'".format(table_name, object_info[0]))
        elif table_name == "users" and object_info:
            cursor.execute(
                "SELECT * FROM {0} WHERE user_id = '{1}'".format(table_name, object_info[0]))
        elif table_name == "results":
            if len(object_info) == 1:
                cursor.execute(
                    "SELECT * FROM {0} WHERE user_id = '{1}'".format(table_name, object_info[0]))
            elif len(object_info) == 2:
                cursor.execute("SELECT * FROM {0} WHERE (user_id = '{1}' AND quiz_id = '{2}')".format(table_name,
                                                                                                      object_info[0],
                                                                                                      object_info[1]))

        # Gets the whole list of table entries in the following format (index, table data...):
        # e.g: [(1, 'New York', 89.2, 84.3, 28317.0, 67.7, 20320876.0, 1448.59, 538.9, 57.08),
        #       (2, 'Los Angeles', 67.4, 52.6, 8484.0, 55.1, 13353907.0, 2535.92, 761.31, 60.35),
        #       (3, 'Chicago', 77.8, 65.3, 11900.0, 71.5, 9533040.0, 3263.8, 1098.86, 41.03),
        #       ...]
        else:
            cursor.execute("SELECT * FROM {0}".format(table_name))
        table_values = cursor.fetchall()

        if table_values:
            return table_labels_min, table_values
        else:
            print("algorithm, query_database(): No data acquired from database in table "
                  "{0}".format(table_name))
            return False

    def query_for_all_city_data(self):
        city_table_name = "city_index"

        raw_city_attributes, raw_city_score_list = self.query_database(
            city_table_name)

        # For city table, first two attributes are city index and name, which we don't care about.
        processed_city_attributes = raw_city_attributes[2:]

        # Create a list of proper CityData objects for consumption by other modules
        processed_city_data = {}
        for index, tuple in enumerate(raw_city_score_list):
            city_index = tuple[0]
            city_name = tuple[1]
            attribute_scores = tuple[2:]
            processed_city_data[city_name] = CityData(
                city_index, city_name, processed_city_attributes, attribute_scores)

        return processed_city_data

    def query_for_all_user_data(self):
        user_table_name = "users"

        user_attributes, raw_user_data = self.query_database(user_table_name)

        # Create a list of proper CityData objects for consumption by other modules
        processed_user_data = {}
        for index, tuple in enumerate(raw_user_data):
            username = tuple[1]
            password = tuple[2]
            email = tuple[3]
            quiz_histoy = tuple[4]
            processed_user_data[username] = UserProfile(
                username, password, email, quiz_histoy)

        return processed_user_data

    def query_for_specific_city_data(self, city_name, table_name=None):
        if table_name:
            city_table_name = table_name
        else:
            city_table_name = "city_index"
        raw_city_attributes, raw_city_data = self.query_database(
            city_table_name, [city_name])
        raw_city_data = list(raw_city_data[0])
        # For city table, first two attributes are city index and name, which we don't care about.
        processed_city_attributes = raw_city_attributes[2:]

        # Create a list of proper CityData objects for consumption by other modules
        city_id = raw_city_data[0]
        city_name = raw_city_data[1]
        attribute_scores = raw_city_data[2:]
        city_data_object = CityData(
            city_id, city_name, processed_city_attributes, attribute_scores)

        return city_data_object

    def query_for_specific_user_data(self, user_id):
        user_table_name = "users"

        user_attributes, raw_user_data = self.query_database(
            user_table_name, [user_id])
        raw_user_data = list(raw_user_data[0])

        username = raw_user_data[1]
        email = raw_user_data[2]
        password = raw_user_data[3]

        user_profile_object = UserProfile(user_id, username, password, email)

        list_of_user_quizzes = self.query_for_specific_user_all_quizzes(
            user_id)
        for quiz in list_of_user_quizzes:
            user_profile_object.add_new_quiz(quiz)

        return user_profile_object

    def query_for_specific_user_all_quizzes(self, user_id):
        results_table_name = "results"

        potential_result = self.query_database(results_table_name, [user_id])

        if isinstance(potential_result, list):
            quiz_attributes = potential_result[0]
            raw_quiz_results = potential_result[1]

            # First two attributes in results are user_id and quiz_id. Not needed for Result object generation
            quiz_attributes = quiz_attributes[2:]
            # last item is scores, drop that as well
            quiz_attributes = quiz_attributes[:len(quiz_attributes)-1]

            list_of_quiz_objects = []
            for quiz in raw_quiz_results:
                quiz_result_list = list(quiz)

                # First two attributes in quiz result list are values for user_id and quiz_id. Nab quiz_id then cull both.
                quiz_id = quiz_result_list[1]
                quiz_result_list = quiz_result_list[2:]

                # Last item is the list of city results (if given), grab those too then cut them off.
                quiz_cities = quiz_result_list[len(quiz_result_list)-1]
                quiz_result_list = quiz_result_list[:len(quiz_result_list)-1]

                quiz_result_dict = {}

                if len(quiz_result_list) == len(quiz_attributes):
                    for index in range(len(quiz_attributes)):
                        quiz_result_dict[quiz_attributes[index]
                                         ] = quiz_result_list[index]

                    quiz_result_object = QuizResults(quiz_result_dict)
                    quiz_result_object.update_city_scores(quiz_cities)
                    quiz_result_object.update_quiz_id(quiz_id)
                    list_of_quiz_objects.append(quiz_result_object)
                else:
                    self.exit_with_error("Controller, Query_for_specific_user_all_quizzes(): Something went wrong and "
                                         "the number of attributes do not match the number of data points retrieved")
            return list_of_quiz_objects
        else:
            return []

    def query_for_specific_user_quiz_id(self, user_id, quiz_id):
        results_table_name = "results"

        quiz_attributes, raw_quiz_results = self.query_database(
            results_table_name, [user_id, quiz_id])
        quiz_attributes = quiz_attributes[2:]

        quiz_results = list(raw_quiz_results[0])

        quiz_result_dict = {}
        for index in range(len(quiz_attributes)):
            quiz_result_dict[quiz_attributes[index]] = quiz_results[index]

        quiz_results_object = QuizResults(quiz_result_dict)
        quiz_results_object.update_quiz_id(quiz_id)

        return quiz_results_object

    @staticmethod
    def store_in_database(table_name, insert_key_names, insert_values):
        formatted_key_string = "({0})".format(", ".join(insert_key_names))
        formatted_value_string = "("

        for value in insert_values:
            formatted_value_string += "\'{0}\', ".format(value)
        formatted_value_string = formatted_value_string.rsplit(", ", 1)[
            0] + ")"

        connection = mysql.connector.connect(host="yuppie-city-simulator-db.cohu57vlr7rd.us-east-2.rds.amazonaws.com",
                                             user="MeanderingArma",
                                             passwd="Dillos1999",
                                             database="YCS")

        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO {0} {1} VALUES {2}".format(
                table_name, formatted_key_string, formatted_value_string))
            connection.commit()
            return True
        except Exception:
            return False

    def store_new_quiz(self, user_id, quiz_results):
        results_table_name = "results"
        # Ensure that what we get is a quiz result object
        if isinstance(quiz_results, QuizResults):
            # pull the parameter list and their corresponding values list for storage
            quiz_results_parameters = quiz_results.return_storage_parameter_names()
            quiz_results_values = quiz_results.return_storage_parameter_values()

            # Quiz value lists don't come from the website with userID, so add that here before shoving it
            # into the database.
            quiz_results_values[0] = user_id

            if self.store_in_database(results_table_name, quiz_results_parameters, quiz_results_values):
                return True
            else:
                return False

    def run_quiz_workflow(self, attribute_dict, alternate_city_data=None):
        """
        Runs the full quiz workflow from raw QuizResult object creation to algorithm calculation to result storage
        to returning dictionaries required to run the UI pages.
        :param attribute_dict: (Dict) -> [Attribute Name: Attribute Value] Key-Value pairs corresponding to user-given
                                         weights for calculation.
        :param alternate_city_data: (Dict) -> OPTIONAL: [City Name: City Object] Key-Value pairs if you don't want
                                              to use the database stuff. Basically just for unit testing
        :return: [list of city objects of top 5 cities, dict of [City Name: City Score] key-value pairs] These two
                 items are all that's required to run the front end view results page.
        """

        raw_quiz_results_object = QuizResults(attribute_dict)
        all_city_data = alternate_city_data if alternate_city_data else self.query_for_all_city_data()

        processed_quiz_results = AlgorithmRunner().run_module(
            raw_quiz_results_object, all_city_data)
        # TODO: Ask nick about how to get the actual user ID
        if not self.store_new_quiz(9999, processed_quiz_results):
            self.exit_with_error(
                "Controller.py, run_quiz_workflow(): Failed to store quiz in database")

        top_city_object_list = []
        city_scores_dict = {}
        for city_name, city_score in processed_quiz_results.return_city_scores():
            if alternate_city_data:
                top_city_object_list.append(alternate_city_data[city_name])
            else:
                top_city_object_list.append(self.query_for_specific_city_data(
                    city_name, "city_index_raw").retrieve_all_city_data())
            city_scores_dict[city_name] = int(city_score)

        return [top_city_object_list, city_scores_dict]

    @staticmethod
    def exit_with_error(error):
        print("Error. Exiting with message:\n{0}\n".format(error))
        exit(0)
