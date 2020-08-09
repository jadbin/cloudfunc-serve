FROM python:3.7

ADD ./ /opt/cloudfunc_serve
WORKDIR /opt/cloudfunc_serve

RUN chmod +x bin/manage \
  && pip install -r requirements/app.txt

CMD bin/manage start --daemon-off
