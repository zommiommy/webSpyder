


from multiprocessing import Lock
import os
import json

class Settings():
	settings = {
	    "identifier":"0",
	    "data_type":"webList",
	    "mode":"wget",
	    "permessive_exception":True,
	    "project":"webSpyder",

	    "clear_html":False,
	    "clear_comments":True,
	    "useless_tags":["svg","input","noscript","link","script","style","iframe","canvas"],
	    "useless_attributes":["style", "href", "role", "src","target","type","lang","async","crossorigin"],

	    "skip_estensions":True,
	    "not_skip_estensions_list":["html","htm","php","aspx","asp","axd","asx","asmx","ashx","cfm","xml","rss","cgi","jsp","jspx"],

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

	    "tqdm_run":True,

	    "multithreading":True,
	    "n_of_workers":8
	    }
	def __str__(self):
		return json.dumps(self.settings, indent=4)
	def __rep__(self):
		return self.__str__()
	def __getitem__(self,name):
		return self.settings[name]
	def __setitem__(self,name,value):
		self.settings[name] = value
	def __init__(self):
		self.identifier_lock = Lock()
		self.data_type_lock = Lock()
		self.mode_lock = Lock()
		self.permessive_exception_lock = Lock()
		self.project_lock = Lock()
		self.clear_html_lock = Lock()
		self.clear_comments_lock = Lock()
		self.useless_tags_lock = Lock()
		self.useless_attributes_lock = Lock()
		self.skip_estensions_lock = Lock()
		self.not_skip_estensions_list_lock = Lock()
		self.state_path_lock = Lock()
		self.cache_lock = Lock()
		self.cache_path_lock = Lock()
		self.log_lock = Lock()
		self.log_path_lock = Lock()
		self.log_format_lock = Lock()
		self.random_wait_lock = Lock()
		self.max_wait_sec_lock = Lock()
		self.use_cookies_lock = Lock()
		self.cookies_file_lock = Lock()
		self.use_headers_lock = Lock()
		self.headers_file_lock = Lock()
		self.tqdm_run_lock = Lock()
		self.multithreading_lock = Lock()
		self.n_of_workers_lock = Lock()

