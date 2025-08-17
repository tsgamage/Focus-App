from focus import FocusController
import os
from tkinter.messagebox import showinfo

def is_app_running(app_name):
    tasks = os.popen('tasklist').read().lower()
    # return app_name.lower() in tasks
    return tasks.count(app_name.lower()) > 2

if __name__ == "__main__":
    if is_app_running("FocusApp.exe"):
        showinfo("Focus App", "Focus App is already running.")
    else:
        app = FocusController()
        app.mainloop()