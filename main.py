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

with open('static/header.html', 'r') as file:
	header = file.read().encode("utf-8")

with open('static/footer.html', 'r') as file:
	footer = file.read().encode("utf-8")

with open('playlist.txt', 'r') as file:
	playlist = file.read()

searchform = b'<form method="POST"><input type="text" class="search" name="search" placeholder="Liedwunsch"><button type="submit">Suchen</button></form>'

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		self.send_response(200)
		self.end_headers()
		self.wfile.write(header + searchform + footer)
	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		body = self.rfile.read(content_length)
		arrpost = body.split(b'=')
		
		self.send_response(200)
		self.end_headers()
		
		response = BytesIO()
		
		if arrpost[0] == b'search':
			response.write(header)
			response.write(b'<form method="POST"><table>')
			hits = api.search(str(arrpost[1], "utf-8"))
			songhits = hits["song_hits"]
			for song in songhits:
				response.write(b'<tr><td><b>')
				response.write(song["track"]["title"].encode("utf-8"))
				response.write(b'</b><hr>')
				response.write(song["track"]["artist"].encode("utf-8"))
				response.write(b'<hr>')
				response.write(song["track"]["album"].encode("utf-8"))
				response.write(b'</td><td><button type="submit" name="add" value="')
				response.write(song["track"]["storeId"].encode("utf-8"))
				response.write(b'"><img height="40px" width="40px" src="')
				response.write(song["track"]["albumArtRef"][0]["url"].encode("utf-8"))
				response.write(b'"></button></td></tr>')
			response.write(b'</table></form>')
			response.write(footer)

		elif arrpost[0] == b'add':
			song = str(arrpost[1], "utf-8")
			api.add_songs_to_playlist(playlist, [song])
			
			response.write(header)
			response.write(b'<h2>Lied gespeichert!</h2><br>')
			response.write(searchform)
			response.write(footer)

		self.wfile.write(response.getvalue())

httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
