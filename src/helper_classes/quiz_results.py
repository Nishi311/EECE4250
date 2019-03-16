
class QuizResults(object):
    def __init__(self, weights):
        if isinstance(weights, dict):
            self.attribute_weights = {}
        else:
            self.exit_with_error("quiz_results, __init__(): object given as answers is not of type dict.")

        self.update_attribute_weights(weights)
        self.city_scores = []

    def return_city_scores(self):
        return self.city_scores

    def return_attribute_weights(self):
        return self.attribute_weights

    def set_city_scores(self, new_results):
        self.city_scores = new_results

    def update_attribute_weights(self, new_weights):
        if isinstance(new_weights, dict):
            self.attribute_weights = new_weights
        else:
            self.exit_with_error("quiz_results, update_attribute_weights(): object given as new_weights is not "
                                 "of type dict.")

    @staticmethod
    def exit_with_error(error):
        print("Error. Exiting with message:\n{0}\n".format(error))
        exit(0)
