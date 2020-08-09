# coding=utf-8

from typing import List

from guniflask.config import settings
from guniflask.context import service
from docker import DockerClient, errors as docker_errors
from docker.models.containers import Container


@service
class DockerService:
    def __init__(self):
        self.docker = DockerClient(settings['docker_host'])

    def run_cloud_func(self, name: str, port: int):
        self.docker.containers.run(settings['docker_base_image'],
                                   name='{}{}'.format(settings['docker_container_prefix'], name),
                                   command=self._get_run_command(name),
                                   ports={'{}/tcp'.format(port): port},
                                   restart_policy={'Name': 'always'},
                                   stdin_open=True,
                                   tty=True,
                                   detach=True)

    def _get_run_command(self, name: str) -> List[str]:
        # FIXME
        return ['/bin/bash']

    def restart_could_func(self, name: str, port: int):
        try:
            container: Container = self.docker.containers.get('{}{}'.format(settings['docker_container_prefix'], name))
        except docker_errors.NotFound:
            pass
        else:
            container.stop()
            container.remove()
        self.run_cloud_func(name, port)
