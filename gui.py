import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
import math


class FocusApp(tb.Window):
    def __init__(self):
        super().__init__(themename='superhero')

        app_icon = tk.PhotoImage(file="./assets/icon/Focus.png")
        self.loop_time = 0

        self.WORK_MIN = 5
        self.SHORT_BREAK_MIN = 3
        self.LONG_BREAK_MIN = 7

        # Timing in seconds
        self.WORKING_TIME_SEC = self.WORK_MIN
        self.SMALL_BREAK_SEC = self.SHORT_BREAK_MIN
        self.LONG_BREAK_SEC = self.LONG_BREAK_MIN

        self.title("Focus App")
        self.geometry("350x500")
        self.iconphoto(False, app_icon)
        self.iconphoto(True, app_icon)
        self.resizable(False, False)

        self.notebook = tb.Notebook()
        self.notebook.grid(row=0, column=0, sticky='nsew', padx=0, pady=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_tab = tb.Frame(self.notebook)
        self.stats_tab = tb.Frame(self.notebook)

        self.notebook.add(self.main_tab, text=f"{' ' * 16}Focus Zone{' ' * 16}", padding=20)
        self.notebook.add(self.stats_tab, text=f"{' ' * 18}Progress{' ' * 20}", padding=20)

        self.main_tab.grid_columnconfigure(0, weight=1)
        self.main_tab.grid_columnconfigure(1, weight=1)
        self.stats_tab.grid_columnconfigure(0, weight=1)
        self.stats_tab.grid_columnconfigure(1, weight=1)

        self.header_text = tb.Label(master=self.main_tab, text="Focus App", font=("montserrat", 26))
        self.header_text.grid(row=0, column=0, columnspan=2, )

        self.quote_text = tb.Label(master=self.main_tab, text="-Never give in and never give up-", font=("poppins", 10))
        self.quote_text.grid(row=1, column=0, columnspan=2)

        self.meter = tb.Meter(
            master=self.main_tab,
            bootstyle="primary",
            metersize=220,
            padding=5,
            amounttotal=60,
            amountused=0,
            metertype="semi",
            # subtext="miles per hour",
            meterthickness=20,
            stripethickness=3,
            showtext=False,
            interactive=True
        )
        self.meter.grid(row=2, column=0, columnspan=2)

        self.timer = tb.Label(master=self.main_tab, text="25:00", font=("poppins", 22), bootstyle="primary")
        self.timer.grid(row=2, column=0, columnspan=2)

        self.sound_tick_value = tb.StringVar()
        self.sound_tick_value.set("1")

        self.sound_tick = tb.Checkbutton(
            master=self.main_tab,
            text="Play Sound",
            bootstyle="primary-round-toggle",
            cursor="hand2",
            variable=self.sound_tick_value
        )
        self.sound_tick.grid(row=3, column=0)

        self.minimize_to_tray_value = tb.StringVar()
        self.minimize_to_tray_value.set("1")

        self.minimize_to_tray = tb.Checkbutton(
            master=self.main_tab,
            text="Minimize to Tray",
            bootstyle="primary-round-toggle",
            cursor="hand2",
            variable=self.minimize_to_tray_value
        )
        self.minimize_to_tray.grid(row=3, column=1)

        self.reset_button = tb.Button(
            master=self.main_tab,
            text="Reset",
            width=22,
            bootstyle="danger",
            cursor="hand2",
            state="disabled"
        )
        self.reset_button.grid(row=4, column=0, pady=(20, 0), padx=(0, 10))

        self.settings_button = tb.Button(
            master=self.main_tab,
            text="Settings",
            width=22,
            bootstyle="primary",
            cursor="hand2",
            command=self.open_settings
        )
        self.settings_button.grid(row=4, column=1, pady=(20, 0))

        self.start_pause_button = tb.Button(
            master=self.main_tab,
            text="Start",
            width=48,
            bootstyle="success",
            cursor="hand2"
        )
        self.start_pause_button.grid(row=5, column=0, columnspan=2, pady=(8, 20))

    def open_settings(self):
        settings_win = tk.Toplevel(self)
        settings_win.title("Settings")
        settings_win.geometry("300x300")
        settings_win.resizable(False, False)

        # Centering the window
        self.update_idletasks()  # Make sure the main window is fully rendered
        x = self.winfo_x()
        y = self.winfo_y()
        main_width = self.winfo_width()
        main_height = self.winfo_height()

        win_width = 300
        win_height = 300
        pos_x = x + (main_width // 2) - (win_width // 2)
        pos_y = y + (main_height // 2) - (win_height // 2)

        settings_win.geometry(f"{win_width}x{win_height}+{pos_x}+{pos_y}")

        # Make it modal
        settings_win.grab_set()  # Prevents clicking on other windows
        settings_win.transient(self)  # Tells OS it's a child of your main app
        settings_win.focus()  # Focus on it automatically

        # override close (X) button behavior
        def on_close():
            # You can put validation logic here before allowing it to close
            if tk.messagebox.askyesno("Exit", "Close without saving?"):
                settings_win.destroy()

        settings_win.protocol("WM_DELETE_WINDOW", on_close)

        tb.Label(settings_win, text="Sound", font=("Segoe UI", 12)).pack(pady=10)
        tb.Checkbutton(settings_win, text="Play sound at session end").pack()

        tb.Label(settings_win, text="Theme", font=("Segoe UI", 12)).pack(pady=10)
        tb.Combobox(settings_win, values=["Superhero", "Darkly", "Flatly"]).pack()

        tb.Button(settings_win, text="Save", command=settings_win.destroy).pack(pady=20)

    # The function that's control the app's state
    def call_timer(self):
        """
        The interval periods of this app

        1: 25 minutes of work,
        2: 5-minute break,
        3: 25 minutes of work,
        4: 5-minute break,
        5: 25 minutes of work,
        6: 5-minute break,
        7: 25 minutes of work,
        8: 20 minutes of long break

        """

        #  Keep track of how many times this function called
        self.loop_time += 1
        # Removed always on top status from app, So user can use another app without distracted from with this app's window
        self.attributes("-topmost", False)

        # If this function runs 8 times, It means it's time for a long break
        if self.loop_time == 8:
            self.update_timer(self.LONG_BREAK_SEC)

        #  All the loop time numbers for a short break are odd value, So this will check whether its odd and set app's state to short Break
        elif self.loop_time % 2 == 0:
            self.update_timer(self.SMALL_BREAK_SEC)

        #  All the loop time numbers for a Working time are even value, So this will check whether its even and set app's state to working
        elif self.loop_time % 2 == 1:
            self.update_timer(self.WORKING_TIME_SEC)

    def update_timer(self, count):
        timer_min = math.floor(count / 60)
        timer_sec = count % 60

        # Adding a '0' to the front of minutes when it is smaller than 10
        if timer_min < 10:
            timer_min = f"0{timer_min}"

        # Adding a '0' to the front of seconds when it is smaller than 10
        if timer_sec < 10:
            timer_sec = f"0{timer_sec}"

        # Adding 00 to the seconds when it is zero
        if timer_sec == 0:
            timer_sec = "00"

        self.timer.configure(text=f"{timer_min}:{timer_sec}")

        if count > 0:
            global timer
            # Runs the whole function continuously after every second
            timer = self.after(1000, self.update_timer, count - 1)

        else:
            # When the timer hits 'zero,' it means it's time to change the app state (Working, Short Break, Long Break)
            # Before calling the call_timer function, the app needs to go to the top of the screen
            # So, the user knows when it's time to a break, or it's time to work
            self.attributes("-topmost", True)

            # After the application comes to the top of the screen, the call_timer function will be executed
            self.call_timer()
