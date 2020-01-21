import Conventions

# ---- GAME LOGIC ----

TESTING_VIEW = False
GENERALLY_DEBUGGING_GAME_LOGIC = False
DEBUGGING_RAW_DICT = False
DEBUGGING_SONGS_LIST_CREATION = False
DEBUGGING_RAW_DICT_ACCESS = False

DEBUGGING_GAME_END = False
DEBUGGING_QUESTIONS_GENERATING = False

MOCK_QUESTIONS_DICT = {
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
                "answers": ["song1_a1", "song1_a2", "song1_a3", "Alon"],
                "true": "right_answer"
            },
            "q4": {
                "text": "Song2?",
                "answers": ["song2_a1", "song2_a2", "Sara", "song2_a3"],
                "true": "right_answer"
            },
            "q5": {
                "text": "Song3?",
                "answers": ["Yana", "song3_a1", "song3_a2", "song3_a3"],
                "true": "Yana"
            }
        }


MOCK_DICT = {
        Conventions.ARTIST_NAME: "Adel",
        Conventions.PROPERTIES: ["Country: UK", "Date: 12.12.1980", "Song1: Alon kaka", "Song2: Sara kaka", "Song3: Yana kaka"],
        Conventions.QUESTIONS: MOCK_QUESTIONS_DICT
    }


MOCK_CHALLENGING_DICT = GameInfoDict = {
        Conventions.ARTIST_NAME: ["Adel", "Adel2", "Adel3", "Ade4", "Adel5"],
        Conventions.PROPERTIES: [["Country: UK", "Date: 12.12.1980", "Song1: Alon kaka", "Song2: Sara kaka", "Song3: Yana kaka"], ["Country1: UK", "Date1: 12.12.1980", "Song11: Alon kaka", "Song12: Sara kaka", "Song13: Yana kaka"], ["Country2: UK", "Date2: 12.12.1980", "Song21: Alon kaka", "Song22: Sara kaka", "Song23: Yana kaka"], ["Country3: UK", "Date3: 12.12.1980", "Song31: Alon kaka", "Song32: Sara kaka", "Song33: Yana kaka"], ["Country4: UK", "Date4: 12.12.1980", "Song41: Alon kaka", "Song42: Sara kaka", "Song43: Yana kaka"]],
        Conventions.QUESTIONS: MOCK_QUESTIONS_DICT
    }
