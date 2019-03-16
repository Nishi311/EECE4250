import sqlite3
import from ..helper_classes.quiz_results import QuizResults

class AlgorithmRunner(object):

    def __init__(self):
        self.result_cities = {}
        self.all_city_data = {}
        self.database_name = ""
        self.db_city_table_name = ""

    def run_module(self, current_quiz):
        if isinstance(current_quiz, QuizResults):
            self.query_database()
            current_quiz.set_results(self.compute_result(current_quiz))
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
            return True
        else:
            self.exit_with_error("algorithm, query_database(): Failed to acquire data from database {0} in table "
                                 "{1}".format(database_name, table_name))
            return False

    def compute_result(self, current_quiz):
        if isinstance(current_quiz, QuizResults):
            attribute_weights = current_quiz.return_answers()

            city_names = list(self.all_city_data.keys())

            for attribute_weights in attribute_weights:


        else:
            self.exit_with_error("algorithm, compute_result(): object passed as current_quiz is NOT of class Quiz "
                                 "Answers.")
        return
    @staticmethod
    def exit_with_error(error):
        print("Error. Exiting with message:\n{0}\n".format(error))
        exit(0)
