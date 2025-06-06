import math

class Sessions:
    def __init__(self, application):

        self.application = application

        self.saved_session_time_in_minutes: int
        self.saved_short_break_time_in_minutes: int
        self.saved_long_break_time_in_minutes: int

        self.session_times: dict = {"focus": 6, "shortB": 3, "longB": 5}
        self.current_session: str = "focus"  # Can use focus, shortB, and longB
        self.session_number: int = 1
        self.session_started: bool = False

        self.current_running_seconds: int = -1
        """
        Passing -1 because application checks this value to start the timer when it is 0, it will pass the if 
        statement that checks "self.current_running_seconds >= 0" and when its zero the application thinks the 
        timer has stopped by the user at 0 seconds so it will pass the zero as seconds. When it passes 0 as the 
        seconds for the timer, the timer will jump to the next session immediately.
        """
        self.formated_current_running_time: str = ''
        self.timer = ''

        self.total_focus_sessions: int = 0
        self.total_short_break_sessions: int = 0
        self.total_long_break_sessions: int = 0



    def reset_variables(self):
        self.current_running_seconds = -1
        self.session_number = 1

    def formate_time(self, seconds: int):
        """ Update the current seconds to the time in min:sec format """
        timer_min = math.floor(seconds / 60)
        timer_sec = seconds % 60

        # Adding a '0' to the front of minutes when it is smaller than 10
        if timer_min < 10:
            timer_min = f"0{timer_min}"

        # Adding a '0' to the front of seconds when it is smaller than 10
        if timer_sec < 10:
            timer_sec = f"0{timer_sec}"

        # Adding '0' to the seconds when it is zero
        if timer_sec == 0:
            timer_sec = "00"

        self.formated_current_running_time =  f"{timer_min}:{timer_sec}"
        return self.formated_current_running_time

    def countdown(self, seconds: int, application):
        """ The main core of the app. Countdown function. """

        self.current_running_seconds = seconds
        self.formate_time(seconds)
        self._running_after_every_seconds()

        if seconds >= 0:
            print(f"seconds: {seconds}")
            print(f"current_session:{self.current_session}\n\n")

            self.application.update_ui_timer(self.formated_current_running_time)

            # used_percentage = math.floor((seconds / self.session_times[f"{self.current_session}"]) * 100)
            application.update_ui_meter(seconds, self.session_times[f"{self.current_session}"])

            self.timer = application.after(1000, self.countdown, self.current_running_seconds - 1, self.application)

        elif self.current_running_seconds < 0:
            self._run_after_finishing_session()

            if self.current_session == "focus":
                self.total_focus_sessions += 1
            elif self.current_session == "shortB":
                self.total_short_break_sessions += 1
            elif self.current_session == "longB":
                self.total_long_break_sessions += 1

            self.session_number += 1
            if self.session_number > 8:
                self.reset_variables()
                self._run_after_long_break()
            self.start_session()

    def start_session(self):

        print(f"session_number: {self.session_number}")

        """
        The interval periods of this app
        1: work,
        2: break,
        3: work,
        4: break,
        5: work,
        6: break,
        7: work,
        8: long break
        """

        if self.session_number == 8:
            self.current_session = "longB"

            passing_value_for_countdown: int = self.session_times["longB"]
            if self.current_running_seconds >= 0:
                passing_value_for_countdown = self.current_running_seconds

            self.countdown(passing_value_for_countdown, self.application)

            self.application.header_text.configure(text="Long Break")

        elif self.session_number % 2 == 0:
            self.current_session = "shortB"

            passing_value_for_countdown: int = self.session_times["shortB"]
            if self.current_running_seconds >= 0:
                passing_value_for_countdown = self.current_running_seconds
            self.countdown(passing_value_for_countdown, self.application)

            self.application.header_text.configure(text="Short Break")

        elif self.session_number % 2 == 1:
            self.current_session = "focus"

            passing_value_for_countdown: int = self.session_times["focus"]
            if self.current_running_seconds >= 0:
                passing_value_for_countdown = self.current_running_seconds
            self.countdown(passing_value_for_countdown, self.application)

            self.application.header_text.configure(text="Focus")

    def _running_after_every_seconds(self):
        # To be overwritten by controller
        pass

    def _run_after_long_break(self):
        # To be overwritten by controller
        pass

    def _run_after_finishing_session(self):
        # To be overwritten by controller
        pass