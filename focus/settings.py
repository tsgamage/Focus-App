import json

class FocusSettings:
    def __init__(self):

        self.settings_file_name = "user_config.json"
        self.settings_file_path = f"test/{self.settings_file_name}"

        self.default_settings = {
            "app": {
                "first_launch": "True",
                "day": 9
            },
            "default": {
                "theme": "superhero",
                "default_target_sessions": 10,
                "default_focus_time": 25,
                "default_short_break_time": 5,
                "default_long_break_time": 20,
            },
            "user": {
                "theme": "",
                "users_target_sessions": 0,
                "users_focus_time": 0,
                "users_short_break_time": 0,
                "users_long_break_time": 0,
                "total_focus_sessions_completed": 0,
                "total_short_breaks_got": 0,
                "total_long_breaks_got": 0,
            }
        }

        self.saved_settings = ""
        self.load_settings()

    def load_settings(self):
        try:
            with open(self.settings_file_path, "r") as settings_file:
                self.saved_settings = json.load(settings_file)
        except FileNotFoundError:
            self.saved_settings = self.default_settings
            with open(self.settings_file_path, "w") as settings_file:
                json.dump(self.default_settings, settings_file, indent=4)
        finally:
            return self.saved_settings


    def save_settings(self, settings_to_save: dict):

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
        self.save_settings(self.default_settings)