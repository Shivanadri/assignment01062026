import http.server, mimetypes, os
mimetypes.add_type("application/javascript", ".jsx")
os.chdir(os.path.dirname(os.path.abspath(__file__)))
httpd = http.server.HTTPServer(("", 3001), http.server.SimpleHTTPRequestHandler)
print("Frontend running at http://localhost:3001")
httpd.serve_forever()
