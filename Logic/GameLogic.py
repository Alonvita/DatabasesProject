import sys
import random
import Queries
import Conventions
import DebuggingConventions


def login(username, password):
    """
    loads the login logic

    :param username:
    :param password:
    :return: whether the user exists or not, and if so, whether DB holds his prederences or not
    """
    user_id = load_user_from_data_base(username, password)

    if user_id == Conventions.USER_DOESNT_EXIST:
        return Conventions.USER_DOESNT_EXIST

    user_preferences = Queries.get_preferred_genres(user_id)

    if user_preferences:
        return Conventions.PREFERENCES_EXIST_STATUS
    else:
        return Conventions.PREFERENCES_NON_EXISTING


def register(user_name, password):
    """
    adds a new user to the database

    :param user_name:
    :param password:
    :return: 0 if user exists or 1 if user was created
    """
    add_success = 1
    add_fail = 0

    print("Game logic: " + user_name + " " + password)
    if Queries.add_user(user_name, password) == Conventions.ADD_FAILURE:
        return add_fail

    return add_success


def add_preferences_to_user(username, properties_dict):
    """
    adds a preference to the user in the DB

    :param username:
    :param properties_dict:
    :return:
    """
    user_id = load_user_id_only_by_name(username)

    if DebuggingConventions.GENERALLY_DEBUGGING_GAME_LOGIC:
        print(properties_dict)
    Queries.add_preferences(user_id, properties_dict)


def load_user_id_only_by_name(username):
    """
    returns the user id from the db by his name
    :param username:
    :return:
    """
    return Queries.get_user_id_by_name(str(username))


def load_user_from_data_base(username, password):
    """
    loads the user id from database by name and password
    :param username:
    :param password:
    :return:
    """
    return Queries.get_user_id(str(username), str(password))


def calculate_final_score(answers_list, game_dict, game_type):
    """
    calcualtes the game final score from the scoring conventions
    :param answers_list:
    :param game_dict:
    :param game_type:
    :return:
    """
    final_score = 0
    q_index = 0

    if DebuggingConventions.DEBUGGING_GAME_END:
        print("at 'calculate_final_score'")

    for question in game_dict['questions'].values():
        if DebuggingConventions.DEBUGGING_GAME_END:
            print("\tquestion: {}".format(question))
            print("\tquestion['true']: {}\n\tanswer: {}".format(question['true'],
                                                                answers_list[q_index]))

        if question['true'] == answers_list[q_index]:
            final_score += Conventions.POINTS_TO_ADD[game_type]
            if DebuggingConventions.DEBUGGING_GAME_END:
                print("Adding {} points on right answer: {}".format(
                    Conventions.POINTS_TO_ADD[game_type], answers_list[q_index]))

        q_index += 1

    return final_score


def end(username, answers_list, game_dict, game_type):
    """
    takes care of the game end logic: adds the game to the DB

    :param username:
    :param answers_list:
    :param game_dict:
    :param game_type:
    :return:
    """
    if DebuggingConventions.DEBUGGING_GAME_END:
        print("Game ended with the following stats:\n\tusername: {}\n\tanswers_list{}\n\tgame_type: {}".format(username, answers_list, game_type))

    final_score = calculate_final_score(answers_list, game_dict,
                                        Conventions.GAME_TYPES_CODE_FROM_VIEW_TO_STRING[game_type])

    if not DebuggingConventions.TESTING_VIEW:
        # get user ID
        user_id = load_user_id_only_by_name(username)

        # save the game
        Queries.add_game(Conventions.GAME_TYPES_CODE_FROM_VIEW_TO_STRING[game_type], final_score, user_id)

        # return final score
        return final_score
    else:
        return Conventions.MOCK_GAME_SCORE


