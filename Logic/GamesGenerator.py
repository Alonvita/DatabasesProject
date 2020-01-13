from Logic.LogicUtilities import LogicUtilities as lG


class GamesGenerator:
    def __init__(self):
        self._games_type_dict = {
            "EASY": None,
            "HARD": None,
            "CHALLENGING": None
        }

        self._logic_generator = lG()

    def start(self, game_type, user_name):
        if game_type not in self._games_type_dict:
            raise ValueError("Unknown game type: " + game_type)

        # TODO: pull from database the dictionary and pass it to Itai

