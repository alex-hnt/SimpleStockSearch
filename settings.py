import sys
from os import path
from json import (load as jsonload, dump as jsondump)
import keyboard

SETTINGS_FILE = path.join(path.dirname(sys.executable), r'config.cfg')

SITE_KEYS = [
    'TRADINGVIEW',
    'TWITTER',
    'YAHOOFINANCE',
    'MARKETWATCH',
    'SEEKINGALPHA',
    'STOCKCHARTS',
    'OPENINSIDER',
    'FINVIZ',
    'ROBINHOOD'
]

DEFAULT_SETTINGS = {
    'theme': '',
    'hotkey': 'shift+alt+h',
    'enabled_sites_keys': ['TRADINGVIEW', 'TWITTER', 'YAHOOFINANCE']
}

# load_settings: Reads the settings file, sets the contents equal to the
# 'settings' variable, and returns it.
def load_settings(settings_file, default_settings):
    try:
        with open(settings_file, 'r') as f:
            settings = jsonload(f)
    # If the settings file cannot be found, creates one with default settings.
    except Exception as e:
        settings = default_settings
        save_settings(settings_file, settings, None)
    return settings

def save_settings(settings_file, settings, checked_indices):
    if checked_indices:
        for i in range(0, len(SITE_KEYS)):
            key = SITE_KEYS[i]
            if i in checked_indices:
                if key not in settings["enabled_sites_keys"]:
                    settings["enabled_sites_keys"].append(key)
            else:
                if key in settings["enabled_sites_keys"]:
                    settings["enabled_sites_keys"].remove(key)

    with open(settings_file, 'w') as f:
        jsondump(settings, f)