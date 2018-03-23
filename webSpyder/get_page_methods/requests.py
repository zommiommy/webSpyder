

import time
import json
import random
import requests
from webSpyder.files_function import check_file_existance

def requests_get_page(url,name,settings,logger):
    logger.info("getting with requests %s"%url)

    if settings["use_cookies"] == True:
        if check_file_existance(settings["cookies_file"]) == False:
            logger.error("The cookies file %s for the requests module does not exist."%(settings["cookies_file"]))
            raise Exception("The cookies file %s for the requests module does not exist."%(settings["cookies_file"]))

        cookies_dic = json.loads(settings["cookies_file"])
        cookies = requests.cookies.RequestsCookieJar()
        for name,value in cookies_dic.items():
            cookies.set(name,value)

    if settings["use_headers"] == True:
        if check_file_existance(settings["headers_file"]) == False:
            logger.error("The headers file %s for the requests module does not exist."%(settings["headers_file"]))
            raise Exception("The headers file %s for the requests module does not exist."%(settings["headers_file"]))

        headers = json.loads(settings["headers_file"])


    if settings["use_cookies"] == True  and settings["use_headers"] == True:
        result = requests.get(url,cookies=cookies,headers=headers)
    elif settings["use_cookies"] == False  and settings["use_headers"] == True:
        result = requests.get(url,headers=headers)
    elif settings["use_cookies"] == True  and settings["use_headers"] == False:
        result = requests.get(url,cookies=cookies)
    else:
        result = requests.get(url)

    error_code = result.status_code

    if error_code == 200 or error_code == 304:
        logger.info("Success %s error code, writing %s"%(error_code,name))
        with open(name,"w") as f:
            f.write(result.text)
    else:
        logger.error("requests error code %s for url %s"%(error_code,url))
        raise Exception("requests error code %s for url %s"%(error_code,url))
        
    if settings["random_wait"]:
        time.sleep(settings["max_wait_sec"]*random.random())
