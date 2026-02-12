from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse
import html

class WebRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = dict(parse_qsl(parsed_url.query))

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        response = self.build_response(parsed_url, query_params)
        self.wfile.write(response.encode("utf-8"))

    def build_response(self, parsed_url, query_params):
        safe_headers = html.escape(str(self.headers))
        safe_path = html.escape(self.path)
        safe_query = html.escape(str(query_params))

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Hola Web</title>
        </head>
        <body>
            <h1>Hola Web</h1>
            <p><strong>URL Parse Result:</strong> {parsed_url}</p>
            <p><strong>Path Original:</strong> {safe_path}</p>
            <p><strong>Headers:</strong> {safe_headers}</p>
            <p><strong>Query:</strong> {safe_query}</p>
        </body>
        </html>
        """

PORT = 8000

if __name__ == "__main__":
    try:
        print(f"Starting server on http://localhost:{PORT}")
        server = HTTPServer(("localhost", PORT), WebRequestHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.server_close()