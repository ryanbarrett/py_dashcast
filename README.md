# py_dashcast

Script to launch urls on chromecasts.


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
usage: py_dashcast.py [-h] [--discover] [--json_config JSON_CONFIG] [--force] [--debug] [--show_zeroconf_debug]

Discover and cast urls to chromecasts

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

## Note - Chromecast with Google TV

Settings I've been testing to allow the Dashcast app to stay in the forefront. Rebooting via power cable is recommended.
```
 Disable ambient mode app: Settings > Apps > All apps > Set Ambient mode to disabled
 Stay awake: Developer mode: Settings > System > About > Tap button on Build 7 times Developer menu > Stay Awake
```

## Examples

./examples includes ways to refresh a page within an iframe, 4-up display, and a page rotation. 

This requires the ability to host a static webpage.
