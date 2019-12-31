import datetime


class LogicGenerator:
    def __init__(self, user, game):
        self._game = game
        self._user = user

    def question_answered(self, question, answer):
        answers_list = self._game.get_answers_list()
        questions_dict = self._game.get_questions_dict()

        # tag the answer (True/False for right/wrong)
        answers_list.append(questions_dict[question][True] == answer)

        # check if score should be calculated
        if len(questions_dict) == answers_list:
            # tag the game ending time
            self._game.set_end_time(self.collect_time_stamp())

            # calculate the score
            self._game.set_final_score(
                self.generate_final_score()(
                    len(questions_dict),
                    answers_list.count(True)
                )
            )

    def generate_properties(self, properties_number):
        """
        Will generate the properties from DB based on the user preferences

        :param properties_number:
        :return:
        """
        pass

    def generate_questions(self, questions_number):
        """
        Will generate the questions based on the user artists preferences
        :return:
        """
        pass

    @staticmethod
    def collect_time_stamp():
        return datetime.datetime.now()

    @staticmethod
    def generate_final_score():
        return lambda correct_answers, questions: (correct_answers / questions) * 100

    @staticmethod
    def generate_artists_list(number_of_artists):
        pass
