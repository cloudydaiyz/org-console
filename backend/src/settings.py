import json
import os

CWD = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = CWD + "/../config/settings.json"

settings = None
range_settings = None
gid_settings = None

with open(SETTINGS_PATH, "r") as settings_file:
    settings = json.load(settings_file)
    range_settings = settings["ranges"]
    gid_settings = settings["google_ids"]

if __name__ == "__main__":
    # print(os.path.isfile(SETTINGS_PATH))
    print(settings)
    print(range_settings)
    print(gid_settings)