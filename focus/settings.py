import json
import datetime as dt


class FocusSettings:
    def __init__(self):

        self.settings_file_name = "user_config.json"
        self.settings_file_path = f"data/{self.settings_file_name}"

        self.folder_structure = {
            "app": {
                "first_launch": "True",
                "day": 9
            },
            "user": {
                "theme": "superhero",
                "users_target_sessions": 10,
                "users_focus_time": 25,
                "users_short_break_time": 5,
                "users_long_break_time": 20,
                "total_focus_sessions_completed": 0,
                "total_short_breaks_got": 0,
                "total_long_breaks_got": 0,
            }
        }

        self.default_user_settings = {
            "users_target_sessions": 10,
            "users_focus_time": 25,
            "users_short_break_time": 5,
            "users_long_break_time": 20,
            "total_focus_sessions_completed": 0,
            "total_short_breaks_got": 0,
            "total_long_breaks_got": 0,
        }

        self.saved_settings = ""
        self.load_settings()
        self.reset_user_progress_daily()

    def load_settings(self):
        try:
            with open(self.settings_file_path, "r") as settings_file:
                self.saved_settings = json.load(settings_file)
        except FileNotFoundError:
            self.saved_settings = self.folder_structure
            with open(self.settings_file_path, "w") as settings_file:
                json.dump(self.folder_structure, settings_file, indent=4)
        finally:
            return self.saved_settings

    def save_user_settings(self, settings_to_save: dict):
        updated_data = self.saved_settings
        for key, value in settings_to_save.items():
            updated_data["user"][key] = value

        try:
            with open(self.settings_file_path, "w") as settings_file:
                json.dump(updated_data, settings_file, indent=4)
        except FileNotFoundError:
            print("Error: Could not save settings.")
            return
        finally:
            self.saved_settings = updated_data

    def reset_settings(self):
        updated_data = self.saved_settings
        for key, value in self.default_user_settings.items():
            updated_data["user"][key] = value
        try:
            with open(self.settings_file_path, "w") as settings_file:
                json.dump(updated_data, settings_file, indent=4)
        except FileNotFoundError:
            print("Error: Could not save settings.")
            return
        finally:
            self.saved_settings = updated_data

    def reset_user_progress_daily(self):
        saved_date = self.saved_settings["app"]["day"]
        today = dt.datetime.today().day
        if saved_date != today:
            updated_date = self.saved_settings
            updated_date["app"]["day"] = today
            try:
                with open(self.settings_file_path, "w") as settings_file:
                    json.dump(updated_date, settings_file, indent=4)
                reset_progress = {
                    "total_focus_sessions_completed": 0,
                    "total_short_breaks_got": 0,
                    "total_long_breaks_got": 0,
                }
                self.save_user_settings(reset_progress)
            except FileNotFoundError:
                print("Error: Could not save settings.")
                return
            finally:
                self.load_settings()

        else:
            print("Restoring Progress")
            self.load_settings()

    def update_first_launch(self):
        saved_data = self.saved_settings
        is_first_launch = saved_data["app"]['first_launch']

        if is_first_launch:
            updated_data = saved_data
            updated_data["app"]['first_launch'] = False
            try:
                with open(self.settings_file_path, "w") as settings_file:
                    json.dump(updated_data, settings_file, indent=4)
            except FileNotFoundError:
                print("Error: Could not save settings.")
                return
            finally:
                self.saved_settings = updated_data
        else:
            return

