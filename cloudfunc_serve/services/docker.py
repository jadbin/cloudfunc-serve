# coding=utf-8

from os.path import join
from shutil import copyfile

from guniflask.config import settings
from guniflask.context import service
from docker import DockerClient, errors as docker_errors
from docker.models.containers import Container


@service
class DockerService:
    def __init__(self):
        self.docker = DockerClient(settings['docker_host'])

    def run_cloud_func(self, name: str):
        self._copy_files_before_run(name)
        self.docker.containers.run(
            settings['docker_base_image'],
            name='{}{}'.format(settings['docker_container_prefix'], name),
            command=['python', 'serve.py'],
            network_mode='host',
            restart_policy={'Name': 'always'},
            volumes={
                join(settings['packages_home'], name): {
                    'bind': f'/opt/{name}',
                    'mode': 'ro'
                }
            },
            working_dir=f'/opt/{name}',
            stdin_open=True,
            tty=True,
            detach=True
        )

    def _copy_files_before_run(self, name: str):
        dest_files = [join(settings['packages_home'], name, 'serve.py')]
        src_files = [join(settings['home'], 'resources', 'serve.py')]
        for src_file, dest_file in zip(src_files, dest_files):
            copyfile(src_file, dest_file)

    def start_could_func(self, name: str):
        try:
            container: Container = self.docker.containers.get('{}{}'.format(settings['docker_container_prefix'], name))
        except docker_errors.NotFound:
            pass
        else:
            if container.status in ('running', 'restarting'):
                pass
            elif container.status == 'paused':
                container.unpause()
            elif container.status in ('created', 'exited'):
                container.start()
            else:
                self.remove_cloud_func(name)

    def restart_could_func(self, name: str):
        self.remove_cloud_func(name)
        self.run_cloud_func(name)

    def remove_cloud_func(self, name: str):
        try:
            container: Container = self.docker.containers.get('{}{}'.format(settings['docker_container_prefix'], name))
        except docker_errors.NotFound:
            pass
        else:
            container.stop()
            container.remove()