#----------------------------------------------------------------
# Async Module
#----------------------------------------------------------------

	def async_set_identifier(self,value):
		self.settings["identifier"] = value
	def async_get_identifier(self):
		return self.settings["identifier"]

	def async_set_data_type(self,value):
		self.settings["data_type"] = value
	def async_get_data_type(self):
		return self.settings["data_type"]

	def async_set_mode(self,value):
		self.settings["mode"] = value
	def async_get_mode(self):
		return self.settings["mode"]

	def async_enable_permessive_exception(self):
		self.settings["permessive_exception"] = True
	def async_disable_permessive_exception(self):
		self.settings["permessive_exception"] = False
	def async_is_permessive_exception_enabled(self):
		return self.settings["permessive_exception"] == True

	def async_set_project(self,value):
		self.settings["project"] = value
	def async_get_project(self):
		return self.settings["project"]

	def async_enable_clear_html(self):
		self.settings["clear_html"] = True
	def async_disable_clear_html(self):
		self.settings["clear_html"] = False
	def async_is_clear_html_enabled(self):
		return self.settings["clear_html"] == True

	def async_enable_clear_comments(self):
		self.settings["clear_comments"] = True
	def async_disable_clear_comments(self):
		self.settings["clear_comments"] = False
	def async_is_clear_comments_enabled(self):
		return self.settings["clear_comments"] == True

	def async_get_useless_tags(self):
		return self.settings["useless_tags"]
	def async_add_useless_tags(self,tags):
		self.settings["useless_tags"] += tags
		self.enable_clear_html()
	def async_set_useless_tags(self,tags):
		self.settings["useless_tags"] = tags
		self.enable_clear_html()

	def async_get_useless_attributes(self):
		return self.settings["useless_attributes"]
	def async_add_useless_attributes(self,tags):
		self.settings["useless_attributes"] += tags
		self.enable_clear_html()
	def async_set_useless_attributes(self,tags):
		self.settings["useless_attributes"] = tags
		self.enable_clear_html()

	def async_enable_skip_estensions(self):
		self.settings["skip_estensions"] = True
	def async_disable_skip_estensions(self):
		self.settings["skip_estensions"] = False
	def async_is_skip_estensions_enabled(self):
		return self.settings["skip_estensions"] == True

	def async_get_not_skip_estensions_list(self):
		return self.settings["not_skip_estensions_list"]
	def async_add_not_skip_estensions_list(self,tags):
		self.settings["not_skip_estensions_list"] += tags
		self.enable_clear_html()
	def async_set_not_skip_estensions_list(self,tags):
		self.settings["not_skip_estensions_list"] = tags
		self.enable_clear_html()

	def async_set_state_path(self,value):
		self.settings["state_path"] = value
	def async_get_state_path(self):
		return self.settings["state_path"]

	def async_enable_cache(self):
		self.settings["cache"] = True
	def async_disable_cache(self):
		self.settings["cache"] = False
	def async_is_cache_enabled(self):
		return self.settings["cache"] == True

	def async_set_cache_path(self,value):
		self.settings["cache_path"] = value
	def async_get_cache_path(self):
		return self.settings["cache_path"]

	def async_enable_log(self):
		self.settings["log"] = True
	def async_disable_log(self):
		self.settings["log"] = False
	def async_is_log_enabled(self):
		return self.settings["log"] == True

	def async_set_log_path(self,value):
		self.settings["log_path"] = value
	def async_get_log_path(self):
		return self.settings["log_path"]

	def async_set_log_format(self,value):
		self.settings["log_format"] = value
	def async_get_log_format(self):
		return self.settings["log_format"]

	def async_enable_random_wait(self):
		self.settings["random_wait"] = True
	def async_disable_random_wait(self):
		self.settings["random_wait"] = False
	def async_is_random_wait_enabled(self):
		return self.settings["random_wait"] == True

	def async_set_max_wait_sec(self,value):
		self.settings["max_wait_sec"] = value
	def async_get_max_wait_sec(self):
		return self.settings["max_wait_sec"]

	def async_enable_use_cookies(self):
		self.settings["use_cookies"] = True
	def async_disable_use_cookies(self):
		self.settings["use_cookies"] = False
	def async_is_use_cookies_enabled(self):
		return self.settings["use_cookies"] == True

	def async_set_cookies_file(self,value):
		self.settings["cookies_file"] = value
	def async_get_cookies_file(self):
		return self.settings["cookies_file"]

	def async_enable_use_headers(self):
		self.settings["use_headers"] = True
	def async_disable_use_headers(self):
		self.settings["use_headers"] = False
	def async_is_use_headers_enabled(self):
		return self.settings["use_headers"] == True

	def async_set_headers_file(self,value):
		self.settings["headers_file"] = value
	def async_get_headers_file(self):
		return self.settings["headers_file"]

	def async_enable_tqdm_run(self):
		self.settings["tqdm_run"] = True
	def async_disable_tqdm_run(self):
		self.settings["tqdm_run"] = False
	def async_is_tqdm_run_enabled(self):
		return self.settings["tqdm_run"] == True

	def async_enable_multithreading(self):
		self.settings["multithreading"] = True
	def async_disable_multithreading(self):
		self.settings["multithreading"] = False
	def async_is_multithreading_enabled(self):
		return self.settings["multithreading"] == True

	def async_set_n_of_workers(self,value):
		self.settings["n_of_workers"] = value
	def async_get_n_of_workers(self):
		return self.settings["n_of_workers"]
