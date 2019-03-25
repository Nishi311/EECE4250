import mysql.connector

from src.helper_classes.user_profile import UserProfile
from src.helper_classes.city_data import CityData


class Controller(object):

    def __init__(self):
        self.db_city_table_name = "city_index"

    @staticmethod
    def query_database(table_name, object_name=None):
        """
        Quick query function to get all the data a given SQL database table.
        :param table_name: Name of the table to query in the SQL database.
        :param object_name: Name of the specific object to query. If none given, will return all table entries in table
                            Otherwise, will search for an entry in the table with this name and return only that entry.
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

        # If object_name designated, search for case insensitive string matches in correct column for the table.
        if table_name == "city_index" and object_name:
            cursor.execute("SELECT * FROM {0} WHERE city_name LIKE '{1}'".format(table_name, object_name))
        elif table_name == "users" and object_name:
            cursor.execute("SELECT * FROM {0} WHERE username LIKE '{1}'".format(table_name, object_name))
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

        raw_city_attributes, raw_city_score_list = self.query_database(city_table_name)

        # For city table, first two attributes are city index and name, which we don't care about.
        processed_city_attributes = raw_city_attributes[2:]

        # Create a list of proper CityData objects for consumption by other modules
        processed_city_data = {}
        for index, tuple in enumerate(raw_city_score_list):
            city_name = tuple[1]
            attribute_scores = tuple[2:]
            processed_city_data[city_name] = CityData(city_name, processed_city_attributes, attribute_scores)

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
            processed_user_data[username] = UserProfile(username, password, email, quiz_histoy)

        return processed_user_data

    def query_for_specific_city_data(self, city_name):
        city_table_name = "city_index"

        raw_city_attributes, raw_city_data = self.query_database(city_table_name, city_name)
        raw_city_data = raw_city_data[0]
        # For city table, first two attributes are city index and name, which we don't care about.
        processed_city_attributes = raw_city_attributes[2:]

        # Create a list of proper CityData objects for consumption by other modules
        city_name = raw_city_data[1]
        attribute_scores = raw_city_data[2:]
        city_data_object = CityData(city_name, processed_city_attributes, attribute_scores)

        return city_data_object

    def query_for_specific_user_data(self, username):
        user_table_name = "users"

        user_attributes, raw_user_data = self.query_database(user_table_name, username)
        raw_user_data = raw_user_data[0]
        # Create a list of proper CityData objects for consumption by other modules
        username = raw_user_data[1]
        password = raw_user_data[2]
        email = raw_user_data[3]
        quiz_histoy = raw_user_data[4]

        user_profile_object = UserProfile(username, password, email, quiz_histoy)

        return user_profile_object

    @staticmethod
    def exit_with_error(error):
        print("Error. Exiting with message:\n{0}\n".format(error))
        exit(0)
