from idlelib.debugger_r import frametable
from tkinter.ttk import Style

import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pathlib
import os


class FocusApp(tb.Window):
    def __init__(self):
        super().__init__(themename='superhero')

        self.app_icon_path = "./assets/icon/Focus.png"
        app_icon = tk.PhotoImage(file=self.app_icon_path)
        self.loop_time = 0
        self.timer_started = False
        self.timer = None
        self.minimized = False
        self.users_working_min = 0
        self.users_short_break_min = 0
        self.users_long_break_min = 0

        self.WORK_MIN = 5
        self.SHORT_BREAK_MIN = 3
        self.LONG_BREAK_MIN = 7

        # Timing in seconds
        self.WORKING_TIME_SEC = self.WORK_MIN
        self.SMALL_BREAK_SEC = self.SHORT_BREAK_MIN
        self.LONG_BREAK_SEC = self.LONG_BREAK_MIN

        self.title("Focus App")
        self.geometry("350x480")
        self.iconphoto(False, app_icon)
        self.iconphoto(True, app_icon)
        self.resizable(False, False)
        # self.eval('tk::PlaceWindow . center')

        self.notebook = tb.Notebook()
        self.notebook.grid(row=0, column=0, sticky='nsew', padx=0, pady=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_tab = tb.Frame(self.notebook)
        self.progress_tab = tb.Frame(self.notebook)

        self.notebook.add(self.main_tab, text=f"{' ' * 16}Focus Zone{' ' * 16}", padding=20)
        self.notebook.add(self.progress_tab, text=f"{' ' * 18}Progress{' ' * 20}", padding=20)

        self.main_tab.grid_columnconfigure(0, weight=1)
        self.main_tab.grid_columnconfigure(1, weight=1)
        self.progress_tab.grid_columnconfigure(0, weight=1)
        self.progress_tab.grid_columnconfigure(1, weight=1)

        #     ---------------------------- MAIN TAB ----------------------------

        self.header_text = tb.Label(master=self.main_tab, text="Focus App", font=("montserrat", 26))
        self.header_text.grid(row=0, column=0, columnspan=2, )

        self.quote_text = tb.Label(master=self.main_tab, text="-Never give in and never give up-", font=("poppins", 10))
        self.quote_text.grid(row=1, column=0, columnspan=2)

        self.meter = tb.Meter(
            master=self.main_tab,
            bootstyle="primary",
            metersize=220,
            padding=5,
            amounttotal=100,
            amountused=60,
            metertype="semi",
            # subtext="miles per hour",
            meterthickness=20,
            stripethickness=3,
            showtext=False,
            interactive=True
        )
        self.meter.grid(row=2, column=0, columnspan=2)

        self.timer_label = tb.Label(master=self.main_tab, text="25:00", font=("poppins", 22), bootstyle="primary")
        self.timer_label.grid(row=2, column=0, columnspan=2)

        self.sound_tick_value = tb.StringVar()
        self.sound_tick_value.set("1")

        self.sound_tick = tb.Checkbutton(
            master=self.main_tab,
            text="Play Session Sound",
            bootstyle="primary-round-toggle",
            cursor="hand2",
            variable=self.sound_tick_value
        )
        self.sound_tick.grid(row=3, column=0)

        self.minimize_to_tray_value = tb.StringVar()
        self.minimize_to_tray_value.set("1")

        self.minimize_to_tray = tb.Checkbutton(
            master=self.main_tab,
            text="Minimize to Taskbar",
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
            # state="disabled"
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
            cursor="hand2",
        )
        self.start_pause_button.grid(row=5, column=0, columnspan=2, pady=(8, 20))

        #     ---------------------------- PROGRESS TAB ----------------------------

        self.focus_progress_today_frame = tb.LabelFrame(self.progress_tab, text="  Focus Progress Today  ",
                                                        padding=10)
        self.focus_progress_today_frame.pack(fill="x", padx=0, pady=0)

        # Create a frame for the first line
        first_line_frame = tb.Frame(self.focus_progress_today_frame)
        first_line_frame.pack(fill="x", pady=2)

        self.focus_sessions_today_label = tb.Label(first_line_frame, text="Total Focus Sessions  :",
                                                   font=("poppins", 12))
        self.focus_sessions_today_label.pack(side="left")
        self.focus_sessions_today_value = tb.Label(first_line_frame, text="9", font=("poppins", 12),
                                                   bootstyle="success")
        self.focus_sessions_today_value.pack(side="right")

        # Create a frame for the second line
        second_line_frame = tb.Frame(self.focus_progress_today_frame)
        second_line_frame.pack(fill="x", pady=2)

        self.total_focus_minutes = tb.Label(second_line_frame, text="Total Focus Time         :", font=("poppins", 12))
        self.total_focus_minutes.pack(side="left")
        self.total_focus_minutes_value = tb.Label(second_line_frame, text="9h & 44min", font=("poppins", 12),
                                                  bootstyle="success")
        self.total_focus_minutes_value.pack(side="right")

        # Create a frame for the third line
        third_line_frame = tb.Frame(self.focus_progress_today_frame)
        third_line_frame.pack(fill="x", pady=2)

        self.total_breaks_today_label = tb.Label(third_line_frame, text="Total Break Time         :",
                                                 font=("poppins", 12))
        self.total_breaks_today_label.pack(side="left")
        self.total_breaks_today_value = tb.Label(third_line_frame, text="1h & 44min", font=("poppins", 12),
                                                 bootstyle="warning")
        self.total_breaks_today_value.pack(side="right")

        self.focus_progress_target_frame = tb.LabelFrame(self.progress_tab, text="  Focus Target  ",
                                                         padding=10, )
        self.focus_progress_target_frame.pack(fill="x", padx=0, pady=(8, 0))

        target_sessions_frame = tb.Frame(self.focus_progress_target_frame)
        target_sessions_frame.pack(side="left")

        self.focus_target_meter = tb.Meter(target_sessions_frame,
                                           bootstyle="success",
                                           metersize=100,
                                           padding=5,
                                           amounttotal=10,
                                           amountused=8,
                                           metertype="semi",
                                           subtext="8/10",
                                           meterthickness=15,
                                           showtext=False,
                                           interactive=True)
        self.focus_target_meter.pack()
        self.focus_target_meter_label = tb.Label(target_sessions_frame, text="Target Focus", font=("poppins", 12))
        self.focus_target_meter_label2 = tb.Label(target_sessions_frame, text="Sessions", font=("poppins", 12))
        self.focus_target_meter_label.pack(pady=(0, 0))
        self.focus_target_meter_label2.pack(pady=(0, 0))

        tb.Separator(self.focus_progress_target_frame, orient='vertical').pack(side="left", fill="y", padx=(35, 0))

        target_time_frame = tb.Frame(self.focus_progress_target_frame)
        target_time_frame.pack(side="right")

        self.target_min_meter = tb.Meter(target_time_frame,
                                         bootstyle="warning",
                                         metersize=100,
                                         padding=5,
                                         amounttotal=300,
                                         amountused=120,
                                         metertype="semi",
                                         subtext="120/300",
                                         meterthickness=15,
                                         showtext=False,
                                         interactive=True)
        self.target_min_meter.pack()
        self.target_min_meter_label = tb.Label(target_time_frame, text="Target Focus", font=("poppins", 12))
        self.target_min_meter_label2 = tb.Label(target_time_frame, text="Minutes", font=("poppins", 12))
        self.target_min_meter_label.pack()
        self.target_min_meter_label2.pack()

        self.reset_progress_button = tb.Button(self.progress_tab, text="Reset Today Progress",
                                               bootstyle="danger-outline", cursor="hand2", command=self.reset_progress, takefocus=False)
        self.reset_progress_button.pack(pady=(12,0))

    def reset_progress(self):
        if tk.messagebox.askyesno("Reset Progress", "Are you sure you want to reset today's progress?"):
            tk.messagebox.askyesno("Reset Progress",
                                   "Reset Today Progress?")

    def on_browse(self):
        """Callback for directory browse"""
        path = filedialog.askopenfilename(title="Select an MP3 File", filetypes=[("MP3 Files", "*.mp3")])
        if path:
            self.entry_var.set(path)

        os.startfile(path)

    def open_settings(self):
        settings_win = tb.Toplevel()
        settings_win.title("Settings")
        settings_win.geometry("300x350")
        settings_win.configure(pady=10, padx=10)
        settings_win.resizable(False, False)

        # Centering the window
        self.update_idletasks()  # Make sure the main window is fully rendered
        x = self.winfo_x()
        y = self.winfo_y()
        main_width = self.winfo_width()
        main_height = self.winfo_height()

        win_width = 300
        win_height = 350
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

        settings_win.grid_columnconfigure(0, weight=1)
        settings_win.grid_rowconfigure(0, weight=1)

        session_sound_label_frame = tb.LabelFrame(settings_win, text="  Set custom session changing sound  ",
                                                  padding=(10, 5))
        session_sound_label_frame.pack(fill="x", pady=(0, 10))

        self.entry_var = tk.StringVar()
        tb.Entry(session_sound_label_frame, textvariable=self.entry_var, width=27).grid(row=1, column=0, pady=(5),
                                                                                        padx=(0, 10))
        tb.Button(session_sound_label_frame, cursor="hand2", text="Browse", command=self.on_browse, width=8).grid(row=1,
                                                                                                                  column=1)

        custom_timer_input_frame = tb.Labelframe(settings_win, text="  Enter times in minutes  ", padding=(10, 5))
        custom_timer_input_frame.pack(fill="x", pady=(0, 10))

        tb.Label(custom_timer_input_frame, text="Focus Time           :").grid(row=0, column=0, padx=(0, 20),
                                                                               pady=(0, 10))
        tb.Spinbox(custom_timer_input_frame, from_=0, to=120, width=10, state="readonly").grid(row=0, column=1,
                                                                                               pady=(0, 10))
        tb.Label(custom_timer_input_frame, text="min").grid(row=0, column=2, pady=(0, 10))

        tb.Label(custom_timer_input_frame, text="Short Break Time :").grid(row=1, column=0, padx=(0, 20), pady=(0, 10))
        tb.Spinbox(custom_timer_input_frame, from_=0, to=30, width=10, state="readonly").grid(row=1, column=1,
                                                                                              pady=(0, 10))
        tb.Label(custom_timer_input_frame, text="min").grid(row=1, column=2, pady=(0, 10))

        tb.Label(custom_timer_input_frame, text="Long Break Time  :").grid(row=2, column=0, padx=(0, 20), pady=(0, 10))
        tb.Spinbox(custom_timer_input_frame, from_=0, to=120, width=10, state="readonly").grid(row=2, column=1,
                                                                                               pady=(0, 10))
        tb.Label(custom_timer_input_frame, text="min").grid(row=2, column=2, pady=(0, 10))

        app_theme_change_frame = tb.Labelframe(settings_win, text="  Change application theme  ", padding=(10, 5))
        app_theme_change_frame.pack(fill="x", pady=(0, 10))

        tb.Button(app_theme_change_frame, cursor="hand2", bootstyle="primary", width=10, text="Blue").grid(row=0,
                                                                                                           column=0,
                                                                                                           padx=(0,
                                                                                                                 5))
        tb.Button(app_theme_change_frame, cursor="hand2", bootstyle="dark", width=9, text="Dark").grid(row=0, column=1,
                                                                                                       padx=(0, 5))
        tb.Button(app_theme_change_frame, cursor="hand2", bootstyle="light", width=10, text="White").grid(row=0,
                                                                                                          column=2)

        tb.Button(settings_win, cursor="hand2", bootstyle="success", text="Save Changes", command=settings_win.destroy,
                  width=40).pack(
            fill="x")
