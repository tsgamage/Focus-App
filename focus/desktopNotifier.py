import threading
import winsound
from plyer import notification
import os

class DesktopNotifier:
    def __init__(self, app_name="Focus App",):
        """
        A cross-platform desktop notifier with optional sound (Windows only).
        :param app_name: Name of the application (shown in some OS notifications)

        """
        self.app_name = app_name

    def _play_sound(self):
        """Play the default Windows notification sound."""
        try:
            winsound.PlaySound("SystemNotification", winsound.SND_ALIAS)
        except RuntimeError:
            pass  # Ignore if sound fails

    def send_notification(self, title, message,icon_path,  timeout=5, sound=False):
        path = icon_path if icon_path and os.path.exists(icon_path) else None
        """
        Send a desktop notification.

        :param title: Title of the notification
        :param message: Message body
        :param timeout: Duration in seconds before notification disappears
        """
        # Play sound in the background thread
        if sound:
            threading.Thread(target=self._play_sound, daemon=True).start()

        # Show notification
        notification.notify(
            title=title,
            message=message,
            app_name=self.app_name,
            app_icon=path,
            timeout=timeout
        )