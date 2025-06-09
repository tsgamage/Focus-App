from .updateWindow import UpdateWindow
import json
import threading
import requests
import math
import os
from tkinter import messagebox
import subprocess


class AutoUpdate(UpdateWindow):
    def __init__(self):
        super().__init__()

        self.api_url = "https://api.github.com/repos/tsgamage/Focus-App/releases/latest"
        # self.api_url = "http://localhost:3000/"

        self.save_path = "C:\\Users\\Public\\Downloads\\FocusApp"
        os.makedirs(self.save_path, exist_ok=True)
        self.current_version = "1.0.0"
        self.update_info = {"update_available": False}
        self.installer_path = None


    def get_current_app_info(self):
        with open("data/app_info.json", "r") as app_info_file:
            app_info = json.load(app_info_file)
        self.current_version = app_info["version"]

    def check_for_update(self, current_version):
        try:
            response = requests.get(self.api_url, timeout=5)
        except:
            print(f"Error: Could not connect to GitHub API.")
        else:
            print(f"Connected to GitHub API.")
            if response.status_code == 200:
                latest = response.json()
                latest_version = latest["tag_name"].lstrip("v")

                if latest_version != current_version:
                    self.update_info = {
                        "update_available": True,
                        "name": latest["name"],
                        "version": latest_version,
                        "release_notes": latest.get("body", "No details."),
                        "size": latest["assets"][0]["size"],
                        "url": latest["assets"][0]["browser_download_url"]
                    }

        if self.update_info["update_available"]:
            print("Update available.")
            do_update = messagebox.askyesno("Update Available",
                                            f"A new version v{self.update_info['version']} is available!\nDo you want to download and install it?")

            if do_update:
                self.create_downloading_window()


    def download_update(self,version, url,file_size):
        save_path = self.save_path + f"\\FocusAppSetup_{version}.exe"
        response = requests.get(url, stream=True)
        downloaded_size = 0
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                downloaded_size += len(chunk)
                self.downloaded_progress.set(math.floor(downloaded_size / file_size * 100))
                self.downloaded_progress_text.set(f"{(downloaded_size / 1024) / 1024:.2f} / {(file_size / 1024) / 1024:.2f} MB")
        self.installer_path = os.path.abspath(save_path)
        self.finish_downloading()


    def _start_download(self):
        threading.Thread(target=self.download_update, args=(self.update_info["version"], self.update_info["url"],self.update_info["size"])).start()

    def update_app(self):
        threading.Thread(target=self.check_for_update, args=(self.current_version,)).start()

    def finish_downloading(self):
        self.window.destroy()
        if messagebox.showinfo("Launching Installer", "The app will now close and update."):
            if self.installer_path:
                subprocess.Popen([self.installer_path])