def generate_questions(raw_artists_dict, game_type):
    """
    Will generate the questions based on the user artists preferences

    :return:
    """
    questions_map = {
        Conventions.FROM: generate_origin_question,
        Conventions.GENRE: generate_genre_question,
        Conventions.BIRTH_DATE: generate_birth_date_question,
        Conventions.SIMILAR: generate_similar_artists_question,
        Conventions.NAME: generate_name_question
    }

    # add questions
    questions = [questions_map[Conventions.FROM](raw_artists_dict, game_type),
                 questions_map[Conventions.GENRE](raw_artists_dict, game_type),
                 questions_map[Conventions.BIRTH_DATE](raw_artists_dict, game_type),
                 questions_map[Conventions.SIMILAR](raw_artists_dict, game_type)
                 ]

    # add songs questions
    songs_questions = generate_songs_questions(raw_artists_dict, game_type)

    if DebuggingConventions.DEBUGGING_SONGS_LIST_CREATION:
        for songs_question in songs_questions:
            print("Song question generated is: {}".format(songs_question))

    for song_question in songs_questions:
        questions.append(song_question)

    if DebuggingConventions.DEBUGGING_SONGS_LIST_CREATION:
        print("final_dict_after_songs_list is")
        for question in questions:
            print("\t{}".format(question))

    random.shuffle(questions)  # shuffle

    # add the artist name question as first question for a hard game
    if game_type == Conventions.HARD_GAME_CODE:
        questions.insert(Conventions.LIST_BEGINNING_OFF_SET,
                         questions_map[Conventions.NAME](raw_artists_dict))

    build_questions_dict_for_view(questions)

    # build and return the questions dict
    return build_questions_dict_for_view(questions)


def generate_songs_questions(raw_artists_dict, game_type=None):
    """
    generates the songs questions from the given raw_artists_dict
    :param raw_artists_dict:
    :return:
    """
    artist_to_play_on = pick_artist_to_play_on(raw_artists_dict, game_type)

    if DebuggingConventions.DEBUGGING_SONGS_LIST_CREATION:
        print("---- AT SONGS QUESTIONS LIST CREATION ----")

    out_questions_list = []

    # check the minimal songs list size
    min_songs_list_size = get_minimal_songs_list_size(raw_artists_dict)

    question_text = Conventions.QUESTIONS_STRINGS_DICT[Conventions.QUESTIONS_DICT_SONGS]

    if game_type == Conventions.CHALLENGING_GAME_CODE:
        question_text += add_artist_name_to_challenging_question(
            load_offset_from_raw_artists_dict(raw_artists_dict,
                                              Conventions.RAW_ARTISTS_DATA_ARTIST_OFFSET,
                                              artist_to_play_on,
                                              Conventions.NAME_OFF_SET)
        )

    answers = []

    # build a song list for each index
    for index in range(min_songs_list_size):
        answers = []

        # take the song at the [index] location from each artist
        for artist in raw_artists_dict[Conventions.RAW_ARTISTS_DATA_ARTIST_OFFSET]:
            song_to_add = artist[Conventions.SONGS_LIST_OFF_SET][index]

            answers.append(song_to_add)

            if DebuggingConventions.DEBUGGING_SONGS_LIST_CREATION:
                print("Song to add is: {} from artist: {}".format(song_to_add, artist[Conventions.NAME_OFF_SET]))

        if DebuggingConventions.DEBUGGING_SONGS_LIST_CREATION:
            print("Songs list is: {}".format(answers))

        # get the right answer
        right_answer = answers[artist_to_play_on]

        # append the built question to the questions dict
        out_questions_list.append(build_question_dict(question_text, answers, right_answer))

    return out_questions_list


def generate_name_question(raw_artists_dict, game_type):
    """
    generates the name question for the playing artist, given the raw_artists_dict

    :param raw_artists_dict:
    :return:
    """
    question_text = Conventions.QUESTIONS_STRINGS_DICT[Conventions.QUESTIONS_DICT_NAME]

    if game_type == Conventions.CHALLENGING_GAME_CODE:
        question_text += add_artist_name_to_challenging_question(
            load_offset_from_raw_artists_dict(raw_artists_dict,
                                              Conventions.RAW_ARTISTS_DATA_ARTIST_OFFSET,
                                              Conventions.PLAYING_ARTIST_OFF_SET,
                                              Conventions.NAME_OFF_SET)
        )

    answers = [artist[Conventions.NAME_OFF_SET] for artist in
               raw_artists_dict[Conventions.RAW_ARTISTS_DATA_ARTIST_OFFSET]]  # append all artists names
    right_answer = load_offset_from_raw_artists_dict(raw_artists_dict,
                                                     Conventions.RAW_ARTISTS_DATA_ARTIST_OFFSET,
                                                     Conventions.PLAYING_ARTIST_OFF_SET,
                                                     Conventions.NAME_OFF_SET)

    return build_question_dict(question_text, answers, right_answer)


