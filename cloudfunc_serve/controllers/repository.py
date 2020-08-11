# coding=utf-8

from flask import request
from guniflask.web import blueprint, post_route

from cloudfunc_serve.services.package import PackageService


@blueprint
class RepositoryController:
    def __init__(self, package_service: PackageService):
        self.package_service = package_service

    @post_route('/repo/upload')
    def upload_package(self):
        name = request.form['name']
        version = request.form['version']
        file = request.files['content']
        self.package_service.update_package(name, version, file)
        return 'success'
