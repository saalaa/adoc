"""Documentaion HTTP server.

This module provides an HTTP server exclusively for the purpose of serving HTML
documentation over HTTP.
"""

import logging

from http import server

from .writers.html import make_html

logger = logging.getLogger(__name__)


class RequestHandler(server.BaseHTTPRequestHandler):
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

        docstrings_format = self.server.docstrings_format
        strip_docstrings = self.server.strip_docstrings

        if self.path == '/':
            project = self.server.parser.parse()

            contents = make_html(
                project, docstrings_format, strip_docstrings
            )

            self.wfile.write(
                contents.encode('utf-8')
            )

    def log_message(self, format, *args):
        requestline, code, size = args

        logging_func = logger.error
        if int(code) // 100 == 2:
            logging_func = logger.info

        logging_func(format, requestline, code, size)


class Server(server.HTTPServer):
    """Documentation HTTP server.

    It will reponde to HTTP requests using `RequestHandler`.
    """
    def __init__(self, host, port, parser, docstrings_format,
                 strip_docstrings):
        self.parser = parser
        self.docstrings_format = docstrings_format
        self.strip_docstrings = strip_docstrings

        super().__init__(
            (host, port), RequestHandler
        )
