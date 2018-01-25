import os
import json
import time

from . import __path__ as path

path = path[0]


with open("%s/wget_settings.json"%path,"r") as f:
    settings = json.load(f)

setting_arg = ""

if settings["random_wait"] == True:
    setting_arg += "--random-wait --wait %d "%(settings["max_wait_time"])


if settings["use_cookies"] == True:
    with open("%s/%s"%(path,settings["cookies_file"]),"r") as f:
        cookies = f.read()

    setting_arg += "--load-cookies %s "%cookies

if settings["use_headers"] == True:
    with open("%s/%s"%(path,settings["headers_file"]),"r") as f:
        headers = f.read()

    setting_arg += "--headers %s "%headers

if settings["log"] == True:
    setting_arg += "--append-output %s/%s "%(path,settings["log_file"])


def wget_get_page(url,name,directory):
    # TODO json settings

    command = "wget  "
    command += setting_arg
    command +=  "--output-document %s%s %s"%(directory,name,url)
    print("executing : %s"%command)
    os.system(command)

    # Wait for the wget to finish
    while name not in os.listdir(directory):
        time.sleep(0.3)