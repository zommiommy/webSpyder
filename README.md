# webSpyder
A little class for making the spyder job easier, it's in a really early point of development but it should work

## An example:

Import the package


```python
import webSpyder
```

Create an istance of the spyder


```python
s = webSpyder.Spyder("""http://www.giallozafferano.it/ricette-cat/page32/""")
```

Create your custom function which decide if the current url have to be parsed or not.

You can add as many function as you wish.

The Spyder take the and of all the filter functions, so all of them have to return True so that the url is parsed.


```python
def my_filter(url):
    return "ricette" in url
```


```python
s.set_filter(my_filter)
```

Create your custom function which recive the soup (bs4 parse html) and the url of the current page.

You can add as many function as you wish.

Each function is called on every page the spyder decide to download and parse.


```python
def test_function(soup,url):
    print("hi the url is %s"%url)
```


```python
s.set_function(test_function)
```

The current state of the spyder is printable


```python
print(s)
```

    settings:
    {'mode': 'wget', 'start_url': 'http://www.giallozafferano.it/ricette-cat/page32/', 'directory': '/home/zommiommy/Desktop/webSpyder/pagecaches/', 'cache': True}
    
    index: 0
    
    urls:
    ['http://www.giallozafferano.it/ricette-cat/page32/']


It can do a single url at time.


```python
s.iteration()
```

    http://www.giallozafferano.it/ricette-cat/page32/
    using cached httpwwwgiallozafferanoitricettecatpage.html
    hi the url is http://www.giallozafferano.it/ricette-cat/page32/


Or it can go on parsing urls that it find in the pages until there aren't anyone left.


```python
s.run()
```
