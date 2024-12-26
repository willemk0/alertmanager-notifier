# alertmanager-notify

An unoficial Alertmanager desktop notification

# Installing from source

```
git clone https://github.com/willemk0/alertmanager-notify
pip3 install .
```

# Usage help

```
usage: alertmanager-notify [-h] [-n INTERVAL] [--pending] [--insecure] [--verbose] prom_server

Alertmanager desktop notification

positional arguments:
  prom_server           Server address

options:
  -h, --help            show this help message and exit
  -n INTERVAL, --interval INTERVAL
                        Prometheus query interval seconds (default: 30)
  --pending             Include alerts in pending state (default: False)
  --insecure            Disable SSL (default: False)
  --verbose             Verbose output (default: False)
```

# Example

```
alertmanager-notify https://localhost
```
