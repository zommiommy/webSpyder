

import webSpyder

sett = webSpyder.Settings()

sett.enable_cache()
sett.disable_permessive_exception()


s = webSpyder.Spyder(sett,"wikipediaSpyder")

s.set_data_type("distribuitedWebList")

s.set_start_url("https://it.wikipedia.org/wiki/Pagina_principale")

def my_filter(url):
    return "wikipedia" in url

s.set_filter(my_filter)

def test_function(soup,url):
    pass

s.set_function(test_function)

print(s)

s.create_needed_folders()

s.iteration()


s.run(100)
