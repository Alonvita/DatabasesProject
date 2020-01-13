import Queries

GAME_TYPES = [
    "EASY",
    "HARD",
    "CHALLENGING"
]

QUESTIONS = {
    "Name": "What was the artist's name",
    "Genre": "Which of the following was one of the artist's genres?",
    "Birth_Date": "When was the artist born?",
    "From": "Where was the artist from?",
    "Songs": None
}


PREFERENCES_EXIST_STATUS = 1
PREFERENCES_NON_EXISTING = 0
USER_DOESNT_EXIST = -1
ADD_FAILURE = -1


def login(username, password):
    user_id = load_user_from_data_base(username)

    if user_id == USER_DOESNT_EXIST:
        return USER_DOESNT_EXIST

    user_preferences = Queries.get_preferred_genres(user_id)

    if user_preferences:
        return PREFERENCES_EXIST_STATUS
    else:
        return PREFERENCES_NON_EXISTING


def register(user_name, password):
    """
    adds a new user to the database

    :param user_name:
    :param password:
    :return: 0 if user exists or 1 if user was created
    """
    add_success = 1
    add_fail = 0

    if Queries.add_user(user_name, password) == ADD_FAILURE:
        return add_fail

    return add_success


def add_preferences_to_user(username, properties_list):
    Queries.add_preferences(load_user_from_data_base(username), properties_list)


def load_user_from_data_base(username):
    return Queries.get_user_id(username)


# def end(username, answers_list, game_dict, game_type):
#     answers_list = game.get_answers_list()
#
#     questions_dict = game.get_questions_dict()
#
#     # tag the answer (True/False for right/wrong)
#     answers_list.append(questions_dict[question][True] == answer)
#
#     # check if score should be calculated
#     if len(questions_dict) == answers_list:
#         # tag the game ending time
#         game.set_end_time(self.collect_time_stamp())
#
#         # calculate the score
#         game.set_final_score(
#             self.generate_final_score()(
#                 len(questions_dict),
#                 answers_list.count(True)
#             )
#         )


def generate_questions(user_name, game_type):
    """
    Will generate the questions based on the user artists preferences

    :return:
    """
    user_id = Queries.get_user_id(user_name)

    artists_list = Queries.get_preferred_artists(user_id)
    '''
    format:
        [
            ["artist_name", "gender", "from", "birth_date", [songs_list]] <- artist played on
            ["artist_name", "gender", "from", "birth_date", [songs_list]] <- wrong answers
            ...
        ]
    '''


    pass


def get_all_preferences():
    return Queries.get_all_genres()


def get_leaderboard():
    leaderboard = list()

    for game_type in GAME_TYPES:
        leaderboard.append(Queries.get_top_players(game_type))

    return leaderboard


def start(username, game_type):
    """
    Easy and hard same dict
    Challenging dict: {
        "artist_name": [artists...]
        "properties": [[artist_1_prop], [artist_2_prop], ... TOTAL 5]
        "questions: {
            QUESTIONS DICT (like easy and hard)
        }
    }

    :param username:
    :param game_type:
    :return:
    """

    # TODO: create a game depending on the game_type
    pass


def generate_easy_or_hard_games():
    pass

