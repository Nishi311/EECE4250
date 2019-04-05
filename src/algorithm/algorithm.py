
from src.helper_classes.quiz_results import QuizResults
from src.controller.Controller import Controller


class AlgorithmRunner(object):

    def __init__(self):
        self.result_cities = {}
        self.all_city_data = {}
        self.all_city_names = []
        self.db_city_table_name = "city_index"
        self.num_cities_to_return = 5
        self.controller = Controller()

    def run_module(self, current_quiz):
        if isinstance(current_quiz, QuizResults):
            self.all_city_data = self.controller.query_for_all_city_data()
            current_quiz.update_city_scores(self.compute_results(current_quiz))
        else:
            self.exit_with_error("algorithm, run_module(): object passed as current_quiz is NOT of class Quiz "
                                 "Answers.")
        return current_quiz

    def compute_results(self, current_quiz):
        if isinstance(current_quiz, QuizResults):

            # Initialize total city scores to 0.
            total_city_scores = {}
            for city_name in self.all_city_data:
                total_city_scores[city_name] = 0

            # Get the list of all the attributes that the quiz used.
            attribute_weights = current_quiz.return_attribute_weights()

            for attribute_name in attribute_weights.keys():
                # For each attribute used in the quiz, get the dict with every city's score for that attribute
                attribute_scores_for_all_cities = self.get_attribute_scores_for_all_cities(attribute_name)
                # Update each cities score with simple formula:
                # city score = (existing score) + (weight of current attribute) * (score for the city in current attribute)
                # TODO: Get more fancy with this scoring system in the future.
                for city_name in self.all_city_data:
                    total_city_scores[city_name] += attribute_weights[attribute_name] * attribute_scores_for_all_cities[city_name]
            # Sort the cities by total score from greatest to least and cut down to top X number of cities
            ordered_cities = sorted(total_city_scores.items(), key=lambda kv: kv[1], reverse=True)
            ordered_cities = ordered_cities[:self.num_cities_to_return]

            # The final returned list of cities will actually be a string of pattern:
            # "[city name]:[city score], [city name]:[city score]"

            return_string = ""
            for city_name, city_value in ordered_cities:
                return_string += "{0}:{1}, ".format(city_name, city_value)
            return_string = return_string.rsplit(", ", 1)[0]

            return return_string
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

        for city_name in self.all_city_data:
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
