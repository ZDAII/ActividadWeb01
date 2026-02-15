from http.server import BaseHTTPRequestHandler, HTTPServer
from os import path
from urllib import response
from urllib.parse import parse_qsl, urlparse
import html

class WebRequestHandler(BaseHTTPRequestHandler):

    contenido = {
        "/": """
        <html>
            <head><meta charset="UTF-8"><title>Home</title></head>
            <body>
                <h1>Home Page</h1>
                <ul>
                    <li><a href="/proyecto/web-uno">Proyecto Web Uno</a></li>
                    <li><a href="/proyecto/web-dos">Proyecto Web Dos</a></li>
                    <li><a href="/proyecto/web-tres">Proyecto Web Tres</a></li>
                </ul>
            </body>
        </html>
        """,

        "/proyecto/web-uno": """
        <html>
            <head><meta charset="UTF-8"></head>
            <body>
                <h1>Proyecto: web-uno</h1>
            </body>
        </html>
        """,

        "/proyecto/web-dos": """
        <html>
            <head><meta charset="UTF-8"></head>
            <body>
                <h1>Proyecto: web-dos</h1>
            </body>
        </html>
        """,

        "/proyecto/web-tres": """
        <html>
            <head><meta charset="UTF-8"></head>
            <body>
                <h1>Proyecto: web-tres</h1>
            </body>
        </html>
        """
    }

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        if path in self.contenido:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(self.contenido[path].encode("utf-8"))
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