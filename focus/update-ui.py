from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
class UpdateWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.is_downloading = False
        self.is_Cancelled = False

        self.geometry('300x130')
        self.title('Focus App')
        self.eval('tk::PlaceWindow . center')


        main_label = ttk.Label(self, text='Download in Progress...', font=('Arial', 12))
        main_label.pack(pady=10, padx=10, anchor='center')

        self.progress_bar = ttk.Progressbar(
            self,
            orient='horizontal',
            mode='determinate',
            length=200
        )
        self.progress_bar.pack()

        value_label = ttk.Label(self, text="10.14 / 30.00 MB")
        value_label.pack(pady=2, padx=10, anchor='center')

        btn_frame = tk.Frame(self)
        btn_frame.pack(fill='x', pady=2, padx=40, anchor='center')

        self.start_download_button = ttk.Button(
            btn_frame,
            text='Pause',
            width=15,
            command=self._handle_pause_download,
        )
        self.start_download_button.pack(side='left')

        self.cancel_download_button = ttk.Button(
            btn_frame,
            text='Cancel',
            width=15,
            command=self._handle_cancel_button_click
        )
        self.cancel_download_button.pack(side='right')


    def _handle_cancel_button_click(self):
        if messagebox.askyesno(title='Confirm', message='Are you sure you want to cancel the download?'):
            messagebox.showinfo(title='Download Cancelled', message='Download has been cancelled.')
            self.is_Cancelled = True
            self.destroy()

    def _handle_pause_download(self):
        if self.is_downloading:
            self.start_download_button.config(text='Pause')
            self.is_downloading = False
        else:
            self.start_download_button.config(text='Resume')
            self.is_downloading = True


window = UpdateWindow()
window.mainloop()