import random
import Queries
import Conventions

TESTING = True
DEBUGGING = True
PLAYING_ARTIST_OFF_SET = 0
NAME_OFF_SET = 0
GENDER_OFF_SET = 1
FROM_OFF_SET = 2
BIRTH_DATE_OFF_SET = 3
SONGS_LIST_OFF_SET = 4


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
    user_id = load_user_from_data_base(username, password)

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
    user_id = load_user_id_only_by_name(username)
    user_id = Queries.get_user_id_by_name(username)

    print(properties_dict)
    Queries.add_preferences(user_id, properties_dict)


def load_user_id_only_by_name(username):
    return Queries.get_user_id_by_name(str(username))


def load_user_from_data_base(username, password):
    return Queries.get_user_id(str(username), str(password))


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


def generate_questions(raw_artists_dict):
    """
    Will generate the questions based on the user artists preferences

    :return:
    """
    questions_map = {
        "from": generate_origin_question,
        "genre": generate_genre_question,
        "birth_date": generate_birth_date_question,
        "similar": generate_similar_artists_question
    }

    questions = [questions_map['from'](raw_artists_dict),
                 questions_map['genre'](raw_artists_dict),
                 questions_map['birth_date'](raw_artists_dict),
                 questions_map['Similar'](raw_artists_dict)
                 ]  # TODO: add the rest of the questions to here
    random.shuffle(questions)  # shuffle

    build_questions_dict_for_view(questions)

    # build and return the questions dict
    return build_questions_dict_for_view(questions)


def build_questions_dict_for_view(questions_list):
    """
    builds the questions dict from the questions list. Inserts question_name: question per not None value.

    :param questions_list:
    :return:
    """
    questions_dict = dict()

    for question in questions_list:
        # index of the question
        index = 1

        # insert question if it is not None
        if question:
            question_name = "q" + str(index)

            questions_dict[question_name] = question
            # increase index, as question was inserted to dict
            index += 1

    return questions_dict


def none_values_exist_in_answer_list(answers_list):
    for answer in answers_list:
        if answer is None:
            return True

    return False


def answers_list_empty_or_less_than_three_songs(answers_list):
    return answers_list == Conventions.EMPTY_ANSWERS_LIST_CODE or \
           len(answers_list) != Conventions.VALID_SONGS_ANSWERS_LIST_SIZE


def generate_origin_question(raw_artists_dict):
    question_text = "Where is the artist from?"  # text
    answers = [artist[FROM_OFF_SET] for artist in raw_artists_dict['Artist']]  # list of all origins

    if none_values_exist_in_answer_list(answers):
        return None

    if answers_list_empty_or_less_than_three_songs(answers):
        return None

    right_answer = raw_artists_dict['Artist'][PLAYING_ARTIST_OFF_SET][FROM_OFF_SET]  # the origin of the playing artist

    return build_question_dict(question_text, answers, right_answer)


def generate_birth_date_question(raw_artists_dict):
    question_text = "What is the artist's birth date?"
    answers = [artist[BIRTH_DATE_OFF_SET] for artist in raw_artists_dict['Artist']]

    if none_values_exist_in_answer_list(answers):
        return None

    if answers_list_empty_or_less_than_three_songs(answers):
        return None

    right_answer = answers[0]

    return build_question_dict(question_text, answers, right_answer)


def generate_genre_question(raw_artists_dict):
    # create the list of genres by order of artists
    list_of_genres = [Queries.get_genre_by_artist(artist_name) for artist_name in raw_artists_dict['Artist'][NAME_OFF_SET]]
    genres_list_sizes = [len(lst) for lst in list_of_genres]

    genres_for_question = list()

    # randomly pick a genre from the list of genres per artist
    for genres_list in list_of_genres:
        genres_for_question.append(genres_list[random.randint(0, len(genres_list - 1))])

    # check for None values
    if none_values_exist_in_answer_list(genres_for_question):
        return None

    if answers_list_empty_or_less_than_three_songs(genres_for_question):
        return None

    question_text = "What is the artist's genre?"
    right_answer = genres_for_question[0]

    return build_question_dict(question_text, genres_for_question, right_answer)


