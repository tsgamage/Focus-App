from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb

class UpdateWindow():
    def __init__(self):
        super().__init__()

        self.is_downloading = False
        self.is_Cancelled = False

        self.start_download_button = None
        self.cancel_download_button = None

        self.downloaded_progress_text = None
        self.downloaded_progress = None

        self.window = None

    def create_downloading_window(self):

        self.window = tb.Toplevel()
        self.window.geometry('300x100')
        self.window.title('Focus App')
        # self.window.eval('tk::PlaceWindow . center')
        self.window.resizable(False, False)

        # Centering the window
        self.window.update_idletasks()  # Make sure the main window is fully rendered
        x = self.window.winfo_x()
        y = self.window.winfo_y()
        main_width = self.window.winfo_width()
        main_height = self.window.winfo_height()

        win_width = 300
        win_height = 100
        pos_x = x + (main_width // 2) - (win_width // 2)
        pos_y = y + (main_height // 2) - (win_height // 2)

        self.window.geometry(f"{win_width}x{win_height}+{pos_x}+{pos_y}")

        # Make it modal
        self.window.grab_set()  # Prevents clicking on other windows
        self.window.transient()  # Tells OS it's a child of your main app
        self.window.focus()  # Focus on it automatically


        main_label = ttk.Label(self.window, text='Download in progress...', font=('Arial', 12))
        main_label.pack(pady=10, padx=10, anchor='center')

        self.downloaded_progress = tk.DoubleVar(value=0)
        self.downloaded_progress_text = tk.StringVar()
        self.downloaded_progress_text.set("0.00 / 0.00 MB")

        progress_bar = ttk.Progressbar(
            self.window,
            orient='horizontal',
            mode='determinate',
            length=200,
            variable= self.downloaded_progress

        )
        progress_bar.pack()

        value_label = ttk.Label(self.window, textvariable=self.downloaded_progress_text, font=('Arial', 12))
        value_label.pack(pady=10, padx=10, anchor='center')

        self.window.after(500, self._start_download)

        self.window.bind('<Alt-F4>', self.alt_f4)
        self.window.bind('<Escape>', self.escape_press)
        self.window.protocol("WM_DELETE_WINDOW", self.do_exit)


    def do_exit(self,):
        pass

    def alt_f4(self, event):
        pass

    def escape_press(self,*event):
        pass

    def _start_download(self):
        pass