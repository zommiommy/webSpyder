

import time
import json
import random
import requests
from webSpyder.files_function import check_file_existance

def requests_get_page(url,name,settings,logger):
    logger.info("getting with requests %s"%url)

    if settings.is_use_cookies_enabled():
        if check_file_existance(settings.get_cookies_file()) == False:
            logger.error("The cookies file %s for the requests module does not exist."%(settings.get_cookies_file()))
            raise Exception("The cookies file %s for the requests module does not exist."%(settings.get_cookies_file()))

        cookies_dic = json.loads(settings.get_cookies_file())
        cookies = requests.cookies.RequestsCookieJar()
        for name,value in cookies_dic.items():
            cookies.set(name,value)

    if settings.is_use_headers_enabled():
        if check_file_existance(settings.get_headers_file()) == False:
            logger.error("The headers file %s for the requests module does not exist."%(settings.get_headers_file()))
            raise Exception("The headers file %s for the requests module does not exist."%(settings.get_headers_file()))

        headers = json.loads(settings.get_headers_file())


    if settings.is_use_cookies_enabled() == True  and settings.is_use_headers_enabled() == True:
        result = requests.get(url,cookies=cookies,headers=headers)
    elif settings.is_use_cookies_enabled() == False  and settings.is_use_headers_enabled() == True:
        result = requests.get(url,headers=headers)
    elif settings.is_use_cookies_enabled() == True  and settings.is_use_headers_enabled() == False:
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

    if settings.is_random_wait_enabled():
        time.sleep(settings.get_max_wait_sec()*random.random())
