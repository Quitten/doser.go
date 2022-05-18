#!/usr/bin/python3
# noqa: F401
import requests
import requests_random_user_agent
import sys
import threading
import random
import argparse
import resource

host = ''
request_counter = 0
printedMsgs = []
payload = None
proxies = None
method = 'GET'
resource.setrlimit(resource.RLIMIT_NOFILE, (999999, 999999))


def printMsg(msg):
    if msg not in printedMsgs:
        print(f"\n{msg} after {request_counter} requests")
        printedMsgs.append(msg)


def initHeaders():
    global additionalHeaders, url
    headers = {'Cache-Control': 'no-cache',
               'Referer': url,
               'Keep-Alive': str(random.randint(110, 120)),
               'Connection': 'keep-alive'
               }

    if additionalHeaders:
        for header in additionalHeaders:
            headers.update({header.split(":")[0]: header.split(":")[1]})
    return headers


def handleStatusCodes(status_code):
    global request_counter
    sys.stdout.write(f"\r{request_counter} requests has been sent.")
    sys.stdout.flush()
    if status_code == 429:
        printMsg("You have been throttled (429).")
    elif status_code == 500:
        printMsg("Status code 500 received.")


def sendRequest(url, payload):
    global request_counter, method
    try:
        request_counter += 1
        request = requests.request(method=method, url=url, proxies=proxies,
                                   data=payload, headers=initHeaders()
                                   )
        handleStatusCodes(request.status_code)
    except Exception as e:
        printMsg(e)
        pass


class SendThread(threading.Thread):
    def run(self):
        try:
            while True:
                global url, payload
                sendRequest(url, payload)
        except Exception as e:
            printMsg(e)
            pass


def main(argv):
    parser = argparse.ArgumentParser(description='Simple python based HTTP load testing tool.')
    parser.add_argument('-x', help='Request method (Default GET). Usage: -x POST URL', default='GET')
    parser.add_argument('-f', help='Payload for the request', default=None)
    parser.add_argument('-p', help='Proxy url with host and port', default=None)
    parser.add_argument('-i', help='Addtional header/s. Usage: -i \'Content-type: application/json\' \'User-Agent: Doser\'', default=None, nargs='*')
    parser.add_argument('-t', help='Number of threads to be used. Default 999', default=999, type=int)
    parser.add_argument('url', nargs=argparse.REMAINDER)
    args = parser.parse_args()

    global url, payload, additionalHeaders, method, proxies
    additionalHeaders = args.i
    payload = args.f
    method = args.x
    url = args.url[0]
    
    if args.p:
        proxies = {
            'http': args.p,
            'https': args.p,
        }

    for i in range(args.t):
        SendThread().start()

    if len(sys.argv) == 1:
        parser.print_help()
        exit()


if __name__ == "__main__":
    main(sys.argv[1:])
