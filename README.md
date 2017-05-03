# Florid Scanner
An active scanner for CTF Game

### Usage:

```
python florid.py -h
python florid.py -u "http://testphp.vulnweb.com/product.php?pic=1" -m ALL
```

:![](DOCUMENT/show.gif)

### Tips

After you scanned a website by this scanner, the system will generate a directory in "./log" named by the hostname of the website. The result of the spider.py will be stored in url_list.txt in that directory.

Now the scanner can scan for the backup files from VIM and Gedit, and sensitive directories and files.

### Development

The modules to run before the check starts should be placed in `./mod/phase1`

The modules for checking URLs should be placed in `./mod/phase2`

You are expected to develop your modules referring to `./mod/phase2/sample.py`
