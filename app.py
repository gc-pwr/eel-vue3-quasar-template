import os
import platform
import sys
import eel
from settings_manager import SettingsManager

settings = SettingsManager()

try:
    import pyi_splash

    splash_available = True

except ImportError:
    splash_available = False


def initialize_app():
    """Initialize application components before showing the UI"""
    if splash_available:
        pyi_splash.update_text("Loading settings...")

    # Load settings
    window_size = settings.get("window_size", (1720, 1080))
    eel.init("web")

    if splash_available:
        pyi_splash.update_text("Preparing user interface...")

    return window_size


@eel.expose
def on_ready():
    if splash_available:
        pyi_splash.close()
    print("Application UI is ready")


@eel.expose
def get_user_settings():
    """Get all current settings for the UI"""
    return settings.get_all()

@eel.expose
def get_setting(setting_name):
    """Get a single setting value by name"""
    return settings.get(
        setting_name,
    )


@eel.expose
def save_user_settings(new_settings):
    """Save user settings from the UI"""
    for key, value in new_settings.items():
        settings.set(key, value)

    # Make sure the directory exists
    os.makedirs(settings.get("output_dir"), exist_ok=True)

    return {"success": True}


@eel.expose
def reset_settings():
    """Reset all settings to default values"""
    settings.reset()
    os.makedirs(settings.get("output_dir"), exist_ok=True)
    return {"success": True}


def main():
    # Initialize app components
    window_size = initialize_app()

    # Update splash screen with final message
    if splash_available:
        pyi_splash.update_text("Starting application...")

    # Start Eel
    try:
        # Check if we're running in a PyInstaller bundle
        is_frozen = getattr(sys, 'frozen', False)

        if is_frozen:
            # If we're in a PyInstaller bundle, use the bundled paths
            base_path = sys._MEIPASS
            # Set environment variable for the Electron process
            os.environ['PYINSTALLER_TEMP_FOLDER'] = base_path

            # Use the known fixed filename for the bundled version
            electron_main = os.path.join(base_path, 'web', 'electron', 'bundle-main.js')

            # Set the path to the Electron executable that we've included in the bundle
            electron_path = os.path.join(base_path, 'electron')
            if platform.system() == 'Windows':
                electron_path = os.path.join(electron_path, 'electron.exe')
            elif platform.system() == 'Darwin':  # macOS
                electron_path = os.path.join(electron_path, 'Electron.app', 'Contents', 'MacOS', 'Electron')
            else:  # Linux
                electron_path = os.path.join(electron_path, 'electron')

            eel.browsers.set_path('electron', electron_path)
        else:
            # In development, use the path from web-src
            electron_main = os.path.join('web-src', 'src', 'electron', 'index.cjs')
            eel.browsers.set_path('electron', 'web-src/node_modules/electron/dist/electron')

        eel.start(
            "",
            mode="electron",
            port=27000,
            block=True,
            size=window_size,
            cmdline_args=[
                '--no-sandbox',
                electron_main
            ]
        )
    except Exception as e:
        # Catch any other exceptions that might occur
        if splash_available:
            pyi_splash.close()
        print(f"Unexpected error: {e}")


# Run the main function
if __name__ == "__main__":
    main()

