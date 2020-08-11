# coding=utf-8

import sys
from typing import List
from os.path import abspath, dirname, join
import socket
from pip._internal.cli.main import main as pip_main

from cloudfunc.setuptools import run_setup, after_setup
from cloudfunc.app import create_app
from gevent.pywsgi import WSGIServer

home = dirname(abspath(__file__))
sys.path.append(home)

pip_index = 'https://pypi.doubanio.com/simple/'


def install_requirements(install_requires: List[str]):
    if not install_requires:
        return
    cmd = ['install'] + install_requires + ['--index', pip_index]
    pip_main(cmd)


def default_settings(name: str, port: int) -> dict:
    return dict(
        project_name=name,
        home=home,
        port=port,
        active_profiles=['prod'],
        guniflask=dict(
            cors=True,
            consul={}
        ))


def get_free_port() -> int:
    sock = socket.socket()
    sock.bind(('', 0))
    _, port = sock.getsockname()
    sock.close()
    return port


def main():
    run_setup(join(home, 'setup.py'))
    install_requirements(after_setup['install_requires'])
    name = after_setup['name']
    port = get_free_port()
    app = create_app(name,
                     settings=default_settings(name, port),
                     includes=after_setup['includes'])
    wsgi = WSGIServer(('0.0.0.0', port), application=app)
    wsgi.serve_forever()


if __name__ == '__main__':
    main()
