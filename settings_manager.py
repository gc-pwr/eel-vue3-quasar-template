import json
import os
import platformdirs
import sys


class SettingsManager:
    """Manages user settings for the application in a PyInstaller-compatible way"""

    def __init__(self, app_name="ElectronApp", default_settings=None):
        """
        Initialize the settings manager

        Args:
            app_name: Name of the application (used for the settings directory)
            default_settings: Dictionary of default settings
        """
        self.app_name = app_name
        self.default_settings = default_settings or {
            "output_dir": os.path.abspath("output"),
            "window_size": (1120, 1130),
        }
        self.settings = {}
        self.settings_file = self._get_settings_path()
        self._load_settings()

    def _get_settings_path(self):
        """Get the path to the settings file, ensuring the directory exists"""
        # Use platformdirs to get the appropriate user data directory based on OS
        # For PyInstaller, we need to handle both development and frozen modes
        if getattr(sys, "frozen", False):
            # We are running in a PyInstaller bundle
            base_dir = platformdirs.user_data_dir(self.app_name, False)
        else:
            # We are running in a normal Python environment
            base_dir = platformdirs.user_data_dir(self.app_name, False)

        # Ensure the directory exists
        os.makedirs(base_dir, exist_ok=True)

        return os.path.join(base_dir, "settings.json")

    def _load_settings(self):
        """Load settings from file, or create with defaults if file doesn't exist"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, "r") as f:
                    loaded_settings = json.load(f)
                    # Merge with defaults to handle new settings in updates
                    self.settings = {**self.default_settings, **loaded_settings}
            else:
                # Start with defaults if no settings file exists
                self.settings = self.default_settings.copy()
                self._save_settings()  # Create the file with defaults
        except Exception as e:
            print(f"Error loading settings: {e}")
            self.settings = self.default_settings.copy()

    def _save_settings(self):
        """Save current settings to file"""
        try:
            with open(self.settings_file, "w") as f:
                json.dump(self.settings, indent=2, sort_keys=True, fp=f)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def get(self, key, default=None):
        """Get a setting value by key"""
        return self.settings.get(key, default)

    def set(self, key, value):
        """Set a setting value and save to disk"""
        self.settings[key] = value
        self._save_settings()

    def get_all(self):
        """Get all settings as a dictionary"""
        return self.settings.copy()

    def reset(self):
        """Reset settings to defaults"""
        self.settings = self.default_settings.copy()
        self._save_settings()