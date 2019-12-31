import pandas as pd
from Logic.User import User


class Authenticator:
    PREFERENCES_EXIST_STATUS = 1
    PREFERENCES_NON_EXISTING = 0
    USER_DOESNT_EXIST = -1

    def login(self, username, password):
        user_data_frame = self.load_user_from_data_base(username, password)

        if user_data_frame is None:
            return self.USER_DOESNT_EXIST, None

        user = User()  # TODO: Create a new user from the df

        if user.get_preferences_dict():
            return self.PREFERENCES_EXIST_STATUS, user
        else:
            return self.PREFERENCES_NON_EXISTING, user


    def load_user_from_data_base(self, username, password):
        # TODO: question DB if user exists
        pass
