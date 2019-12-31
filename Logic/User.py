class User:
    def __init__(self, username, password):
        self._username = username
        self._password = password

        self._preferences_dict = {
            "Genres": None,
            "Songs": None,
            "Artists": None
        }  # it's a dict containing lists as values

        self._games_list = list()  # it's a list of dicts

    def get_username(self):
        return self._username

    def check_password(self, password):
        return self._password == password

    def add_game_score(self, game_type, game_timestamp, final_score):
        """
        :param game_type: the game type
        :param game_timestamp: the time game ended
        :param final_score: the final score
        """
        self._games_list.append({
            "Type": game_type,
            "Timestamp": game_timestamp,
            "Score": final_score
        })

    def get_preferences_dict(self):
        return self._preferences_dict

    def get_preferences_list_for(self, preference_type):
        """

        :param preference_type: the preference type as String
        :return: returns a list of strings associated  with the preference_type
        """
        if preference_type not in self._preferences_dict.keys():
            raise ValueError("Unknown preference type.")

        return self._preferences_dict[preference_type]

    def enlist_preference(self, preference_type, preference):
        """

        :param preference_type:
        :param preference:
        :return:
        """
        if preference_type not in self._preferences_dict.keys():
            self._preferences_dict[preference_type] = list()
            self._preferences_dict[preference_type].append(preference)

        self._preferences_dict[preference_type].append(preference)
