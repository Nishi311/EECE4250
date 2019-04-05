
class QuizResults(object):
    def __init__(self, weights):

        self.quiz_id = None
        self.user_id = None

        if isinstance(weights, dict):
            self.attribute_weights = {}
        else:
            self.exit_with_error("quiz_results, __init__(): object given as answers is not of type dict.")

        self.update_attribute_weights(weights)
        self.city_scores = []

    def return_quiz_id(self):
        return self.quiz_id

    def return_city_scores(self):
        return self.city_scores

    def return_calculation_attribute_set(self):
        return self.attribute_weights

    def update_quiz_id(self, new_quiz_id):
        self.quiz_id = new_quiz_id

    def update_user_id(self, new_user_id):
        self.user_id = new_user_id

    def update_city_scores(self, city_string):
        if city_string:
            individual_city_list = city_string.split(", ")
            city_score_list = []
            for city in individual_city_list:
                city_name = city.split(":")[0]
                city_score = float(city.split(":")[1])
                city_score_list.append([city_name, city_score])

            self.city_scores = city_score_list
        else:
            self.exit_with_error("quiz_results, update_city_scores(): ERROR city_string passed NULL.")

    def update_attribute_weights(self, new_weights):
        if isinstance(new_weights, dict):
            self.attribute_weights = new_weights
        else:
            self.exit_with_error("quiz_results, update_attribute_weights(): object given as new_weights is not "
                                 "of type dict.")

    def return_storage_parameter_names(self):
        return_list = ["user_id", "quiz_id"]

        for name, value in self.attribute_weights.items():
            return_list.append(name)

        return_list.append("scores")
        return return_list

    def return_storage_parameter_values(self):
        return_list = [self.user_id, self.quiz_id]
        for name, value in self.attribute_weights.items():
            return_list.append(value)
        return_list.append(self.print_cities())
        return return_list

    def print_cities(self):
        return_string = ""
        for city_bundle in self.city_scores:
            return_string += "{0}:{1}, ".format(city_bundle[0], city_bundle[1])

        return_string = return_string.rsplit(", ", 1)[0]
        return return_string

    @staticmethod
    def exit_with_error(error):
        print("Error. Exiting with message:\n{0}\n".format(error))
        exit(0)
