

class Settings():

    settings = {
        "identifier":"0",
        "data_type":"webList",
        "mode":"wget",
        "permessive_exception":True,
        "start_url":"",
        "project":"webSpyder",

        "clear_html":False,
        "clear_comments":True,
        "useless_tags":["svg","input","noscript","link","script","style","iframe","canvas"],
        "useless_attributes":["style", "href", "role", "src","target","type","lang","async","crossorigin"],

        "skip_estensions":True,
        "not_skip_estensions_list":["html","htm","php","aspx","asp","axd","asx","asmx","ashx","cfm","xml","rss","cgi","jsp","jspx",],

        "state_path":"%s/state/"%os.getcwd(),

        "cache":False,
        "cache_path":"%s/pagecaches/"%os.getcwd(),

        "log": True,
        "log_path":"%s/log/"%os.getcwd(),
        "log_format": '%(asctime)s - %(name)s - %(levelname)s - %(message)s',

        "random_wait": True,
        "max_wait_sec": 5,
        "use_cookies": False,
        "cookies_file":"cookies.json",
        "use_headers": False,
        "headers_file": "headers.json",

        "tqdm_run":True
    }

     def __init__(self):
         pass

     def __str__(self):
         return json.dumps(self.settings, indent=4)
#---------------------------------------------------------------------------
# Modifiers and Observers
#---------------------------------------------------------------------------

    # Boolean
    def enable_permessive_exception(self):
        self.settings["permessive_exception"] = True
    def disable_permessive_exception(self):
        self.settings["permessive_exception"] = False
    def disable_permessive_exception_enabled(self):
        return self.settings["permessive_exception"] == True

    def enable_clear_html(self):
        self.settings["clear_html"] = True
    def disable_clear_html(self):
        self.settings["clear_html"] = False
    def disable_clear_html_enabled(self):
        return self.settings["clear_html"] == True

    def enable_clear_comments(self):
        self.settings["clear_comments"] = True
    def disable_clear_comments(self):
        self.settings["clear_comments"] = False
    def is_clear_comments_enabled(self):
        return self.settings["clear_comments"] == True

    def enable_skip_estensions(self):
        self.settings["skip_estensions"] = True
    def disable_skip_estensions(self):
        self.settings["skip_estensions"] = False
    def is_skip_estensions_enabled(self):
        return self.settings["skip_estensions"] == True

    def enable_cache(self):
        self.settings["cache"] = True
    def disable_cache(self):
        self.settings["cache"] = False
    def is_cache_enabled(self):
        return self.settings["cache"] == True

    def enable_log(self):
        self.settings["log"] = True
    def disable_log(self):
        self.settings["log"] = False
    def is_log_enabled(self):
        return self.settings["log"] == True

    def enable_random_wait(self):
        self.settings["random_wait"] = True
    def disable_random_wait(self):
        self.settings["random_wait"] = False
    def is_random_wait_enabled(self):
        return self.settings["random_wait"] == True

    def enable_use_cookies(self):
        self.settings["use_cookies"] = True
    def disable_use_cookies(self):
        self.settings["use_cookies"] = False
    def is_use_cookies_enabled(self):
        return self.settings["use_cookies"] == True

    def enable_use_headers(self):
        self.settings["use_headers"] = True
    def disable_use_headers(self):
        self.settings["use_headers"] = False
    def is_use_headers_enabled(self):
        return self.settings["use_headers"] == True

    def enable_tqdm_run(self):
        self.settings["tqdm_run"] = True
    def disable_tqdm_run(self):
        self.settings["tqdm_run"] = False
    def is_tqdm_run_enabled(self):
        return self.settings["tqdm_run"] == True
#---------------------------------------------------------------------------
# Incrementing list
#---------------------------------------------------------------------------

    def get_useless_attributes(self):
        return self.settings["useless_attributes"]

    def add_useless_attributes(self,attributes):
        self.settings["useless_attributes"] += attributes
        self.enable_clear_html()

    def set_useless_attributes(self,attributes):
        self.settings["useless_attributes"] = attributes
        self.enable_clear_html()

    def get_useless_tags(self):
        return self.settings["useless_tags"]

    def add_useless_tags(self,tags):
        self.settings["useless_tags"] += tags
        self.enable_clear_html()

    def set_useless_tags(self,tags):
        self.settings["useless_tags"] = tags
        self.enable_clear_html()


#---------------------------------------------------------------------------
# Not Boolean
#---------------------------------------------------------------------------
    def set_identifier(self,value):
        self.settings["identifier"] = value
    def get_identifier(self):
        return self.settings["identifier"]

    def set_data_type(self,value):
        self.settings["data_type"] = value
    def get_data_type(self):
        return self.settings["data_type"]

    def set_mode(self,value):
        self.settings["mode"] = value
    def get_mode(self):
        return self.settings["mode"]

    def set_start_url(self,value):
        self.settings["start_url"] = value
    def get_start_url(self):
        return self.settings["start_url"]

    def set_project(self,value):
        self.settings["project"] = value
    def get_project(self):
        return self.settings["project"]

    def set_state_path(self,value):
        self.settings["state_path"] = value
    def get_state_path(self):
        return self.settings["state_path"]

    def set_cache_path(self,value):
        self.settings["cache_path"] = value
    def get_cache_path(self):
        return self.settings["cache_path"]

    def set_log_path(self,value):
        self.settings["log_path"] = value
    def get_log_path(self):
        return self.settings["log_path"]

    def set_log_format(self,value):
        self.settings["log_format"] = value
    def get_log_format(self):
        return self.settings["log_format"]

    def set_not_skip_estensions_list(self,value):
        self.settings["not_skip_estensions_list"] = value
    def get_not_skip_estensions_list(self):
        return self.settings["not_skip_estensions_list"]

    def set_max_wait_sec(self,value):
        self.settings["max_wait_sec"] = value
    def get_max_wait_sec(self):
        return self.settings["max_wait_sec"]

    def set_cookies_file(self,value):
        self.settings["cookies_file"] = value
    def get_cookies_file(self):
        return self.settings["cookies_file"]

    def set_headers_file(self,value):
        self.settings["headers_file"] = value
    def get_headers_file(self):
        return self.settings["headers_file"]
