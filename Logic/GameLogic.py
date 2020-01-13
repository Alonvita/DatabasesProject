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

    print("Game logic: "+user_name+" "+password)
    if Queries.add_user(user_name, password) == ADD_FAILURE:
        return add_fail

    return add_success


def add_preferences_to_user(username, properties_dict):
    user_id = load_user_from_data_base(username)

    print(properties_dict)
    Queries.add_preferences(user_id, properties_dict)


def load_user_from_data_base(username):
    return Queries.get_user_id(str(username))


def end(username, answers_list, game_dict, game_type):
    return MOCK_GAME_SCORE
    # answers_list = game.get_answers_list()
    #
    # questions_dict = game.get_questions_dict()
    #
    # # tag the answer (True/False for right/wrong)
    # answers_list.append(questions_dict[question][True] == answer)
    #
    # # check if score should be calculated
    # if len(questions_dict) == answers_list:
    #     # tag the game ending time
    #     game.set_end_time(self.collect_time_stamp())
    #
    #     # calculate the score
    #     game.set_final_score(
    #         self.generate_final_score()(
    #             len(questions_dict),
    #             answers_list.count(True)
    #         )
    #     )


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
    return {
        "a": ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    }

    # return Queries.get_all_genres()


def get_leaderboard():

    return {
        "EASY": [['Player name', 'score'], ['baba', 100], ['gaga', 98], ['jaja', 90]],
        "HARD": [['Player name', 'score'], ['nana', 100], ['mama', 96], ['haha', 95]],
        "CHALLENGING": [['Player name', 'score'], ['lala', 99], ['tata', 95], ['rara', 90]]
    }

    # leaderboard = dict()
    #
    # for game_type in GAME_TYPES:
    #     leaderboard[game_type] = Queries.get_top_players(game_type)
    #
    # return leaderboard


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
    if game_type == "EASY" or game_type == "HARD":
        return generate_easy_or_hard_games()

    return generate_challenging_game()


def generate_challenging_game():
    return MOCK_CHALLENGING_DICT


def generate_easy_or_hard_games():
    return MOCK_DICT


MOCK_DICT = {
        "artist_name": "Adel",
        "properties": ["Country: UK", "Date: 12.12.1980", "Song1: Alon kaka", "Song2: Sara kaka", "Song3: Yana kaka"],
        "questions": {
            "q1": {
                "text": "Country?",
                "answers": ["Israel", "USA", "Poland", "UK"],
                "true": "UK"
            },
            "q2": {
                "text": "Date?",
                "answers": ["12.12.1984", "12.12.1979", "12.12.1980", "12.12.1981"],
                "true": "12.12.1980"
            },
            "q3": {
                "text": "Song1?",
                "answers": ["song1_a1", "song1_a2", "song1_a3", "Alon kaka"],
                "true": "right_answer"
            },
            "q4": {
                "text": "Song2?",
                "answers": ["song2_a1", "song2_a2", "Sara kaka", "song2_a3"],
                "true": "right_answer"
            },
            "q5": {
                "text": "Song3?",
                "answers": ["Yana kaka", "song3_a1", "song3_a2", "song3_a3"],
                "true": "Yana kaka"
            }
        }
    }


MOCK_CHALLENGING_DICT = GameInfoDict = {
        "artist_name": ["Adel", "Adel2", "Adel3", "Ade4", "Adel5"],
        "properties": [["Country: UK", "Date: 12.12.1980", "Song1: Alon kaka", "Song2: Sara kaka", "Song3: Yana kaka"], ["Country1: UK", "Date1: 12.12.1980", "Song11: Alon kaka", "Song12: Sara kaka", "Song13: Yana kaka"], ["Country2: UK", "Date2: 12.12.1980", "Song21: Alon kaka", "Song22: Sara kaka", "Song23: Yana kaka"], ["Country3: UK", "Date3: 12.12.1980", "Song31: Alon kaka", "Song32: Sara kaka", "Song33: Yana kaka"], ["Country4: UK", "Date4: 12.12.1980", "Song41: Alon kaka", "Song42: Sara kaka", "Song43: Yana kaka"]],
        "questions": {
            "q1": {
                "text": "Country?",
                "answers": ["Israel", "USA", "Poland", "UK"],
                "true": "UK"
            },
            "q2": {
                "text": "Date?",
                "answers": ["12.12.1984", "12.12.1979", "12.12.1980", "12.12.1981"],
                "true": "12.12.1980"
            },
            "q3": {
                "text": "Song1?",
                "answers": ["song1_a1", "song1_a2", "song1_a3", "Alon kaka"],
                "true": "right_answer"
            },
            "q4": {
                "text": "Song2?",
                "answers": ["song2_a1", "song2_a2", "Sara kaka", "song2_a3"],
                "true": "right_answer"
            },
            "q5": {
                "text": "Song3?",
                "answers": ["Yana kaka", "song3_a1", "song3_a2", "song3_a3"],
                "true": "Yana kaka"
            }
        }
    }

MOCK_GAME_SCORE = 1200