import sys
from os import path
from json import (load as jsonload, dump as jsondump)
import keyboard

SETTINGS_FILE = path.join(path.dirname(sys.executable), r'config.cfg')

SITES = {
    "TRADINGVIEW": f"https://www.tradingview.com/chart/?symbol={{symbol}}",
    "TWITTER": f"https://twitter.com/search?q=%24{{symbol}}",
    "YAHOOFINANCE": f"https://finance.yahoo.com/quote/{{symbol}}",
    "MARKETWATCH": f"https://www.marketwatch.com/investing/stock/{{symbol}}",
    "SEEKINGALPHA": f"https://seekingalpha.com/symbol/{{symbol}}",
    "STOCKCHARTS": f"https://stockcharts.com/sc3/ui/?s={{symbol}}",
    "OPENINSIDER": f"http://openinsider.com/{{symbol}}",
    "FINVIZ": f"https://finviz.com/quote.ashx?t={{symbol}}",
    "ROBINHOOD": f"https://robinhood.com/stocks/{{symbol}}",
}

DEFAULT_SETTINGS = {
    'theme': 'default_dark',
    'hotkey': 'shift+alt+h',
    'enabled_sites_keys': ['TRADINGVIEW', 'TWITTER', 'YAHOOFINANCE']
}

def load_settings(settings_file, default_settings):
    try:
        with open(settings_file, 'r') as f:
            settings = jsonload(f)
    except Exception as e:
        settings = default_settings
        save_settings(settings_file, settings, None)
    return settings

def save_settings(settings_file, settings, checked_indices):
    if checked_indices:
        for i, (key) in enumerate(SITES):
            if i in checked_indices:
                if key not in settings["enabled_sites_keys"]:
                    settings["enabled_sites_keys"].append(key)
            else:
                if key in settings["enabled_sites_keys"]:
                    settings["enabled_sites_keys"].remove(key)

    with open(settings_file, 'w') as f:
        jsondump(settings, f)