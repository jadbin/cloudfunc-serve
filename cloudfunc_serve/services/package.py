# coding=utf-8

import os
from os.path import join, isfile, isdir
import shutil
import tarfile
import fcntl

from flask import abort
from werkzeug.utils import secure_filename
from guniflask.config import settings
from guniflask.context import service

from cloudfunc_serve.services.docker import DockerService


@service
class PackageService:
    def __init__(self, docker_service: DockerService):
        self.docker_service = docker_service

    def update_package(self, name: str, version: str, file):
        lock_file = join(settings['dists_home'], '{}.lock'.format(name))
        dist_name = secure_filename(file.filename)
        dist_file = join(settings['dists_home'], dist_name)
        dist_dir = join(settings['dists_home'], dist_name.split('.', maxsplit=1)[0])
        package_dir = join(settings['packages_home'], name)
        with open(lock_file, 'w') as fd:
            fcntl.flock(fd, fcntl.LOCK_EX)
            self._check_version(name, version)
            try:
                file.save(dist_file)
                with tarfile.open(dist_file, 'r') as f:
                    def is_within_directory(directory, target):
                        
                        abs_directory = os.path.abspath(directory)
                        abs_target = os.path.abspath(target)
                    
                        prefix = os.path.commonprefix([abs_directory, abs_target])
                        
                        return prefix == abs_directory
                    
                    def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                    
                        for member in tar.getmembers():
                            member_path = os.path.join(path, member.name)
                            if not is_within_directory(path, member_path):
                                raise Exception("Attempted Path Traversal in Tar File")
                    
                        tar.extractall(path, members, numeric_owner=numeric_owner) 
                        
                    
                    safe_extract(f, dist_dir)
                self.docker_service.remove_cloud_func(name)
                if isdir(package_dir):
                    shutil.rmtree(package_dir)
                shutil.move(dist_dir, package_dir)
                self.docker_service.run_cloud_func(name)
            finally:
                if isfile(dist_file):
                    os.remove(dist_file)
                if isdir(dist_dir):
                    shutil.rmtree(dist_dir)

    def _check_version(self, name: str, version: str):
        # TODO
        pass
