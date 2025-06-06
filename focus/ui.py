import ttkbootstrap as tb
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os

class FocusApp(tb.Window):
    def __init__(self):
        super().__init__()

        self.app_icon_path = "assets/icons/Focus.png"
        app_icon = tk.PhotoImage(file=self.app_icon_path)
        self.loop_time = 0
        self.timer_started = False
        self.minimized = False
        self.user_settings:dict = {}

        self.users_target_focus_periods = tb.IntVar()
        self.users_focus_time = tb.IntVar()
        self.users_short_break_time = tb.IntVar()
        self.users_long_break_time = tb.IntVar()
        self.play_session_sound_tick = tb.BooleanVar()
        self.minimize_to_tray_tick = tb.BooleanVar()


        self.app_theme_name = tk.StringVar()
        self.app_theme_name.set("superhero")
        self.reset_user_settings = False
        self.reset_today_progress = False


        self.title("Focus App")
        self.geometry("350x512")
        self.iconphoto(False, app_icon)
        self.iconphoto(True, app_icon)
        self.resizable(False, False)
        # self.eval('tk::PlaceWindow . center')
        self.style.theme_use(self.app_theme_name.get())
        self.settings_window = None

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

        self.main_meter = tb.Meter(
            master=self.main_tab,
            bootstyle="info",
            metersize=220,
            padding=5,
            amounttotal=100,
            amountused=100,
            metertype="semi",
            # subtext="miles per hour",
            meterthickness=20,
            stripethickness=3,
            showtext=False,
            interactive=False
        )
        self.main_meter.grid(row=2, column=0, columnspan=2)

        self.timer_label = tb.Label(master=self.main_tab, text="00:00", font=("poppins", 28), bootstyle="info")
        self.timer_label.grid(row=2, column=0, columnspan=2)

        self.play_session_sound_tick.set(True)
        self.sound_tick = tb.Checkbutton(
            master=self.main_tab,
            text="Play Session Sound",
            bootstyle="primary-round-toggle",
            cursor="hand2",
            variable=self.play_session_sound_tick
        )
        self.sound_tick.grid(row=3, column=0)

        self.minimize_to_tray_tick.set(True)
        self.minimize_to_tray = tb.Checkbutton(
            master=self.main_tab,
            text="Minimize to Taskbar",
            bootstyle="primary-round-toggle",
            cursor="hand2",
            variable=self.minimize_to_tray_tick
        )
        self.minimize_to_tray.grid(row=3, column=1)

        reset_btn_frame = tb.Frame(self.main_tab)
        reset_btn_frame.grid(row=4, column=0, columnspan=2, pady=(20, 0), sticky="w")

        self.skip_button = tb.Button(
            master=reset_btn_frame,
            text="Skip >>",
            width=8,
            bootstyle="warning",
            state="disabled"
        )
        self.skip_button.grid(row=0, column=0, padx=(0, 7))

        self.reset_timer_button = tb.Button(
            master=reset_btn_frame,
            text="Reset Timer",
            takefocus=False,
            bootstyle="danger",
            width=21,
            state="disabled"
        )
        self.reset_timer_button.grid(row=0, column=1)

        self.settings_button = tb.Button(
            master=reset_btn_frame,
            text="Settings",
            width=8,
            bootstyle="primary",
            cursor="hand2",
            command=self.open_settings
        )
        self.settings_button.grid(row=0, column=2, padx=(7, 0))

        self.start_pause_button = tb.Button(
            master=self.main_tab,
            text="Start",
            width=49,
            bootstyle="success",
            cursor="hand2"
        )
        self.start_pause_button.grid(row=5, column=0, columnspan=2, pady=(8, 0))


        tb.Separator(self.main_tab, orient='horizontal').grid(row=6, column=0, columnspan=2, pady=(10, 2), sticky="ew")


        self.main_bottom_text = tb.Label(master=self.main_tab,text="Made with 🖤 by Princess Software Solutions", font=("poppins", 10), bootstyle="info")
        self.main_bottom_text.grid(row=7, column=0, columnspan=2)

        #     ---------------------------- PROGRESS TAB ----------------------------

        self.focus_progress_today_frame = tb.LabelFrame(self.progress_tab, text="  Focus Progress Today  ", padding=10)
        self.focus_progress_today_frame.pack(fill="x", padx=0, pady=0)

        # Create a frame for the first line
        first_line_frame = tb.Frame(self.focus_progress_today_frame)
        first_line_frame.pack(fill="x", pady=2)

        self.focus_sessions_today_label = tb.Label(first_line_frame, text="Total Focus Sessions  :", font=("poppins", 12))
        self.focus_sessions_today_label.pack(side="left")
        self.focus_sessions_today_value = tb.Label(first_line_frame, text="9", font=("poppins", 12), bootstyle="success")
        self.focus_sessions_today_value.pack(side="right")

        # Create a frame for the second line
        second_line_frame = tb.Frame(self.focus_progress_today_frame)
        second_line_frame.pack(fill="x", pady=2)

        self.total_focus_minutes = tb.Label(second_line_frame, text="Total Focus Time         :", font=("poppins", 12))
        self.total_focus_minutes.pack(side="left")
        self.total_focus_minutes_value = tb.Label(second_line_frame, text="9h & 44min", font=("poppins", 12), bootstyle="success")
        self.total_focus_minutes_value.pack(side="right")

        # Create a frame for the third line
        third_line_frame = tb.Frame(self.focus_progress_today_frame)
        third_line_frame.pack(fill="x", pady=2)

        self.total_breaks_today_label = tb.Label(third_line_frame, text="Total Break Time         :", font=("poppins", 12))
        self.total_breaks_today_label.pack(side="left")
        self.total_breaks_today_value = tb.Label(third_line_frame, text="1h & 44min", font=("poppins", 12), bootstyle="warning")
        self.total_breaks_today_value.pack(side="right")

        self.focus_progress_target_frame = tb.LabelFrame(self.progress_tab, text="  Focus Target  ", padding=10, )
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
            interactive=False
        )
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
            interactive=False
        )
        self.target_min_meter.pack()
        self.target_min_meter_label = tb.Label(target_time_frame, text="Target Focus", font=("poppins", 12))
        self.target_min_meter_label2 = tb.Label(target_time_frame, text="Minutes", font=("poppins", 12))
        self.target_min_meter_label.pack()
        self.target_min_meter_label2.pack()

        self.reset_progress_button = tb.Button(self.progress_tab, text="Reset Today Progress", bootstyle="danger-outline", cursor="hand2", command=self.handle_reset_today_progress_click, takefocus=False)
        self.reset_progress_button.pack(pady=(12, 0))


        tb.Separator(self.progress_tab, orient='horizontal').pack( fill="x", pady=(10, 2))

        self.progress_bottom_text = tb.Label(master=self.progress_tab, text="Where Elegance Meets Logic.", font=("poppins", 10), bootstyle="info")
        self.progress_bottom_text.pack()

    def handle_reset_today_progress_click(self):
        if tk.messagebox.askyesno("Reset Progress", "Are you sure you want to reset today's progress?"):
            if tk.messagebox.askyesno("Reset Progress","Reset Today Progress?"):
                self.reset_today_progress = True


    # def on_browse(self):
    #     """Callback for directory browse"""
    #     path = filedialog.askopenfilename(title="Select an MP3 File", filetypes=[("MP3 Files", "*.mp3")])
    #     if path:
    #         self.sound_file_path_var.set(path)
    #
    #     os.startfile(path)

    def open_settings(self):
        self.settings_window = tb.Toplevel()
        self.settings_window.title("Settings")
        self.settings_window.geometry("300x450")
        self.settings_window.configure(pady=15, padx=10)
        self.settings_window.resizable(False, False)
        self.settings_window.grid_columnconfigure(0, weight=1)
        self.settings_window.grid_rowconfigure(0, weight=1)

        # Centering the window
        self.update_idletasks()  # Make sure the main window is fully rendered
        x = self.winfo_x()
        y = self.winfo_y()
        main_width = self.winfo_width()
        main_height = self.winfo_height()

        win_width = 300
        win_height = 395
        pos_x = x + (main_width // 2) - (win_width // 2)
        pos_y = y + (main_height // 2) - (win_height // 2)

        self.settings_window.geometry(f"{win_width}x{win_height}+{pos_x}+{pos_y}")

        # Make it modal
        self.settings_window.grab_set()  # Prevents clicking on other windows
        self.settings_window.transient(self)  # Tells OS it's a child of your main app
        self.settings_window.focus()  # Focus on it automatically

        # override close (X) button behavior
        def on_close():
            if tk.messagebox.askyesno("Exit", "Close without saving?"):
                self.settings_window.destroy()

        self.settings_window.protocol("WM_DELETE_WINDOW", on_close)

        #  Frame for users targets ----------------
        users_targets_frame = tb.Labelframe(self.settings_window, text="  Enter your Targets per day  ", padding=(10, 10))
        users_targets_frame.pack(fill="x", pady=(0, 10))

        tb.Label(users_targets_frame, text="Target Focus Periods per day :").pack(side="left")
        tb.Spinbox(users_targets_frame,textvariable= self.users_target_focus_periods, from_=0, to=10, width=2, state="readonly").pack(side="right")

        # Frame for custom timer inputs ----------------
        custom_timer_input_frame = tb.Labelframe(self.settings_window, text="  Enter times in minutes  ", padding=(10, 5))
        custom_timer_input_frame.pack(fill="x", pady=(0, 10))

        # First line - Focus Time
        focus_line = tb.Frame(custom_timer_input_frame)
        focus_line.pack(fill="x", pady=2)

        tb.Label(focus_line, text="Focus Time in minutes :").pack(side="left")
        tb.Spinbox(focus_line,textvariable= self.users_focus_time, from_=0, to=120, width=5, state="readonly").pack(side="right")

        # Second line - Short Break Time
        short_break_line = tb.Frame(custom_timer_input_frame)
        short_break_line.pack(fill="x", pady=2)

        tb.Label(short_break_line, text="Short Break Time in minutes :").pack(side="left")
        tb.Spinbox(short_break_line,textvariable= self.users_short_break_time, from_=0, to=15, width=5, state="readonly").pack(side="right")

        # Third line - Long Break Time
        long_break_line = tb.Frame(custom_timer_input_frame)
        long_break_line.pack(fill="x", pady=2)

        tb.Label(long_break_line, text="Long Break Time in minutes :").pack(side="left")
        tb.Spinbox(long_break_line,textvariable= self.users_long_break_time, from_=0, to=30, width=5, state="readonly").pack(side="right")

        # # Frame for the sound browse button ----------------
        # session_sound_label_frame = tb.LabelFrame(self.settings_window, text="  Set custom session changing sound  ",padding=(10, 10))
        # session_sound_label_frame.pack(fill="x", pady=(0, 10))
        #
        # self.sound_file_path_var.set("No custom sound set")
        # tb.Entry(session_sound_label_frame, textvariable=self.sound_file_path_var, width=27, state="readonly").pack(side="left")
        # tb.Button(session_sound_label_frame, cursor="hand2", text="Browse", command=self.on_browse, width=8).pack(side="right")

        # Frame for change app theme ----------------
        app_theme_change_frame = tb.Labelframe(self.settings_window, text="  Change application theme  ", padding=(10, 10))
        app_theme_change_frame.pack(fill="x", pady=(0, 15))



        tb.Button(app_theme_change_frame, cursor="hand2", bootstyle="info", width=10, text="Blue", command=lambda : self.change_app_theme("superhero")).grid(row=0,column=0,padx=(0, 5))
        tb.Button(app_theme_change_frame, cursor="hand2", bootstyle="dark", width=10, text="Dark", command=lambda : self.change_app_theme("darkly")).grid(row=0, column=1,padx=(0, 5))
        tb.Button(app_theme_change_frame, cursor="hand2", bootstyle="light", width=10, text="White", command=lambda : self.change_app_theme("flatly")).grid(row=0,column=2)

        tb.Button(self.settings_window, cursor="hand2", bootstyle="danger-outline", text="Reset all settings to defaults",command=self._on_settings_reset, takefocus=False).pack(fill="x", pady=(0, 10))
        tb.Button(self.settings_window, cursor="hand2", bootstyle="success", text="Save Changes",command=self._on_settings_save, takefocus=False).pack(fill="x")

    def change_app_theme(self, theme):
        self.app_theme_name.set(theme)
        self.style.theme_use(self.app_theme_name.get())

    def update_ui_timer(self, formated_time:str):
        """Update the timer label"""
        self.timer_label.configure(text=formated_time)

    def update_timer_color(self, amount_used:int):
        """Update the timer & label color"""
        if amount_used > 60:
            self.main_meter.configure(bootstyle="warning")
            self.timer_label.configure(bootstyle="warning")
        elif amount_used > 30:
            self.main_meter.configure(bootstyle="info")
            self.timer_label.configure(bootstyle="info")
        elif amount_used > 0:
            self.main_meter.configure(bootstyle="success")
            self.timer_label.configure(bootstyle="success")

        elif amount_used == 0:
            self.main_meter.configure(bootstyle="primary")
            self.timer_label.configure(bootstyle="primary")

    def update_ui_meter(self, amount_used:int):
        """Update the meter in the main tab"""
        # self.update_timer_color(amount_used)
        self.main_meter.configure(amountused=amount_used)

    def _on_settings_save(self):
        # This function will be overwritten by the controller
        self.user_settings = {
                    "theme": self.app_theme_name.get(),  # from a ttkbootstrap StringVar
                    "users_target_sessions": int(self.users_target_focus_periods.get()),
                    "users_focus_time": int(self.users_focus_time.get()),
                    "users_short_break_time": int(self.users_short_break_time.get()),
                    "users_long_break_time": int(self.users_long_break_time.get()),
        }
        # if tk.messagebox.showinfo("Settings Saved", "Settings saved successfully!"):
        self.settings_window.destroy()

    def _on_settings_reset(self):
        # This function will be overwritten by the controller
        if tk.messagebox.askyesno("Reset Settings", "Are you sure you want to reset all settings to default values?"):
            self.reset_user_settings = True
