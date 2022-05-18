# doser.py
Very simple DoS tool for HTTP requests in Python with random User-Agents.

# Prerequisites
Install requirements.
`pip3 install -r requirement.txt`

# Examples
999 threads sends GET requests:

```bash
python3 doser.py 'https://targeted.site.com'
```

999 threads sends POST requests with json data:

```bash
python3 doser.py -x POST -I 'Content-Type: application/json' -d '{"json": "payload"}' 'https://targeted.site.com'
```

# Usage

```bash

usage: doser.py [-h] [-x X] [-f F] [-p P] [-i [I [I ...]]] [-t T] ...

Simple python based HTTP load testing tool.

positional arguments:
  url

optional arguments:
  -h, --help      show this help message and exit
  -x X            Request method (Default GET). Usage: -x POST URL
  -f F            Payload for the request
  -p P            Proxy url with host and port
  -i [I [I ...]]  Addtional header/s. Usage: -i 'Content-type: application/json' 'User-Agent: Doser'
  -t T            Number of threads to be used. Default 999
```

# Proxy usage (example with Tor)

1. Install prerequisites
`apt install -y tor privoxy`

2. Edit the config `/etc/privoxy/config`
```
listen-address 127.0.0.1:8118
listen-address [::1]:8118
forward-socks5t / 127.0.0.1:9050 .
```

Now run the doser with -p https://127.0.0.1:8118