def build_questions_dict_for_view(questions_list):
    """
    builds the questions dict from the questions list. Inserts question_name: question per not None value.

    :param questions_list:
    :return:
    """
    questions_dict = dict()

    if DebuggingConventions.DEBUGGING_QUESTIONS_GENERATING:
        print("Questions list is:\n{}".format(questions_list))

    for question in questions_list:
        # insert question if it is not None
        if question:
            question_name = question[Conventions.QUESTION_NAME_OFFSET]

            if DebuggingConventions.DEBUGGING_QUESTIONS_GENERATING:
                print("Question name to add is: {}".format(question_name))

            questions_dict[question_name] = question

    if DebuggingConventions.DEBUGGING_QUESTIONS_GENERATING:
        print("Questions dict build:\n{}".format(questions_dict))

    return questions_dict


def none_values_exist_in_answer_list(answers_list):
    """
    check if answers list holds None values
    :param answers_list:
    :return:
    """
    for answer in answers_list:
        if answer is None:
            if DebuggingConventions.DEBUGGING_QUESTIONS_GENERATING:
                print("answers list holds None values:{}".format(answers_list))
            return True

    return False


def answers_list_empty_or_holds_less_than_three_values(answers_list):
    """
    checks if the answers list is empty or holds less than three values
    :param answers_list:
    :return:
    """
    if answers_list == Conventions.EMPTY_ANSWERS_LIST_CODE or \
           len(answers_list) != Conventions.VALID_ANSWERS_LIST_SIZE:
        if DebuggingConventions.DEBUGGING_QUESTIONS_GENERATING:
            print("answers list is in wrong size of empty:{}".format(answers_list))
        return None


def generate_random_list_of_origins():
    """
    generates the random list of origins
    :return:
    """
    list_of_origins = Conventions.LIST_OF_ORIGINS.copy()

    origins_list_to_return = list()

    for number_of_origins_to_add in range(Conventions.NUMBER_OF_ORIGINS):
        # get a random origin
        rand_origin = random.choice(list_of_origins)

        # add it to the list
        origins_list_to_return.append(rand_origin)

        # remove it from the list_of_origins
        list_of_origins.remove(rand_origin)

    return origins_list_to_return


def generate_origin_question(raw_artists_dict, game_type=None):
    """
    generates the origin question

    :param raw_artists_dict:
    :return:
    """
    artist_to_play_on = pick_artist_to_play_on(raw_artists_dict, game_type)

    question_text = Conventions.QUESTIONS_STRINGS_DICT[Conventions.QUESTIONS_DICT_FROM]

    if game_type == Conventions.CHALLENGING_GAME_CODE:
        question_text += add_artist_name_to_challenging_question(
            load_offset_from_raw_artists_dict(raw_artists_dict,
                                              Conventions.RAW_ARTISTS_DATA_ARTIST_OFFSET,
                                              artist_to_play_on,
                                              Conventions.NAME_OFF_SET)
        )

    # generate a random list of origins and add the right answer
    answers = generate_random_list_of_origins()
    answers.append(load_offset_from_raw_artists_dict(raw_artists_dict,
                                                     Conventions.RAW_ARTISTS_DATA_ARTIST_OFFSET,
                                                     artist_to_play_on,
                                                     Conventions.FROM_OFF_SET))

    if none_values_exist_in_answer_list(answers):
        return None

    if answers_list_empty_or_holds_less_than_three_values(answers):
        return None

    # the origin of the playing artist as the right answer
    right_answer = \
        raw_artists_dict[Conventions.RAW_ARTISTS_DATA_ARTIST_OFFSET][artist_to_play_on][Conventions.FROM_OFF_SET]

    return build_question_dict(question_text, answers, right_answer)


def generate_birth_date_question(raw_artists_dict, game_type=None):
    """
    generates the birth date question

    :param raw_artists_dict:
    :return:
    """
    artist_to_play_on = pick_artist_to_play_on(raw_artists_dict, game_type)

    question_text = Conventions.QUESTIONS_STRINGS_DICT[Conventions.QUESTIONS_DICT_BIRTH_DATE]

    if game_type == Conventions.CHALLENGING_GAME_CODE:
        question_text += add_artist_name_to_challenging_question(
            load_offset_from_raw_artists_dict(raw_artists_dict,
                                              Conventions.RAW_ARTISTS_DATA_ARTIST_OFFSET,
                                              artist_to_play_on,
                                              Conventions.NAME_OFF_SET)
        )

    answers = [artist[Conventions.BIRTH_DATE_OFF_SET] for artist in
               raw_artists_dict[Conventions.RAW_ARTISTS_DATA_ARTIST_OFFSET]]

    if none_values_exist_in_answer_list(answers):
        return None

    if answers_list_empty_or_holds_less_than_three_values(answers):
        return None

    right_answer = answers[artist_to_play_on]

    return build_question_dict(question_text, answers, right_answer)


