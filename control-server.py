import time
import serial
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

hostName = ''
hostPort = 8000
serial = serial.Serial('/dev/ttyACM0', 9600)

class MyServer(BaseHTTPRequestHandler):
	
	def _handleError(self, message):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		self.wfile.write(bytes("<html><head><title>Error</title></head><body>Chyba: %s</body></html>" % message, "utf-8"))
	
	def do_POST(self):
		form = cgi.FieldStorage(fp=self.rfile,headers=self.headers,environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':self.headers['Content-Type']})
		if "blink" in form :
			self._startBlink()
		elif "no-blink" in form:
			self._stopBlink()
		self.do_GET()
		

	def do_GET(self):
		"""
		Serve index.html
		"""
		try:
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			f = open("index.html")
			self.wfile.write(bytes(f.read(), "utf-8"))
			f.close()
		except:
			print("Error")
			self._handleError("Unexpected error")


	def _startBlink(self):
		serial.write(b'1')

	def _stopBlink(self):
		serial.write(b'0')
	

def getSerial():
	return serial.Serial('/dev/ttyACM0', 9600)

def main():
	try:
		print("Starting server")
		server = HTTPServer((hostName, hostPort), MyServer)
		print(time.asctime(), "Server starts - %s:%s" % (hostName, hostPort))
		server.serve_forever()
	except KeyboardInterrupt:
		print("Received ^C, stopping server")
		server.server_close()

main()
	

#while True:
#	print("Up")
#	ser.write(b'1')
#	time.sleep(timeout)
#	print("Down")
#	ser.write(b'0')
#	time.sleep(timeout)

