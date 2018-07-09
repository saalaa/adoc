"""Documentaion HTTP server.

This module provides an HTTP server exclusively for the purpose of serving HTML
documentation over HTTP.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer

from .parser import parse
from .writer import html


class RequestHandler(BaseHTTPRequestHandler):
    """Documentation HTTP request handler.

    It will serve HTML documentation for the project at `project_path`. A
    documentation server will only accept `HEAD` and `GET` requests and reply
    with 404s for any request that's not made on `/`.
    """
    def send_headers(self):
        self.send_response(200 if self.path == '/' else 404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_HEAD(self):
        """Respond to `HEAD` requests."""
        self.send_headers()

    def do_GET(self):
        """Respond to `GET` requests.

        Only `/` will be served, other paths will result in 404s.
        """
        self.send_headers()

        if self.path == '/':
            project = parse(self.server.project_path)
            contents = html(project)

            self.wfile.write(
                contents.encode('utf-8')
            )


class Server(HTTPServer):
    """Documentation HTTP server.

    It will reponde to HTTP requests using `RequestHandler`.
    """
    def __init__(self, host, port, project_path):
        self.project_path = project_path

        super().__init__(
            (host, port), RequestHandler
        )