def generate_genre_question(raw_artists_dict, game_type=None):
    """
    generates the genre question

    :param raw_artists_dict:
    :return:
    """
    artist_to_play_on = pick_artist_to_play_on(raw_artists_dict, game_type)

    list_of_lists_of_genres = list()

    for artist in raw_artists_dict[Conventions.RAW_ARTISTS_DATA_ARTIST_OFFSET]:
        # appends a LIST of genres per artist name
        list_of_lists_of_genres.append(Queries.get_genre_by_artist(artist[Conventions.NAME_OFF_SET]))

    genres_for_question = list()

    # randomly pick a genre from the list of genres per artist
    for artist_genres_list in list_of_lists_of_genres:
        genres_for_question.append(artist_genres_list[random.randint(0, len(artist_genres_list) - 1)])

    # check for None values
    if none_values_exist_in_answer_list(genres_for_question):
        return None

    if answers_list_empty_or_holds_less_than_three_values(genres_for_question):
        return None

    question_text = Conventions.QUESTIONS_STRINGS_DICT[Conventions.QUESTIONS_DICT_GENRE]

    if game_type == Conventions.CHALLENGING_GAME_CODE:
        question_text += add_artist_name_to_challenging_question(
            load_offset_from_raw_artists_dict(raw_artists_dict,
                                              Conventions.RAW_ARTISTS_DATA_ARTIST_OFFSET,
                                              artist_to_play_on,
                                              Conventions.NAME_OFF_SET)
        )

    right_answer = genres_for_question[artist_to_play_on]

    return build_question_dict(question_text, genres_for_question, right_answer)


def generate_similar_artists_question(raw_artists_dict, game_type=None):
    """
    generates the similar artists question
    :param raw_artists_dict:
    :return:
    """
    artist_to_play_on = pick_artist_to_play_on(raw_artists_dict, game_type)

    # artist name
    artist_name = load_offset_from_raw_artists_dict(raw_artists_dict,
                                                    Conventions.RAW_ARTISTS_DATA_ARTIST_OFFSET,
                                                    artist_to_play_on,
                                                    Conventions.NAME_OFF_SET)

    question_text = Conventions.QUESTIONS_STRINGS_DICT[Conventions.QUESTIONS_DICT_SIMILAR]

    if game_type == Conventions.CHALLENGING_GAME_CODE:
        question_text += add_artist_name_to_challenging_question(
            load_offset_from_raw_artists_dict(raw_artists_dict,
                                              Conventions.RAW_ARTISTS_DATA_ARTIST_OFFSET,
                                              artist_to_play_on,
                                              Conventions.NAME_OFF_SET)
        )

    # generate similar artist by randomly picking a genre of similarity
    similar_artists_list = Queries.get_similar_and_different_artists_list(artist_name)

    similar_artists_list = [artist[0] for artist in similar_artists_list]

    # check None values
    if none_values_exist_in_answer_list(similar_artists_list):
        return None

    if answers_list_empty_or_holds_less_than_three_values(similar_artists_list):
        return None

    return build_question_dict(question_text, similar_artists_list, similar_artists_list[Conventions.ZERO])


def build_question_dict(text, answers, right_answer):
    """
    turns question text, answers and right_answer into a question dictionary
    :param text:
    :param answers:
    :param right_answer:
    :return:
    """
    return {
        "text": text,
        "answers": answers,
        "true": right_answer
    }


def get_all_preferences():
    """
    load all preferences for user

    :return:
    """
    return Queries.get_all_genres()


def get_leader_board():
    """
    loads the leader boards
    :return:
    """
    leader_board = dict()

    for game_type in Conventions.GAME_TYPES:
        leader_board[game_type] = list()
        leader_board[game_type].append(['Player name', 'Score'])

        top_players = Queries.get_top_players(game_type)

        for data_list in top_players:
            leader_board[game_type].append(data_list)

        if top_players != Conventions.EMPTY_ANSWERS_LIST_CODE:
            for data_list in top_players:
                leader_board[game_type].append(data_list)

    return leader_board