def generate_similar_artists_question(raw_artists_dict):
    # artist name
    artist_name = raw_artists_dict['Artist'][NAME_OFF_SET]

    question_text = "Who is the most similar artist to this artist?"

    # generate genres from db
    genres_of_the_artist = Queries.get_genre_by_artist(artist_name)

    # generate similar artist by randomly picking a genre of similarity
    similar_artist_list = Queries.get_similar_artist(artist_name)

    # randomply pick a similar artist from the similar_artits_list
    similar_artist = similar_artist_list[random.randint(0, len(similar_artist_list) - 1)]

    answers = [artist_name for artist_name in raw_artists_dict['Artist'][NAME_OFF_SET]]
    answers = answers[1:]  # remove the name of the artist we are playing on
    answers.append(similar_artist)  # append the name of the similar artist

    # check None values
    if none_values_exist_in_answer_list(answers):
        return None

    if answers_list_empty_or_less_than_three_songs(answers):
        return None

    return build_question_dict(question_text, answers, similar_artist_list)


def build_question_dict(text, answers, right_answer):
    return {
        "text": text,
        "answers": answers,
        "true": right_answer
    }


def get_all_preferences():
    return Queries.get_all_genres()


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


def generate_challenging_game(user_name, game_type):
    user_id = Queries.get_user_id_by_name(user_name)  # generate user ID

    raw_artists_dict = Queries.get_preferred_artists(user_id, game_type)  # generate raw artists dict

    # generate artists list
    artists_list = [artist[NAME_OFF_SET] for artist in raw_artists_dict['Artist']]

    # generate the properties list
    properties_list_for_each_artist = list()

    for artist in raw_artists_dict['Artist']:
        # create a list per artist
        list_for_artist = list()

        # append relevant information
        list_for_artist.append(artist[PLAYING_ARTIST_OFF_SET][FROM_OFF_SET])  # from
        list_for_artist.append(artist[PLAYING_ARTIST_OFF_SET][BIRTH_DATE_OFF_SET])  # birth date

        for song in artist[SONGS_LIST_OFF_SET]:
            list_for_artist.append(song)  # append all songs

        properties_list_for_each_artist.append(list_for_artist)

    if not TESTING:
        return {
            "artist name": artists_list,
            "properties": properties_list_for_each_artist,
            "questions": generate_questions(raw_artists_dict)
        }
    else:
        return MOCK_CHALLENGING_DICT


def generate_easy_or_hard_games(user_name, game_type):
    user_id = Queries.get_user_id_by_name(user_name)  # generate user ID

    raw_artists_dict = Queries.get_preferred_artists(user_id, game_type)  # generate raw artists dict
    print(raw_artists_dict)
    '''
    format:
        { 'Artist':
            ["artist_name", "gender", "from", "birth_date", [songs_list]] <- artist played on
            ["artist_name", "gender", "from", "birth_date", [songs_list]] <- wrong answers
            ...
        }
    '''
    
    print(raw_artists_dict)
    # generate the properties list
    properties = list()
    properties.append(raw_artists_dict['Artist'][PLAYING_ARTIST_OFF_SET][FROM_OFF_SET])  # from
    properties.append(raw_artists_dict['Artist'][PLAYING_ARTIST_OFF_SET][BIRTH_DATE_OFF_SET])  # birth date

    # append all songs
    for song in raw_artists_dict['Artist'][SONGS_LIST_OFF_SET]:
        properties.append(song)

    if not TESTING:
        return {
            "artist name": raw_artists_dict['Artist'][PLAYING_ARTIST_OFF_SET][NAME_OFF_SET],
            "properties": properties,
            "questions": generate_questions(raw_artists_dict)
        }
    else:
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