from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO

from gmusicapi import Mobileclient

api = Mobileclient()

with open('key.txt', 'r') as file:
	key = file.read()

if not api.oauth_login(key): #valide device-id
	api.perform_oauth()

if not api.is_authenticated():
	print("Authentication failed somehow")
	quit()


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		self.send_response(200)
		self.end_headers()
		with open('static/index.html', 'r') as file:
			self.wfile.write(file.read().encode("utf-8"))

	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		body = self.rfile.read(content_length)
		arrpost = body.split(b'=')
		
		self.send_response(200)
		self.end_headers()
		
		response = BytesIO()
		with open('static/header.html', 'r') as file:
			response.write(file.read().encode("utf-8"))

		if arrpost[0] == b'search':
			hits = api.search(str(arrpost[1], "utf-8"))
			songhits = hits["song_hits"]
			for song in songhits:
				print(song)
				response.write(b'<tr><td>')
				response.write(song["track"]["title"].encode("utf-8"))
				response.write(b'</td><td>')
				response.write(song["track"]["artist"].encode("utf-8"))
				response.write(b'</td><td>')
				response.write(song["track"]["album"].encode("utf-8"))
				response.write(b'</td><td><button type="submit" name="add" value="')
				response.write(song["track"]["storeId"].encode("utf-8"))
				response.write(b'">+</button></td></tr>')
			
		with open('static/footer.html', 'r') as file:
			response.write(file.read().encode("utf-8"))

		self.wfile.write(response.getvalue())

httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
