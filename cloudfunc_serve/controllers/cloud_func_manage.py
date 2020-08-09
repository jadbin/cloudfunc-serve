# coding=utf-8

from guniflask.web import blueprint, put_route

from cloudfunc_serve.services.docker import DockerService


@blueprint
class CloudFuncManage:
    def __init__(self, docker_service: DockerService):
        self.docker_service = docker_service

    @put_route('/manage/restart')
    def restart_cloud_func(self, name: str):
        # FIXME: get port from table
        self.docker_service.restart_could_func(name=name, port=8080)
        return 'success'
