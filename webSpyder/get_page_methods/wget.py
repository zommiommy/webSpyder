

import os
import json
import time
import subprocess

def wget_get_page(url,name,settings,logger):

    cache_path = settings.get_cache_path()

    command = "wget  "

    if settings.is_random_wait_enabled():
        command += "--random-wait --wait %d "%(settings.get_max_wait_sec())


    if settings.is_use_cookies_enabled() == True:
        with open("%s/%s"%(path,settings.get_cookies_file()),"r") as f:
            cookies = f.read()
        command += "--load-cookies %s "%cookies

    if settings.is_use_headers_enabled():
        with open("%s/%s"%(path,settings.get_headers_file()),"r") as f:
            headers = f.read()
        command += "--headers %s "%headers

    if settings.is_log_enabled():
        command += "--append-output %s/wget.log "%( settings.get_log_path())

    command +=  "--output-document %s%s %s"%(cache_path,name,url)
    logger.info("executing : %s"%command)

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    logger.info("process result %s"%process.returncode)
