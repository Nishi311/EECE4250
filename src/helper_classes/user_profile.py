
class UserProfile(object):
    def __init__(self, user_id, username, password, email, quiz_history=None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        if quiz_history:
            self.quiz_history = quiz_history
        else:
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
