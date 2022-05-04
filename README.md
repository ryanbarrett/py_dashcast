# py_dashcast

Script to launch urls on chromecast dashboards.

## Setup
create a virtual environment and activate it; then install requirements.
```
$ python3 -m venv env && . env/bin/activate
$ pip install -r requirements.txt
```

Use the virtualenv python to launch the script.
cron may look something like this (need to test)
```
/5 * * * * /home/my/virtual/bin/python /home/my/project/py_dashcast.py
```


## Help

```
usage: py_cast.py [-h] [--discover] [--json_config JSON_CONFIG] [--force] [--debug] [--show_zeroconf_debug]

Example that shows how the DashCast controller can be used.

optional arguments:
  -h, --help            show this help message and exit
  --discover            Discover chromecasts
  --json_config JSON_CONFIG
                        Path to json config file
  --force               Force reload of url
  --debug               Enable debug log
  --show_zeroconf_debug
                        Enable debug log
```

