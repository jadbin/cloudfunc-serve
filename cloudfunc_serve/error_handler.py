# coding=utf-8

from werkzeug.exceptions import HTTPException
from flask import Response
from guniflask.web import blueprint, app_error_handler


@blueprint
class ErrorHandler:
    @app_error_handler(HTTPException)
    def handle_http_exception(self, error: HTTPException):
        return Response(response=error.description, status=error.code)
