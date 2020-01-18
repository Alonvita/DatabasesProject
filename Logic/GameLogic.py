import Queries
import Conventions

DEBUGGING = True

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
<<<<<<< HEAD
    user_id = load_user_id_from_data_base(username)
=======
    user_id = load_user_from_data_base(username,password)
>>>>>>> 986ca718fa2539773d8680f27e374c7ae2d0f027

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
<<<<<<< HEAD
    user_id = load_user_id_from_data_base(username)
=======
    user_id =  Queries.get_user_id_by_name(username)
>>>>>>> 986ca718fa2539773d8680f27e374c7ae2d0f027

    print(properties_dict)
    Queries.add_preferences(user_id, properties_dict)


<<<<<<< HEAD
def load_user_id_from_data_base(username):
    return Queries.get_user_id(str(username))
=======
def load_user_from_data_base(username, password):
    return Queries.get_user_id(str(username), str(password))
>>>>>>> 986ca718fa2539773d8680f27e374c7ae2d0f027


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
<<<<<<< HEAD
    return Queries.get_all_genres()
=======
   """return {
        "a": ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    }"""""
   return Queries.get_all_genres()
>>>>>>> 986ca718fa2539773d8680f27e374c7ae2d0f027


def get_leaderboard():
    leaderboard = dict()

    for game_type in GAME_TYPES:
        leaderboard[game_type] = list()
        leaderboard[game_type].append(['Player name', 'Score'])

        top_players = Queries.get_top_players(game_type)

        for data_list in top_players:
            leaderboard[game_type].append(data_list)

    return leaderboard

    # FORMAT:
    # {
    #     "EASY": [['Player name', 'score'], ['baba', 100], ['gaga', 98], ['jaja', 90]],
    #     "HARD": [['Player name', 'score'], ['nana', 100], ['mama', 96], ['haha', 95]],
    #     "CHALLENGING": [['Player name', 'score'], ['lala', 99], ['tata', 95], ['rara', 90]]
    # }


def start(username, game_type):
    """
    :param username:
    :param game_type:
    :return:
    """

    if DEBUGGING:
        print("The game type received is: {}".format(game_type))

    # create a game depending on the game_type
    if game_type == Conventions.EASY_GAME_CODE or game_type == Conventions.HARD_GAME_CODE:
        if DEBUGGING:
            print("Creating an easy game!")
        return generate_easy_or_hard_games(username, game_type)

    return generate_challenging_game(username, game_type)


def generate_challenging_game(username, game_type):
    return MOCK_CHALLENGING_DICT


def generate_easy_or_hard_games(username, game_type):
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

MOCK_GAME_SCORE = 1200g