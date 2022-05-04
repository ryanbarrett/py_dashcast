# pylint: disable=invalid-name

import argparse
import logging
import sys
import time

import zeroconf
import json

import pychromecast
from pychromecast.controllers import dashcast


parser = argparse.ArgumentParser(description="Discover and cast urls to chromecasts")
parser.add_argument("--discover", help="Discover chromecasts", action="store_true")
parser.add_argument("--json_config", help="Path to json config file", default="config.json")
parser.add_argument("--force", help="Force reload of url", action="store_true")
parser.add_argument("--debug", help="Enable debug log", action="store_true")
parser.add_argument("--show_zeroconf_debug", help="Enable debug log", action="store_true")
parser.epilog = "Example: python3 py_dashcast.py --discover  OR python3 py_dashcast.py --json_config config.json"
args = parser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
if args.show_zeroconf_debug:
    print("Zeroconf version: " + zeroconf.__version__)
    logging.getLogger("zeroconf").setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

def discover_chromecasts()->dict:
    chromecasts = {}
    logger.debug("Starting discovery")
    devices, browser = pychromecast.get_chromecasts()
    for device in devices:
        ccdevice = device
        logger.debug(f"Found device: {ccdevice.cast_info}")
        chromecasts[ccdevice.uuid] = {}
        chromecasts[ccdevice.uuid]["device"] = ccdevice
        chromecasts[ccdevice.uuid]["media_controller"] = ccdevice.media_controller.status
        chromecasts[ccdevice.uuid]["name"] = ccdevice.name
        chromecasts[ccdevice.uuid]["host"] = ccdevice.cast_info.host
        chromecasts[ccdevice.uuid]["model_name"] = ccdevice.model_name
        chromecasts[ccdevice.uuid]["is_idle"] = ccdevice.is_idle
    logger.debug("Stopping discovery")
    browser.stop_discovery()
    return chromecasts

def load_config(json_config):
    config = {}
    try:
        logger.debug(f"Loading config file {json_config}")
        config = dict(json.load(open(json_config)))
    except FileNotFoundError:
        logger.error(f'Config file "{json_config}" not found')
        sys.exit(1)
    except json.JSONDecodeError:
        logger.error(f'Config file "{json_config}" is not valid json')
        sys.exit(1)
    except TypeError:
        logger.error(f'Config file "{json_config}" is not a valid dict type json file')
        logger.error('expecting: {"Emergencies":"http://192.168.1.4/test-4frame.html","Some Other Chromecast":"http://192.168.1.4/test-4frame.html"}')
        sys.exit(1)
    return config

def cast_urls(cast_url_dict:dict, force=False):
    for uuid in cast_url_dict.keys():
        load_url = cast_url_dict[uuid]["url"]
        friendly_name = cast_url_dict[uuid]['name']
        expected_title = cast_url_dict[uuid]['expected_title']
        logger.debug(f"Starting discovery for {friendly_name}")
        chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[friendly_name])
        if not chromecasts:
            logger.error(f'No chromecast with uuid "{uuid}" discovered')
        else:
            cast = chromecasts[0]
            cast.wait()

            d = dashcast.DashCastController()
            cast.register_handler(d)

            logger.info(f"Chromecast info: {cast.cast_info.uuid} : {cast.cast_info.host} : {cast.cast_info.friendly_name}")
            time.sleep(1)
            logger.debug(f"cast.media_controller.status: {cast.media_controller.status}")

            # if the expected title is different from the current title, quit the app and reload the url
            # If force is set, quit the app and reload the url regardless
            if expected_title != cast.status.status_text or force:
                logger.debug(f"Expected title not found(or refresh forced), quitting app")
                cast.quit_app()
                time.sleep(1)
                logger.debug(f"Loading url: {load_url}")
                d.load_url(load_url,force=True)
                #Wait for the url to load before shutting down the browser.
                time.sleep(7)
                logger.info(f"chromecast is now running: {cast.status.status_text}")
            else:
                logger.info(f"{friendly_name} is already running {expected_title}")

        # Shut down discovery
        logger.debug(f"Shutting down discovery")
        browser.stop_discovery()


def main(args):
    cast_url_dict = {}
    # Run discovery only
    if args.discover:
        logger.info("Discovering chromecasts")
        devices = discover_chromecasts()
        for device in devices:
            logger.info(f"Found device: {devices[device]['name']} : {device} : {devices[device]['host']}")
    else:
        logger.debug(f"Loading config file {args.json_config}")
        cast_url_dict = load_config(args.json_config)
    
    if cast_url_dict:
        logger.debug(f"Casting urls to chromecasts")
        cast_urls(cast_url_dict,args.force)


if __name__ == "__main__":
    main(args)
