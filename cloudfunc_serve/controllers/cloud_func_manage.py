# coding=utf-8

from flask import request
from guniflask.web import blueprint, put_route, post_route

from cloudfunc_serve.services.docker import DockerService
from cloudfunc_serve.services.package import PackageService


@blueprint
class CloudFuncManage:
    def __init__(self, docker_service: DockerService, package_service: PackageService):
        self.docker_service = docker_service
        self.package_service = package_service

    @put_route('/manage/restart')
    def restart_cloud_func(self, name: str):
        self.docker_service.restart_could_func(name=name)
        return 'success'

    @post_route('/manage/upload')
    def upload_package(self):
        name = request.form['name']
        version = request.form['version']
        file = request.files['content']
        self.package_service.update_package(name, version, file)
        return 'success'
