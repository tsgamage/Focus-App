# Changelog

All notable changes to this project will be documented in this file.  
This project adheres to [Semantic Versioning](https://semver.org/).

---

## [v1.2.0](https://github.com/tsgamage/Focus-App/releases/tag/v1.2.0) - 2025-06-10

### Added
- Auto-update feature: The app now checks for the latest version on startup and provides a prompt to download and install updates.
- Version tracking system using a local version file `app_info.json`, enabling smooth comparison between installed and latest versions.

### Fixed
- Resolved a critical bug where resetting time settings would unintentionally reset all user data.

### Notes
- This version prepares the foundation for seamless background update experiences in future releases.

---

## [v1.1.0](https://github.com/tsgamage/Focus-App/releases/tag/v1.1.0) - 2025-06-08

### Fixed
- Resolved `PermissionError` when saving `user_config.json` to protected directories like `Program Files`.
- Fixed crash when users edited or corrupted the `user_config.json` file manually.

### Added
- Validation and auto-reset logic for settings file integrity.
- Safe fallback location using `%APPDATA%` for storing user settings to avoid permission issues.

### Changed
- Refactored and unified settings update flow into a cleaner `update_user_settings` method.
- Removed unused `user_config.json` related code and logic.

### Removed
- Deprecated usage of settings file in restricted locations.

---

## [v1.0.0](https://github.com/tsgamage/Focus-App/releases/tag/v1.0.0) - 2025-06-07
### Added
- Initial public release of **Focus App** 
- A **clean**, **modern** focus timer, built with **Python** and `ttkbootstrap`
- Core features:
  - Pomodoro timer with configurable intervals
  - Light/Dark mode switch with ttkbootstrap styling
  - Auto and manual cycle switching
  - Progress tab to track daily focus time
  - Saves your settings automatically (using JSON)
  - Clean modular structure
- Installer created using Inno Setup (.exe file)

---


