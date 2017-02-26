# Florid-Scanner
An active scanner

### Usage:

```
python florid.py -h
python florid.py -u "http://testphp.vulnweb.com/product.php?pic=1" -m "sqli,test"
python florid.py -u "http://testphp.vulnweb.com/product.php?pic=1" -m ALL -v
```

### Tips

After you scanned a website by this scanner, the system will generate a directory in "./log" named by the hostname of the website. The result of the spider.py will be stored in url_list.txt in that directory.

If you want to include "sqli" module, you should run "sqlmapapi.py", because the function is based on it.

### Development

Just add module into the directory - "./mod". 

Variable `MODULE_NAME` is needed.

Function `init()` should return `True` to tell the main script the initialization of this module works properly.

Function `run(options)` if the entry of the module.