def start(username, game_type):
    """
    handles the start game logic

    :param username:
    :param game_type:
    :return:
    """

    if DebuggingConventions.GENERALLY_DEBUGGING_GAME_LOGIC:
        print("The game type received is: {}".format(game_type))

    # create a game depending on the game_type
    if game_type == Conventions.EASY_GAME_CODE or game_type == Conventions.HARD_GAME_CODE:
        if DebuggingConventions.GENERALLY_DEBUGGING_GAME_LOGIC:
            print("Creating an easy game!")
        return generate_easy_or_hard_games(username, game_type)

    return generate_challenging_game(username, game_type)


def get_minimal_songs_list_size(raw_artists_dict):
    """
    returns the minimal songs list size for this raw_artists_dict
    :param raw_artists_dict:
    :return:
    """
    min_songs_list_size = sys.maxsize

    # check songs list length == 3
    for artist in raw_artists_dict[Conventions.RAW_ARTISTS_DATA_ARTIST_OFFSET]:
        if DebuggingConventions.DEBUGGING_RAW_DICT:
            print("Checking artist: {}\n\tsongs list: {}".format(artist, artist[Conventions.SONGS_LIST_OFF_SET]))

        # songs list of this artist is empty -> return 0
        if len(artist) != 5:
            if DebuggingConventions.DEBUGGING_RAW_DICT:
                print("Error in artist length: {}".format(len(artist)))
            return Conventions.ZERO

        # check if this songs list's length is smaller than the smallest
        if len(artist[Conventions.SONGS_LIST_OFF_SET]) < min_songs_list_size:
            if DebuggingConventions.DEBUGGING_RAW_DICT:
                print("Error in songs list length: {}".format(len(artist[Conventions.SONGS_LIST_OFF_SET])))
            # if so -> update smallest size
            min_songs_list_size = len(artist[Conventions.SONGS_LIST_OFF_SET])

    return min_songs_list_size


def song_name_str(song_name, index):
    """
    returns the defined song name str + index + the song name

    :param song_name:
    :param index:
    :return: the defined song text + index for song name
    """
    return Conventions.SONG_NAME_STR + str(index) + ": " + song_name


def generate_challenging_game(user_name, game_type):
    """
    Generates the challenging game dictionary for the view

    :param user_name:
    :param game_type:
    :return:
    """

    user_id = load_user_id_only_by_name(user_name)  # generate user ID

    raw_artists_dict = Queries.get_preferred_artists(user_id, game_type)  # generate raw artists dict

    # generate artists list
    artists_list = [artist[Conventions.NAME_OFF_SET] for artist in
                    raw_artists_dict[Conventions.RAW_ARTISTS_DATA_ARTIST_OFFSET]]

    # generate the properties list
    properties_list_for_each_artist = list()

    index = 0

    for artist in raw_artists_dict[Conventions.RAW_ARTISTS_DATA_ARTIST_OFFSET]:
        if DebuggingConventions.DEBUGGING_CHALLENGING_GAME:
            print("artist is: {}\n\tfrom: {}\n\tborn on: {}".format(artist,
                                                                    artist[Conventions.FROM_OFF_SET],
                                                                    artist[Conventions.BIRTH_DATE_OFF_SET]))

        # create a list per artist
        properties_list_for_artist = list()
        
        # append relevant information
        properties_list_for_artist.append(Conventions.ORIGINS_STR +
                                          load_offset_from_raw_artists_dict(
                                              artist, Conventions.FROM_OFF_SET))  # from
        properties_list_for_artist.append(Conventions.BIRTH_DATE_STR +
                                          load_offset_from_raw_artists_dict(
                                              artist, Conventions.BIRTH_DATE_OFF_SET))  # birth day

        # generate the songs list for this artist
        generate_songs_list(raw_artists_dict, properties_list_for_artist, index)
        index +=1

        if DebuggingConventions.DEBUGGING_CHALLENGING_GAME:
            print("Created properties list for: {}".format(artist[Conventions.NAME_OFF_SET]))

            print("properties list is:\n{}".format(properties_list_for_artist))

        properties_list_for_each_artist.append(properties_list_for_artist)

    if not DebuggingConventions.TESTING_VIEW:
        return {
            Conventions.ARTIST_NAME: artists_list,
            Conventions.PROPERTIES: properties_list_for_each_artist,
            Conventions.QUESTIONS: generate_questions(raw_artists_dict, game_type)
        }
    else:
        return DebuggingConventions.MOCK_CHALLENGING_DICT