#----------------------------------------------------------------
# Sync Module
#----------------------------------------------------------------

	def set_identifier(self,value):
		self.identifier_lock.acquire()
		self.settings["identifier"] = value
		self.identifier_lock.release()
	def get_identifier(self):
		self.identifier_lock.acquire()
		value =  self.settings["identifier"]
		self.identifier_lock.release()
		return value

	def set_data_type(self,value):
		self.data_type_lock.acquire()
		self.settings["data_type"] = value
		self.data_type_lock.release()
	def get_data_type(self):
		self.data_type_lock.acquire()
		value =  self.settings["data_type"]
		self.data_type_lock.release()
		return value

	def set_mode(self,value):
		self.mode_lock.acquire()
		self.settings["mode"] = value
		self.mode_lock.release()
	def get_mode(self):
		self.mode_lock.acquire()
		value =  self.settings["mode"]
		self.mode_lock.release()
		return value

	def enable_permessive_exception(self):
		self.permessive_exception_lock.acquire()
		self.settings["permessive_exception"] = True
		self.permessive_exception_lock.release()
	def disable_permessive_exception(self):
		self.permessive_exception_lock.acquire()
		self.settings["permessive_exception"] = False
		self.permessive_exception_lock.release()
	def is_permessive_exception_enabled(self):
		self.permessive_exception_lock.acquire()
		value = self.settings["permessive_exception"] == True
		self.permessive_exception_lock.release()
		return value

	def set_project(self,value):
		self.project_lock.acquire()
		self.settings["project"] = value
		self.project_lock.release()
	def get_project(self):
		self.project_lock.acquire()
		value =  self.settings["project"]
		self.project_lock.release()
		return value

	def enable_clear_html(self):
		self.clear_html_lock.acquire()
		self.settings["clear_html"] = True
		self.clear_html_lock.release()
	def disable_clear_html(self):
		self.clear_html_lock.acquire()
		self.settings["clear_html"] = False
		self.clear_html_lock.release()
	def is_clear_html_enabled(self):
		self.clear_html_lock.acquire()
		value = self.settings["clear_html"] == True
		self.clear_html_lock.release()
		return value

	def enable_clear_comments(self):
		self.clear_comments_lock.acquire()
		self.settings["clear_comments"] = True
		self.clear_comments_lock.release()
	def disable_clear_comments(self):
		self.clear_comments_lock.acquire()
		self.settings["clear_comments"] = False
		self.clear_comments_lock.release()
	def is_clear_comments_enabled(self):
		self.clear_comments_lock.acquire()
		value = self.settings["clear_comments"] == True
		self.clear_comments_lock.release()
		return value

	def get_useless_tags(self):
		self.useless_tags_lock.acquire()
		value = self.settings["useless_tags"]
		self.useless_tags_lock.release()
		return value
	def add_useless_tags(self,tags):
		self.useless_tags_lock.acquire()
		self.settings["useless_tags"] += tags
		self.enable_clear_html()
	def set_useless_tags(self,tags):
		self.useless_tags_lock.acquire()
		self.settings["useless_tags"] = tags
		self.enable_clear_html()
		self.useless_tags_lock.release()

	def get_useless_attributes(self):
		self.useless_attributes_lock.acquire()
		value = self.settings["useless_attributes"]
		self.useless_attributes_lock.release()
		return value
	def add_useless_attributes(self,tags):
		self.useless_attributes_lock.acquire()
		self.settings["useless_attributes"] += tags
		self.enable_clear_html()
	def set_useless_attributes(self,tags):
		self.useless_attributes_lock.acquire()
		self.settings["useless_attributes"] = tags
		self.enable_clear_html()
		self.useless_attributes_lock.release()

	def enable_skip_estensions(self):
		self.skip_estensions_lock.acquire()
		self.settings["skip_estensions"] = True
		self.skip_estensions_lock.release()
	def disable_skip_estensions(self):
		self.skip_estensions_lock.acquire()
		self.settings["skip_estensions"] = False
		self.skip_estensions_lock.release()
	def is_skip_estensions_enabled(self):
		self.skip_estensions_lock.acquire()
		value = self.settings["skip_estensions"] == True
		self.skip_estensions_lock.release()
		return value

	def get_not_skip_estensions_list(self):
		self.not_skip_estensions_list_lock.acquire()
		value = self.settings["not_skip_estensions_list"]
		self.not_skip_estensions_list_lock.release()
		return value
	def add_not_skip_estensions_list(self,tags):
		self.not_skip_estensions_list_lock.acquire()
		self.settings["not_skip_estensions_list"] += tags
		self.enable_clear_html()
	def set_not_skip_estensions_list(self,tags):
		self.not_skip_estensions_list_lock.acquire()
		self.settings["not_skip_estensions_list"] = tags
		self.enable_clear_html()
		self.not_skip_estensions_list_lock.release()

	def set_state_path(self,value):
		self.state_path_lock.acquire()
		self.settings["state_path"] = value
		self.state_path_lock.release()
	def get_state_path(self):
		self.state_path_lock.acquire()
		value =  self.settings["state_path"]
		self.state_path_lock.release()
		return value

	def enable_cache(self):
		self.cache_lock.acquire()
		self.settings["cache"] = True
		self.cache_lock.release()
	def disable_cache(self):
		self.cache_lock.acquire()
		self.settings["cache"] = False
		self.cache_lock.release()
	def is_cache_enabled(self):
		self.cache_lock.acquire()
		value = self.settings["cache"] == True
		self.cache_lock.release()
		return value

	def set_cache_path(self,value):
		self.cache_path_lock.acquire()
		self.settings["cache_path"] = value
		self.cache_path_lock.release()
	def get_cache_path(self):
		self.cache_path_lock.acquire()
		value =  self.settings["cache_path"]
		self.cache_path_lock.release()
		return value

	def enable_log(self):
		self.log_lock.acquire()
		self.settings["log"] = True
		self.log_lock.release()
	def disable_log(self):
		self.log_lock.acquire()
		self.settings["log"] = False
		self.log_lock.release()
	def is_log_enabled(self):
		self.log_lock.acquire()
		value = self.settings["log"] == True
		self.log_lock.release()
		return value

	def set_log_path(self,value):
		self.log_path_lock.acquire()
		self.settings["log_path"] = value
		self.log_path_lock.release()
	def get_log_path(self):
		self.log_path_lock.acquire()
		value =  self.settings["log_path"]
		self.log_path_lock.release()
		return value

	def set_log_format(self,value):
		self.log_format_lock.acquire()
		self.settings["log_format"] = value
		self.log_format_lock.release()
	def get_log_format(self):
		self.log_format_lock.acquire()
		value =  self.settings["log_format"]
		self.log_format_lock.release()
		return value

	def enable_random_wait(self):
		self.random_wait_lock.acquire()
		self.settings["random_wait"] = True
		self.random_wait_lock.release()
	def disable_random_wait(self):
		self.random_wait_lock.acquire()
		self.settings["random_wait"] = False
		self.random_wait_lock.release()
	def is_random_wait_enabled(self):
		self.random_wait_lock.acquire()
		value = self.settings["random_wait"] == True
		self.random_wait_lock.release()
		return value

	def set_max_wait_sec(self,value):
		self.max_wait_sec_lock.acquire()
		self.settings["max_wait_sec"] = value
		self.max_wait_sec_lock.release()
	def get_max_wait_sec(self):
		self.max_wait_sec_lock.acquire()
		value =  self.settings["max_wait_sec"]
		self.max_wait_sec_lock.release()
		return value

	def enable_use_cookies(self):
		self.use_cookies_lock.acquire()
		self.settings["use_cookies"] = True
		self.use_cookies_lock.release()
	def disable_use_cookies(self):
		self.use_cookies_lock.acquire()
		self.settings["use_cookies"] = False
		self.use_cookies_lock.release()
	def is_use_cookies_enabled(self):
		self.use_cookies_lock.acquire()
		value = self.settings["use_cookies"] == True
		self.use_cookies_lock.release()
		return value

	def set_cookies_file(self,value):
		self.cookies_file_lock.acquire()
		self.settings["cookies_file"] = value
		self.cookies_file_lock.release()
	def get_cookies_file(self):
		self.cookies_file_lock.acquire()
		value =  self.settings["cookies_file"]
		self.cookies_file_lock.release()
		return value

	def enable_use_headers(self):
		self.use_headers_lock.acquire()
		self.settings["use_headers"] = True
		self.use_headers_lock.release()
	def disable_use_headers(self):
		self.use_headers_lock.acquire()
		self.settings["use_headers"] = False
		self.use_headers_lock.release()
	def is_use_headers_enabled(self):
		self.use_headers_lock.acquire()
		value = self.settings["use_headers"] == True
		self.use_headers_lock.release()
		return value

	def set_headers_file(self,value):
		self.headers_file_lock.acquire()
		self.settings["headers_file"] = value
		self.headers_file_lock.release()
	def get_headers_file(self):
		self.headers_file_lock.acquire()
		value =  self.settings["headers_file"]
		self.headers_file_lock.release()
		return value

	def enable_tqdm_run(self):
		self.tqdm_run_lock.acquire()
		self.settings["tqdm_run"] = True
		self.tqdm_run_lock.release()
	def disable_tqdm_run(self):
		self.tqdm_run_lock.acquire()
		self.settings["tqdm_run"] = False
		self.tqdm_run_lock.release()
	def is_tqdm_run_enabled(self):
		self.tqdm_run_lock.acquire()
		value = self.settings["tqdm_run"] == True
		self.tqdm_run_lock.release()
		return value

	def enable_multithreading(self):
		self.multithreading_lock.acquire()
		self.settings["multithreading"] = True
		self.multithreading_lock.release()
	def disable_multithreading(self):
		self.multithreading_lock.acquire()
		self.settings["multithreading"] = False
		self.multithreading_lock.release()
	def is_multithreading_enabled(self):
		self.multithreading_lock.acquire()
		value = self.settings["multithreading"] == True
		self.multithreading_lock.release()
		return value

	def set_n_of_workers(self,value):
		self.n_of_workers_lock.acquire()
		self.settings["n_of_workers"] = value
		self.n_of_workers_lock.release()
	def get_n_of_workers(self):
		self.n_of_workers_lock.acquire()
		value =  self.settings["n_of_workers"]
		self.n_of_workers_lock.release()
		return value
