FROM python:3

ADD ivrExample.py /
ADD menus.json /

RUN pip install flask
RUN pip install signalwire

EXPOSE 5000

CMD [ "python", "./ivrExample.py" ]