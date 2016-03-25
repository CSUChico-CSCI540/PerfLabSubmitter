FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install -y supervisor
RUN groupadd -r celery && useradd -r -g celery celery
ADD celery.conf /etc/supervisor/conf.d/
RUN mkdir /home/celery/
RUN mkdir /home/celery/.ssh
RUN chown celery:celery -R /home/celery/
ADD id_rsa.pub /home/celery/.ssh/id_rsa.pub
ADD id_rsa /home/celery/.ssh/id_rsa
RUN chown celery:celery -R /home/celery/.ssh


CMD supervisord -c /etc/supervisor/supervisord.conf
#ADD celeryd /etc/default/
#ADD initd /etc/init.d/celeryd
#RUN chmod 755 /etc/init.d/celeryd
#RUN chown root:root /etc/init.d/celeryd