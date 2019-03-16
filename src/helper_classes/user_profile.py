
class UserProfile(object):
    def __init__(self):
        self.username = ""
        self.password = ""
        self.email = ""
        self.quiz_history = []

    def get_credentials(self):
        return self.username, self.password

    def get_quiz_results(self):
        return self.quiz_results

    def overwrite_credentials(self, new_username, new_password):
        self.username = new_username
        self.password = new_password

    def add_new_quiz(self, new_result):
        self.quiz_history.append(new_result)
