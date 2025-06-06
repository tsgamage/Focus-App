
from .ui import FocusApp
from .core import Sessions
from .settings import FocusSettings

from tkinter import messagebox

#  These all for the tray icon
from ttkbootstrap.toast import ToastNotification
import pystray
from pystray import MenuItem
from PIL import Image
import threading

class FocusController(FocusApp, Sessions, FocusSettings):
    def __init__(self):
        FocusApp.__init__(self)
        FocusSettings.__init__(self)
        Sessions.__init__(self, self)

        self.is_minimized = False
        self.window_bottom_text = "Only 3 more sessions to for a long break."
        self.link_buttons()
        self.update_ui_settings_with_saved_settings(start=True)

    def link_buttons(self):
        self.bind("<Unmap>",self.on_minimize)
        self.start_pause_button.configure(command=self.handle_start_pause_button)
        self.skip_button.configure(command=self.skip_session)
        self.reset_timer_button.configure(command=self.reset_timer)

    def pause_session(self):
        self.after_cancel(self.timer)

    def skip_session(self):
        self.current_running_seconds = -1
        self.session_number += 1
        if self.session_number > 8:
            self.reset_variables()
        self.start_pause_button.configure(state="disabled", cursor="arrow")
        self.handle_start_pause_button()
        self.after(3000, lambda :    self.start_pause_button.configure(state="normal", cursor="hand2")  )

    def reset_timer(self):
        def back_to_normal():
            # Enable buttons
            self.start_pause_button.configure(state="normal", cursor="hand2")
            self.settings_button.configure(state="normal", cursor="hand2")
            self.main_bottom_text.configure(text="Paused! Press Start to continue.")

        # Disable all Buttons
        self.reset_timer_button.configure(state="disabled", cursor="arrow")
        self.skip_button.configure(state="disabled", cursor="arrow")
        self.settings_button.configure(state="disabled", cursor="arrow")
        self.start_pause_button.configure(state="disabled", cursor="arrow")

        self.current_running_seconds = -1
        self.update_ui_meter(100)
        self.update_ui_timer(self.formate_time(self.session_times[f"{self.current_session}"]))
        self.main_bottom_text.configure(text="Timer has reset!.")
        self.after(500, back_to_normal)

    def handle_start_pause_button(self):

        if self.session_started:
            self.session_started = False
            self.start_pause_button.configure(text="Start")

            # Enable all buttons
            self.reset_timer_button.configure(state="normal", cursor="hand2")
            self.skip_button.configure(state="normal", cursor="hand2")
            self.settings_button.configure(state="normal", cursor="hand2")

            self.main_bottom_text.configure(text="Paused! Press Start to continue.")
            self.progress_bottom_text.configure(text="Paused! Press Start in Focus Zone to continue.")
            self.pause_session()
        else:
            self.session_started = True
            self.start_pause_button.configure(text="Pause")

            # Disable all buttons
            self.reset_timer_button.configure(state="disabled", cursor="arrow")
            self.skip_button.configure(state="disabled", cursor="arrow")
            self.settings_button.configure(state="disabled", cursor="arrow")

            self.main_bottom_text.configure(text=self.window_bottom_text)
            self.progress_bottom_text.configure(text=self.window_bottom_text)
            self.start_session()

    def hide_window(self):
        def quit_window(icon, item):
            icon.stop()
            # self.destroy()
            self.quit()

        def show_window(icon, item):
            self.is_minimized = False
            icon.stop()
            self.after(0, self.deiconify)

        def show_about():
            toast = ToastNotification(
                title="About Focus App",
                message="Made with 🖤 by Princess Software Solutions",
                duration=5000,
                alert=True,
                icon="🖤",
            )
            toast.show_toast()

        self.withdraw()
        image = Image.open("assets/icons/Focus.png")
        menu = (MenuItem("Restore", show_window, default=True),MenuItem("About", show_about), MenuItem('Quit', quit_window))
        tray_icon = pystray.Icon("Focus", image, "Focus App", menu)
        threading.Thread(target=tray_icon.run).start()

    def on_minimize(self, event):
        if self.minimize_to_tray_tick.get():
            if self.state() == 'iconic' and not self.is_minimized:
                self.is_minimized = True
                self.hide_window()

    def _on_settings_save(self):
        super()._on_settings_save()
        self.save_user_settings(self.user_settings)

    def _on_settings_reset(self):
        super()._on_settings_reset()
        if self.reset_user_settings:
            self.reset_settings()
            self.update_ui_settings_with_saved_settings()
            self.reset_user_settings = False

    def update_ui_settings_with_saved_settings(self, start = False):
        self.users_target_focus_periods.set(self.saved_settings["user"]["users_target_sessions"])
        self.users_focus_time.set(self.saved_settings["user"]["users_focus_time"])
        self.users_short_break_time.set(self.saved_settings["user"]["users_short_break_time"])
        self.users_long_break_time.set(self.saved_settings["user"]["users_long_break_time"])
        if start:
            self.change_app_theme(self.saved_settings["user"]["theme"])