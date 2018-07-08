"""Documentaion HTTP server.

This module provides an HTTP server exclusively for the purpose of serving HTML
documentation over HTTP.
"""

try:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from http.server import BaseHTTPRequestHandler, HTTPServer

from .parser import parse
from .writer import html


def _make_request_handler(project_path):
    class RequestHandler(BaseHTTPRequestHandler):
        def send_headers(self):
            self.send_response(200 if self.path == '/' else 404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        def do_HEAD(self):
            self.send_headers()

        def do_GET(self):
            self.send_headers()

            if self.path == '/':
                project = parse(project_path)
                contents = html(project)

                self.wfile.write(
                    contents.encode('utf-8')
                )

    return RequestHandler


class Server(HTTPServer):
    """Documentation HTTP server.

    It will serve HTML documentation for the project at `project_path`. A
    documentation server will only accept `HEAD` and `GET` requests and reply
    with 404s for any request that's not made on `/`.
    """
    def __init__(self, host, port, project_path):
        handler = _make_request_handler(project_path)
        super().__init__((host, port), handler)
