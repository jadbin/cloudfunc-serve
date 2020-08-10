# coding=utf-8

# Database URI when using Flask-SQLAlchemy, example: mysql+pymysql://username:password@server/db?charset=utf8mb4
# SQLALCHEMY_DATABASE_URI = ''

docker_host = 'unix:///var/run/docker.sock'
docker_base_image = 'jadbin/cloudfunc'
docker_container_prefix = 'cloudfunc-'

# guniflask configuration
guniflask = dict(
    cors=True,
    consul={},
)
