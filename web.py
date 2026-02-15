from http.server import BaseHTTPRequestHandler, HTTPServer
from os import path
from urllib import response
from urllib.parse import parse_qsl, urlparse
import html

class WebRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = dict(parse_qsl(parsed_url.query))
        path = parsed_url.path

        if path == "/":
            try:
                with open("home.html", "r", encoding="utf-8") as file:
                    content = file.read()

                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))

            except FileNotFoundError:
                self.send_response(500)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"<h1>500 - home.html no encontrado</h1>")

        elif path.startswith("/proyecto/"):
            self.handle_proyecto(path, query_params)

        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<h1>404 - Pagina no encontrada</h1>")


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
    
    def handle_proyecto(self, path, query_params):
        partes = path.split("/")
        proycto = partes[2] if len(partes) > 2 else "desconocido"

        autor = query_params.get("autor", "desconocido")

        proyecto = html.escape(proycto)
        autor = html.escape(autor)

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        response = f"<h1>Proyecto: {proyecto} Autor: {autor}</h1>"
        self.wfile.write(response.encode("utf-8"))

    def handle_default(self, parsed_url, query_params):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(response.encode("utf-8"))


PORT = 8000

if __name__ == "__main__":
    try:
        print(f"Starting server on http://localhost:{PORT}")
        server = HTTPServer(("localhost", PORT), WebRequestHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.server_close()