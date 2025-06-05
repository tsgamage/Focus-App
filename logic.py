
from gui import FocusApp
import threading
from time import sleep
import math


app = FocusApp()

current_running_seconds: int = 0

session_times: dict = {"focus":6, "shortB":3, "longB":5}
current_session: str = "focus" # Can use focus, shortB, and longB
session_number: int = 7
session_started: bool = False
timer = ''


def formate_time(seconds:int):
    """ Returns the time in min:sec format """
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

    return f"{timer_min}:{timer_sec}"

def countdown(seconds:int, application):
    global current_running_seconds, timer, session_number

    current_running_seconds = seconds
    if seconds >= 0:
        print(f"seconds: {seconds}")
        print(f"current_session:{current_session}")
        formatted_time = formate_time(seconds)
        application.update_ui_timer(formatted_time)

        used_percentage = math.floor((seconds / session_times[f"{current_session}"]) * 100)
        application.update_ui_meter(used_percentage)

        timer = app.after(1000, countdown,current_running_seconds - 1, app)

    elif current_running_seconds < 0:
        print("Session over")
        session_number += 1
        if session_number > 8:
            reset_variables()
        start_session()

def reset_variables():
    global current_running_seconds
    current_running_seconds = 0
    global session_number
    session_number = 1

def start_session():

    global session_number
    global current_session

    print(f"session_number: {session_number}")

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

    if session_number == 8:
        current_session = "longB"

        passing_value_for_countdown: int = session_times["longB"]
        if current_running_seconds > 0:
            passing_value_for_countdown = current_running_seconds
        countdown(passing_value_for_countdown, app)

        app.header_text.configure(text="Long Break")

    elif session_number % 2 == 0:
        current_session = "shortB"

        passing_value_for_countdown: int = session_times["shortB"]
        if current_running_seconds > 0:
            passing_value_for_countdown = current_running_seconds
        countdown(passing_value_for_countdown, app)

        app.header_text.configure(text="Short Break")

    elif session_number % 2 == 1:
        current_session = "focus"

        passing_value_for_countdown: int = session_times["focus"]
        if current_running_seconds > 0:
            passing_value_for_countdown = current_running_seconds
        countdown(passing_value_for_countdown, app)

        app.header_text.configure(text="Focus")

def pause_session():
    app.after_cancel(timer)

def skip_session():
    global session_number, current_running_seconds
    current_running_seconds = 0
    session_number += 1
    if session_number > 8:
        reset_variables()
    app.start_pause_button.configure(state="disabled")
    handle_start_pause_button()
    app.after(3000, lambda :    app.start_pause_button.configure(state="normal"))

def reset_timer():
    print("Resetting timer")
    global current_running_seconds

    def back_to_normal():
        app.start_pause_button.configure(state="normal")
        app.settings_button.configure(state="normal")
        app.main_bottom_text.configure(text="Paused! Press Start to continue.")
        print("Timer has been reset")

    app.start_pause_button.configure(state="disabled")
    app.skip_button.configure(state="disabled")
    app.reset_timer_button.configure(state="disabled")
    app.settings_button.configure(state="disabled")
    current_running_seconds = 0
    app.update_ui_meter(100)
    app.update_ui_timer(formate_time(session_times[f"{current_session}"]))
    app.main_bottom_text.configure(text="Timer has reset!.")
    app.after(500, back_to_normal)


def handle_start_pause_button():
    global session_started

    if session_started:
        app.start_pause_button.configure(text="Start")
        app.main_bottom_text.configure(text="Paused! Press Start to continue.")
        app.progress_bottom_text.configure(text="Paused! Press Start to continue.")
        app.skip_button.configure(state="normal")
        app.reset_timer_button.configure(state="normal")
        app.settings_button.configure(state="normal")
        session_started = False
        pause_session()
    else:
        app.start_pause_button.configure(text="Pause")
        app.main_bottom_text.configure(text="Only 3 more sessions to for a long break.")
        app.progress_bottom_text.configure(text="Only 3 more sessions to for a long break.")
        app.skip_button.configure(state="disabled")
        app.reset_timer_button.configure(state="disabled")
        app.settings_button.configure(state="disabled")
        session_started = True
        start_session()

app.start_pause_button.configure(command=handle_start_pause_button)
app.skip_button.configure(command=skip_session)
app.reset_timer_button.configure(command=reset_timer)

app.mainloop()