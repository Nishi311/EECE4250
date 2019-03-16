
class QuizResults(object):
    def __init__(self, answers):

        self.answers = {}
        self.update_answers(answers)
        self.city_results = []

    def return_results(self):
        return self.city_results

    def return_answers(self):
        return self.answers

    def set_results(self, new_results):
        self.city_results = new_results

    def update_answers(self, new_answers):
        if isinstance(new_answers, dict):
            self.answers = new_answers
        else:
            self.exit_with_error("quiz_results, __init__(): object given as new_answers is not of type dict.")

    @staticmethod
    def exit_with_error(error):
        print("Error. Exiting with message:\n{0}\n".format(error))
        exit(0)
