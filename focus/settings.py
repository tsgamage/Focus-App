import json
import datetime as dt
from .loggingHandler import *


def setting_file_is_correct(user_data_dict, default_data_dict):
    def extract_keys(data_dict):
        extracted_key_list = []

        for key, value in data_dict.items():
            extracted_key_list.append(key)
            for inner_keys in data_dict[key]:
                extracted_key_list.append(inner_keys)

        return extracted_key_list

    user_data_keys = extract_keys(user_data_dict)
    default_data_keys = extract_keys(default_data_dict)

    return user_data_keys == default_data_keys

class FocusSettings:
    def __init__(self):

        self.PARENT_PATH = "Princess Software Solutions"
        self.APP_NAME = "Focus App"
        self.SUB_FILE_NAME = "data"
        self.SETTINGS_FILE_NAME = "user_config.json"

        self.APP_FOLDER = os.path.join(os.getenv("APPDATA"), self.PARENT_PATH, self.APP_NAME, self.SUB_FILE_NAME)

        # Generate the folder if it doesn't exist.'
        os.makedirs(self.APP_FOLDER, exist_ok=True)

        self.USER_SETTINGS_FILE_PATH = os.path.join(self.APP_FOLDER, self.SETTINGS_FILE_NAME)

        # Default Settings
        self.FOLDER_STRUCTURE = {
            "app": {
                "first_launch": "True",
                "day": 9
            },
            "user": {
                "theme": "darkly",
                "users_target_sessions": 10,
                "users_focus_time": 25,
                "users_short_break_time": 5,
                "users_long_break_time": 20,
                "total_focus_sessions_completed": 0,
                "total_short_breaks_completed": 0,
                "total_long_breaks_completed": 0,
                "total_focus_minutes": 0,
                "total_break_minutes":0,
            }
        }
        # Make these separately because it's easy to reset all data with this
        self.DEFAULT_ALL_SETTINGS = {
            "users_target_sessions": 10,
            "users_focus_time": 25,
            "users_short_break_time": 5,
            "users_long_break_time": 20,
            "total_focus_sessions_completed": 0,
            "total_short_breaks_completed": 0,
            "total_long_breaks_completed": 0,
            "total_focus_minutes": 0,
            "total_break_minutes": 0,
        }
        self.DEFAULT_USER_SETTINGS = {
            "users_target_sessions": 10,
            "users_focus_time": 25,
            "users_short_break_time": 5,
            "users_long_break_time": 20,
        }
        self.DEFAULT_PROGRESS_SETTINGS = {
            "total_focus_sessions_completed": 0,
            "total_short_breaks_completed": 0,
            "total_long_breaks_completed": 0,
            "total_focus_minutes": 0,
            "total_break_minutes": 0,
        }

        # Loaded user settings will be stored here.
        self.saved_settings = {}

        self.load_settings()

        # Check if the settings file is correct. If not, reset it.
        if not setting_file_is_correct(self.saved_settings, self.FOLDER_STRUCTURE):
            log_debug("Resetting All settings to default values because settings file is not correct.")
            self.update_user_settings("resetFile")

        self.reset_user_settings_if_they_changed_to_wrong()

        self.reset_user_progress_daily()


    # Load the settings file.
    def load_settings(self):
        try:
            with open(self.USER_SETTINGS_FILE_PATH, "r") as settings_file:
                self.saved_settings = json.load(settings_file)
            log_info("Settings loaded successfully.")

        # Create the settings file if it doesn't exist and insert default values.
        except:
            self.saved_settings = self.FOLDER_STRUCTURE
            with open(self.USER_SETTINGS_FILE_PATH, "w") as settings_file:
                json.dump(self.FOLDER_STRUCTURE, settings_file, indent=4)
            log_info("Settings file created successfully.")

    def update_user_settings(self, settings_to_save):
        users_data = settings_to_save

        if settings_to_save == "resetFile":
            users_data = self.FOLDER_STRUCTURE
            log_info("Resetting settings file to default values.")

        if settings_to_save == "resetAll":
            users_data = self.DEFAULT_ALL_SETTINGS
            log_info("Changing all settings to default values.")

        if settings_to_save == "resetSettings":
            users_data = self.DEFAULT_USER_SETTINGS
            log_info("Changing user settings to default values.")

        updated_data = self.saved_settings
        # Resetting the whole file if the 'resetFile' is passed as settings_to_save.
        # Otherwise, updating only the data wanted
        if settings_to_save == "resetFile":
            updated_data = self.FOLDER_STRUCTURE
        else:
            for key, value in users_data.items():
                updated_data["user"][key] = value

        # Try to save the updated settings.
        try:
            with open(self.USER_SETTINGS_FILE_PATH, "w") as settings_file:
                json.dump(updated_data, settings_file, indent=4)

            log_info("Settings updated successfully.")

        except FileNotFoundError:
            log_error("Settings update failed.")
            print("Error: Could not save settings.")

        finally:
            self.saved_settings = updated_data

    def reset_user_progress_daily(self):
        saved_date = self.saved_settings["app"]["day"]
        today = dt.datetime.today().day
        if saved_date != today:
            updated_date = self.saved_settings
            updated_date["app"]["day"] = today
            try:
                with open(self.USER_SETTINGS_FILE_PATH, "w") as settings_file:
                    json.dump(updated_date, settings_file, indent=4)
                self.update_user_settings(self.DEFAULT_PROGRESS_SETTINGS)
                log_info("Progress reset successful.")
            except FileNotFoundError:
                print("Error: Could not save settings.")
                log_error("Progress reset failed.")
                return
            finally:
                self.load_settings()

        else:
            self.load_settings()

    def update_first_launch(self):
        saved_data = self.saved_settings
        is_first_launch = saved_data["app"]['first_launch']

        if is_first_launch:
            updated_data = saved_data
            updated_data["app"]['first_launch'] = False
            try:
                with open(self.USER_SETTINGS_FILE_PATH, "w") as settings_file:
                    json.dump(updated_data, settings_file, indent=4)
                log_info("First launch update successful.")
            except FileNotFoundError:
                print("Error: Could not save settings.")
                log_error("First launch update failed.")
                return
            finally:
                self.saved_settings = updated_data
        else:
            return

    def reset_user_settings_if_they_changed_to_wrong(self):
        is_target_sessions_zero = self.saved_settings["user"]["users_target_sessions"] == 0
        is_focus_time_zero = self.saved_settings["user"]["users_focus_time"] == 0
        is_short_break_time_zero = self.saved_settings["user"]["users_short_break_time"] == 0
        is_long_break_time_zero = self.saved_settings["user"]["users_long_break_time"] == 0

        is_first_launch_is_bool = not isinstance(self.saved_settings["app"]["first_launch"], bool)
        is_day_is_int = not isinstance(self.saved_settings["app"]["day"], int)
        is_target_sessions_is_int = not isinstance(self.saved_settings["user"]["users_target_sessions"], int)
        is_focus_time_is_int = not isinstance(self.saved_settings["user"]["users_focus_time"], int)
        is_short_break_time_is_int = not isinstance(self.saved_settings["user"]["users_short_break_time"], int)
        is_long_break_time_is_int = not isinstance(self.saved_settings["user"]["users_long_break_time"], int)
        is_total_focus_sessions_completed_is_int = not isinstance(self.saved_settings["user"]["total_focus_sessions_completed"], int)
        is_total_short_breaks_completed_is_int = not isinstance(self.saved_settings["user"]["total_short_breaks_completed"], int)
        is_total_long_breaks_completed_is_int = not isinstance(self.saved_settings["user"]["total_long_breaks_completed"], int)
        is_total_focus_minutes_is_int = not isinstance(self.saved_settings["user"]["total_focus_minutes"], int)
        is_total_break_minutes_is_int = not isinstance(self.saved_settings["user"]["total_break_minutes"], int)

        if is_target_sessions_zero or is_focus_time_zero or is_short_break_time_zero or is_long_break_time_zero:
            log_debug("Resetting All settings to default values because some values are zero.")
            self.update_user_settings("resetAll")

        if is_first_launch_is_bool or is_day_is_int or is_target_sessions_is_int or is_focus_time_is_int or is_short_break_time_is_int or is_long_break_time_is_int or is_total_focus_sessions_completed_is_int or is_total_short_breaks_completed_is_int or is_total_long_breaks_completed_is_int or is_total_focus_minutes_is_int or is_total_break_minutes_is_int:
            log_debug("Resetting All settings to default values because data type of some values are wrong.")
            self.update_user_settings("resetAll")