def generate_songs_list(raw_artists_dict, out_list, artist_index):
    """
    uses the raw_artists_dict to generate the list of songs for the out_list

    :param raw_artists_dict:
    :param out_list:
    :return:
    """
    if get_minimal_songs_list_size(raw_artists_dict) == Conventions.ZERO:
        songs_list = []
    else:
        songs_list = load_offset_from_raw_artists_dict(raw_artists_dict,
                                                       Conventions.RAW_ARTISTS_DATA_ARTIST_OFFSET,
                                                       artist_index,
                                                       Conventions.SONGS_LIST_OFF_SET)

    # append the songs_list to the properties list. appends an empty list if there are no songs for the artist
    if songs_list is []:
        out_list.append(Conventions.EMPTY_SONGS_LIST_STR)
    else:
        index = 1

        for song in songs_list:
            out_list.append(song_name_str(song, index))
            index += 1


def generate_easy_or_hard_games(user_name, game_type):
    """
    generates the easy and hard games dict
    :param user_name:
    :param game_type:
    :return:
    """
    user_id = load_user_id_only_by_name(user_name)  # generate user ID

    raw_artists_dict = Queries.get_preferred_artists(user_id, game_type)  # generate raw artists dict

    if DebuggingConventions.GENERALLY_DEBUGGING_GAME_LOGIC:
        print(raw_artists_dict)

    # generate the properties list
    properties = list()
    properties.append(Conventions.ORIGINS_STR +
                      load_offset_from_raw_artists_dict(raw_artists_dict,
                                                        Conventions.RAW_ARTISTS_DATA_ARTIST_OFFSET,
                                                        Conventions.PLAYING_ARTIST_OFF_SET,
                                                        Conventions.FROM_OFF_SET))

    properties.append(Conventions.BIRTH_DATE_STR +
                      load_offset_from_raw_artists_dict(raw_artists_dict,
                                                        Conventions.RAW_ARTISTS_DATA_ARTIST_OFFSET,
                                                        Conventions.PLAYING_ARTIST_OFF_SET,
                                                        Conventions.BIRTH_DATE_OFF_SET))

    generate_songs_list(raw_artists_dict, properties, Conventions.PLAYING_ARTIST_OFF_SET)

    if not DebuggingConventions.TESTING_VIEW:
        return {
            Conventions.ARTIST_NAME: load_offset_from_raw_artists_dict(raw_artists_dict,
                                                                       Conventions.RAW_ARTISTS_DATA_ARTIST_OFFSET,
                                                                       Conventions.PLAYING_ARTIST_OFF_SET,
                                                                       Conventions.NAME_OFF_SET),
            Conventions.PROPERTIES: properties,
            Conventions.QUESTIONS: generate_questions(raw_artists_dict, game_type)
        }
    else:
        return DebuggingConventions.MOCK_DICT


def load_offset_from_raw_artists_dict(raw_artists_dict, offset_one, offset_two=None, offset_three=None):
    """
    return the raw_artists_dict offset, depending on how many were given
    :param raw_artists_dict:
    :param offset_one:
    :param offset_two:
    :param offset_three:
    :return:
    """
    if offset_two is not None:
        if offset_three is not None:
            if DebuggingConventions.DEBUGGING_RAW_DICT_ACCESS:
                print("raw_artists_dict will return: {}".format(raw_artists_dict[offset_one][offset_two][offset_three]))
            return raw_artists_dict[offset_one][offset_two][offset_three]
        if DebuggingConventions.DEBUGGING_RAW_DICT_ACCESS:
            print("raw_artists_dict will return: {}".format(raw_artists_dict[offset_one][offset_two]))
        return raw_artists_dict[offset_one][offset_two]

    if DebuggingConventions.DEBUGGING_RAW_DICT_ACCESS:
        print("raw_artists_dict will return: {}".format(raw_artists_dict[offset_one]))
    return raw_artists_dict[offset_one]


def add_artist_name_to_challenging_question(artist_name):
    """
    creates a special wrapping for a challenging question, containing the artist name
    :param artist_name:
    :return:
    """
    return " (on artist: " + artist_name + ")"


def pick_a_random_number_from_zero_to(num):
    return random.randint(0, num - 1)


def pick_artist_to_play_on(raw_artists_dict, game_type):
    if game_type == Conventions.CHALLENGING_GAME_CODE:
        # generate a random number to play on
        artist_to_play_on = pick_a_random_number_from_zero_to(
            len(raw_artists_dict[Conventions.RAW_ARTISTS_DATA_ARTIST_OFFSET]))
    else:
        artist_to_play_on = Conventions.ZERO

    return artist_to_play_on
