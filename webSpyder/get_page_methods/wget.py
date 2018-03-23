

import os
import json
import time
import subprocess

def wget_get_page(url,name,settings,logger):

    cache_path = settings["cache_path"]

    command = "wget  "

    if settings["random_wait"] == True:
        command += "--random-wait --wait %d "%(settings["max_wait_sec"])


    if settings["use_cookies"] == True:
        with open("%s/%s"%(path,settings["cookies_file"]),"r") as f:
            cookies = f.read()
        command += "--load-cookies %s "%cookies

    if settings["use_headers"] == True:
        with open("%s/%s"%(path,settings["headers_file"]),"r") as f:
            headers = f.read()
        command += "--headers %s "%headers

    if settings["log"] == True:
        command += "--append-output %s/wget.log "%( settings["log_path"])

    command +=  "--output-document %s%s %s"%(cache_path,name,url)
    logger.info("executing : %s"%command)

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    logger.info("process result %s"%process.returncode)
