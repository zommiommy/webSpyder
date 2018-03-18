
# coding: utf-8

# # webSpyder
# A little class for making the spyder job easier, it's in a really early point of development but it should work

# # An example:
# A spyder that search wikipedia for page about food

# Import the package

# In[1]:


import webSpyder


# Create an istance of the spyder

# In[2]:


s = webSpyder.Spyder("wikipediaSpyder")


# Add the url of the page from which the spyder will start

# In[3]:


s.set_start_url("https://it.wikipedia.org/wiki/Pagina_principale")


# Create your custom function which decide if the current url have to be parsed or not.
#
# You can add as many function as you wish.
#
# The Spyder take the and of all the filter functions, so all of them have to return True so that the url is parsed.

# In[4]:


def my_filter(url):
    return "wikipedia" in url


# In[5]:


s.set_filter(my_filter)


# Create your custom function which recive the soup (bs4 parse html) and the url of the current page.
#
# You can add as many function as you wish.
#
# Each function is called on every page the spyder decide to download and parse.

# In[6]:


def test_function(soup,url):
    print("hi the url is %s"%url)


# In[7]:


s.set_function(test_function)


# The current state of the spyder is printable

# In[8]:


print(s)


# if there aren't already there create the folder for the logs and the caches

# In[9]:


s.create_needed_folders()


# It can do a single url at time.

# In[10]:


s.iteration()


# Or it can do a n of iteration or if it not passed any value it will go on parsing urls that it find in the pages until there aren't anyone left

# In[11]:


s.run(10)
# or s.run() to go on indefinitivly


# It can be stopped throwing a KeyboardInerrupt pressing Ctrl-C

# # Complete code

# In[12]:


import webSpyder

s = webSpyder.Spyder("wikipediaSpyder")

s.set_start_url("https://it.wikipedia.org/")

def my_filter(url):
    return "wikipedia" in url
s.set_filter(my_filter)

def test_function(soup,url):
    print("hi the url is %s\nand the html is %s"%(url,soup))
s.set_function(test_function)

s.create_needed_folders()

s.run(10)


# # Settings

# * `mode`: choose the wey the page will be downloaded, the default way is by wget with the value "wget". For now there is only wget but in the future it will support ["wget","urllib","selenium","requests"] librarys.
# * `permessive_exception`: if permessive_exception is True then if there is an exception in the parsing of the page the spyder will just ignore that page. Else if it is false the spyder will throw the exception.
# * `start_url`: is the url from which the spyder will start
# * `project`: name of the spyder, it's the name of the default logfile and it can be usefull in mulithreading situations.

# ### Logs

# *  `enable_log()`: enable the logging
# *  `disable_log()`: disable the logging
# *  `set_log_path(path)`: sets the absolute path of the log file ex. "C:\log.log"
# *  `set_log_format("format")`: sets the format of the log (same syntax of the logging module format)

# ## Cache

# *  `enable_cache()`: enable the caching of the pages
# *  `disable_cache()`: disable the caching of the pages
# *  `set_cache_path(path)`: set the absolute path to the folder where the pages files will be cached

# ## HTML Clean functions

# Function to eliminate unwanted part of the html like comments or script tags
#
# Clear html is the main switch , it enable or disable all the other functions
# *  `enable_clear_html()`: enable the clear html function
# *  `disable_clear_html()`: disable the clear html function
# *  `enable_clear_comments()`: the spyder will delete the comments from the html
# *  `disable_clear_comments()`:  the spyder will NOT delete the comments from the html
# *  `set_useless_attributes(attributes_list)`:  set the list of attributes that will be eliminated (if there are any) from the html in every tags. ex. set_useless_attributes(["style","id"]) will eliminate every style or id attribute from the tags.
# *  `set_useless_tags(tags_list)`: set the list of tags that will be eliminated (if there are any) from the html. ex.set_useless_tags(["img","p"]) will eliminate every img and p tag from the html.

# ## Search Algorithm

# The search work somewhat like disktra's algorithm where instead of having the cost on the edges of the graph it has them it on the nodes and it get the minimum spanning tree of the page link's graph.

# * `set_cost_function(f)` the function f(soup,url) has to return the cost of the page which is a real non negative number

# The default cost function return always 1 so that the spyder will do a width first search.
# The more the max cost is bigger then the min cost, decided by the function, the more the algorithm will tend to do a depth first search.
