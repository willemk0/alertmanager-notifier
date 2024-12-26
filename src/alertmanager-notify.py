#!/usr/bin/python

import os, subprocess, argparse
import requests, time
from notifypy import Notify
from xdg.Config import icon_theme as sys_icon_theme
from xdg.IconTheme import IconTheme, getIconPath
import threading

import logging
logging.basicConfig(level=logging.INFO)


if sys_icon_theme == "hicolor":
    icon_path = '/usr/share/icons/Tango/24x24/status'
    warn_icon = icon_path + '/dialog-warning.png'
    crit_icon = icon_path +'/messagebox_critical.png'
else:
    warn_icon = 'dialog-warning'
    crit_icon = 'messagebox_critical'

notification = Notify()
notification.title = "Alertmanager notification"
notification.icon = "icons/prometheus_logo_grey.svg"

pending = False
verbose = False
 

# Parse command line arguments
def create_args():
    parser = argparse.ArgumentParser(description="Alertmanager desktop notification",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-n", "--interval",
                        help="Prometheus query interval seconds",
                        type=int,
                        default=30)
    parser.add_argument("--pending",
                        action="store_true",
                        help="Include alerts in pending state")
    parser.add_argument("--insecure",
                        action="store_true",
                        help="Disable SSL")
    parser.add_argument("--verbose",
                        action="store_true",
                        help="Verbose output")
    parser.add_argument("prom_server", help="Server address")
    args = parser.parse_args()

    if args.interval:
        if args.interval < 10 or args.interval > 300:
            print("Error: Interval should be between 10 to 300 seconds")
            exit()

    return args

# Return alerts
def get_alerts(prom_url: str, ssl: bool):
    notification = Notify()
    notification.title = "Alertmanager notification"
    notification.icon = "icons/prometheus_logo_grey.svg"

    try:
        resp = requests.get(prom_url, verify=ssl)
        resp.raise_for_status()
    except requests.exceptions.Timeout:
        notification.message = "Connection timeout.\nrRetrying in 30 seconds..."
        time.sleep(30)
        raise notification.send()
    except requests.exceptions.HTTPError as errh:
        notification.message = "Unable to connect to\n" + server
        raise notification.send()

    results = resp.json()
    logging.debug(results)

    return results

# Display notification
def prom_notify(prom_url: str, interval: int, ssl: bool):
    notifications = []
    alert_list = {}
    remove_list = []
    repeat = 300 / interval
    repeat = 10

    if verbose:
        print("Query interval n seconds: %s" % interval)
        print("Repeat n seconds: %s" % repeat)

    i = 0
    while True:
        results = get_alerts(prom_url, ssl)

        total = len(results['data']['alerts'])
        logging.debug("Total alerts: %d" % total)
        if total == 0 and len(alert_list) > 0:
            alert_list.clear()
        else:
            for item in results['data']['alerts']:

                # filter pending alerts
                if item['state'] == "pending" and pending == False:
                    continue

                # prepare notification
                name = item['labels']['alertname']
                msg = item['annotations']['summary']
                if item['labels']['severity'] == "critical":
                    notification.icon = getIconPath(crit_icon)
                elif item['labels']['severity'] == "warning":
                    notification.icon = getIconPath(warn_icon)

                notification.title = name
                notification.message = msg
                logging.info("alertmanager-notifiy: %s - %s" % (name, msg))

                # notification already at dict
                if alert_list.get(name) is not None:
                    v = alert_list.get(name)
                    if v >= repeat:
                        v = 0
                        notification.send()
                    else:
                        v = v + 1
                    alert_list.update([(name, v)])
                else:
                    notification.send()
                    alert_list.update([(name, 0)])

        logging.debug(alert_list)


        i = i + 1
        time.sleep(interval)

def main():
    config = create_args()
    ssl = config.insecure
    global pending
    pending = config.pending
    global verbose
    verbose = config.verbose
 
    prom_url = config.prom_server + '/api/v1/alerts'

    logging.info("alertmanager-notify starting...")
    notification.message = "Starting..."
    notification.send()

    try:
        response = requests.get(prom_url, verify=ssl)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        notification.message = "Unable to connect to\n" + server
        raise notification.send()

    logging.debug("System icon theme: %s" % sys_icon_theme)
    logging.debug(warn_icon)
    logging.debug(crit_icon)

    prom_notify(prom_url, config.interval, ssl)

if __name__ == "__main__":
    main()
