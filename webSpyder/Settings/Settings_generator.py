
import os

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

bool_func_pattern = '\tdef async_enable_{value}(self):\n\t\tself.settings["{value}"] = True\n\tdef async_disable_{value}(self):\n\t\tself.settings["{value}"] = False\n\tdef async_is_{value}_enabled(self):\n\t\treturn self.settings["{value}"] == True\n'
list_func_pattern = '\tdef async_get_{value}(self):\n\t\treturn self.settings["{value}"]\n\tdef async_add_{value}(self,tags):\n\t\tself.settings["{value}"] += tags\n\t\tself.enable_clear_html()\n\tdef async_set_{value}(self,tags):\n\t\tself.settings["{value}"] = tags\n\t\tself.enable_clear_html()\n'
else_func_pattern ='\tdef async_set_{value}(self,value):\n\t\tself.settings["{value}"] = value\n\tdef async_get_{value}(self):\n\t\treturn self.settings["{value}"]\n'

sync_bool_func_pattern = '\tdef enable_{value}(self):\n\t\tself.{value}_lock.acquire()\n\t\tself.settings["{value}"] = True\n\t\tself.{value}_lock.release()\n\tdef disable_{value}(self):\n\t\tself.{value}_lock.acquire()\n\t\tself.settings["{value}"] = False\n\t\tself.{value}_lock.release()\n\tdef is_{value}_enabled(self):\n\t\tself.{value}_lock.acquire()\n\t\tvalue = self.settings["{value}"] == True\n\t\tself.{value}_lock.release()\n\t\treturn value\n'
sync_list_func_pattern = '\tdef get_{value}(self):\n\t\tself.{value}_lock.acquire()\n\t\tvalue = self.settings["{value}"]\n\t\tself.{value}_lock.release()\n\t\treturn value\n\tdef add_{value}(self,tags):\n\t\tself.{value}_lock.acquire()\n\t\tself.settings["{value}"] += tags\n\t\tself.enable_clear_html()\n\tdef set_{value}(self,tags):\n\t\tself.{value}_lock.acquire()\n\t\tself.settings["{value}"] = tags\n\t\tself.enable_clear_html()\n\t\tself.{value}_lock.release()\n'
sync_else_func_pattern ='\tdef set_{value}(self,value):\n\t\tself.{value}_lock.acquire()\n\t\tself.settings["{value}"] = value\n\t\tself.{value}_lock.release()\n\tdef get_{value}(self):\n\t\tself.{value}_lock.acquire()\n\t\tvalue =  self.settings["{value}"]\n\t\tself.{value}_lock.release()\n\t\treturn value\n'

stringa = ""
stringa += "\n\n\nfrom multiprocessing import Lock\nimport os\nimport json\n\n"
stringa += "class Settings():\n"

stringa += '\tdef __str__(self):\n\t\treturn json.dumps(self.settings, indent=4)\n\tdef __rep__(self):\n\t\treturn self.__str__()\n\tdef __getitem__(self,name):\n\t\treturn self.settings[name]\n\tdef __setitem__(self,name,value):\n\t\tself.settings[name] = value\n'
stringa += "\tdef __init__(self):"
for key in settings.keys():
    stringa += "\n\t\tself.{value}_lock = Lock()".format(value=key)
stringa += "\n\n#" + "-"*64 + "\n"
stringa += "# Async Module" + "\n"
stringa += "#" + "-"*64 + "\n"
for key,value in settings.items():
    stringa += "\n"
    if type(value) == type(True):
        stringa += bool_func_pattern.format(value=key)
    elif type(value) == type([]):
        stringa += list_func_pattern.format(value=key)
    else:
        stringa += else_func_pattern.format(value=key)

stringa += "#" + "-"*64 + "\n"
stringa += "# Sync Module" + "\n"
stringa += "#" + "-"*64 + "\n"
for key,value in settings.items():
    stringa += "\n"
    if type(value) == type(True):
        stringa += sync_bool_func_pattern.format(value=key)
    elif type(value) == type([]):
        stringa += sync_list_func_pattern.format(value=key)
    else:
        stringa += sync_else_func_pattern.format(value=key)




print(stringa)
with open("generated_settings.py","a"):
    pass

with open("generated_settings.py","w") as f:
    f.write(stringa)
