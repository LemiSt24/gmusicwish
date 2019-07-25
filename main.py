from http.server import HTTPServer, BaseHTTPRequestHandler

from gmusicapi import Mobileclient
"""
api = Mobileclient()

with open('key.txt', 'r') as file:
	key = file.read()

if not api.oauth_login(key): #valide device-id
	api.perform_oauth()

if not api.is_authenticated():
	print("Authentication failed somehow")
	quit()
"""


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		self.send_response(200)
		self.end_headers()
		with open('static/index.html', 'r') as file:
			self.wfile.write(file.read().encode("utf-8"))

	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		body = self.rfile.read(content_length)
		self.send_response(200)
		self.end_headers()
		response = BytesIO()
		response.write(b'This is POST request. ')
		response.write(b'Received: ')
		response.write(body)
		self.wfile.write(response.getvalue())

httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()