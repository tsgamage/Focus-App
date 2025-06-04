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
        self.geometry("350x500")
        self.iconphoto(False, app_icon)
        self.iconphoto(True, app_icon)
        self.resizable(False, False)
        # self.eval('tk::PlaceWindow . center')

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
            bootstyle="success",
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
            cursor="hand2",
        )
        self.start_pause_button.grid(row=5, column=0, columnspan=2, pady=(8, 20))

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

        session_sound_label_frame = tb.LabelFrame(settings_win, text="Set custom session changing sound",
                                                  padding=(10, 5))
        session_sound_label_frame.pack(fill="x", pady=(0, 10))

        self.entry_var = tk.StringVar()
        tb.Entry(session_sound_label_frame, textvariable=self.entry_var, width=27).grid(row=1, column=0, pady=(5),
                                                                                        padx=(0, 10))
        tb.Button(session_sound_label_frame, cursor="hand2", text="Browse", command=self.on_browse, width=8).grid(row=1,
                                                                                                                  column=1)

        custom_timer_input_frame = tb.Labelframe(settings_win, text="Enter times in minutes", padding=(10, 5))
        custom_timer_input_frame.pack(fill="x", pady=(0, 10))

        tb.Label(custom_timer_input_frame, text="Focus Time           :").grid(row=0, column=0, padx=(0, 20),
                                                                               pady=(0, 10))
        tb.Spinbox(custom_timer_input_frame, from_=0, to=120, width=10).grid(row=0, column=1, pady=(0, 10))
        tb.Label(custom_timer_input_frame, text="min").grid(row=0, column=2, pady=(0, 10))

        tb.Label(custom_timer_input_frame, text="Short Break Time :").grid(row=1, column=0, padx=(0, 20), pady=(0, 10))
        tb.Spinbox(custom_timer_input_frame, from_=0, to=30, width=10).grid(row=1, column=1, pady=(0, 10))
        tb.Label(custom_timer_input_frame, text="min").grid(row=1, column=2, pady=(0, 10))

        tb.Label(custom_timer_input_frame, text="Long Break Time  :").grid(row=2, column=0, padx=(0, 20), pady=(0, 10))
        tb.Spinbox(custom_timer_input_frame, from_=0, to=120, width=10, ).grid(row=2, column=1, pady=(0, 10))
        tb.Label(custom_timer_input_frame, text="min").grid(row=2, column=2, pady=(0, 10))

        app_theme_change_frame = tb.Labelframe(settings_win, text="Change application theme", padding=(10, 5))
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
