import urllib.request
import json
import os
try:
    import httplib

except ImportError:
    import http.client as httplib


def have_internet():
    conn = httplib.HTTPConnection("www.example.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False


VER_URL = "https://drive.google.com/uc?export=download&id=17KGPTgF6xWKH3dk7Sd74niL548WU6Tts"


def check_update():
    data = {}
    # VER_URL is a shared google drive link that has the current version of stickmanranger
    with urllib.request.urlopen(VER_URL) as response:
        version = response.read().decode()
    # decode the current version from "settings.json"
    current_version = json.JSONDecoder().decode(
        open(os.path.join('config', 'windows_config.json')).read())['version']
    # if the version is the same
    print(current_version, version)

    if current_version == version:
        return False
    return True


def main():
    print(check_update())
    if check_update():
        import run_auto_install


main()
