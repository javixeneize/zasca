FROM python:alpine3.15
RUN pip install yasca
COPY entrypoint.sh .
ENTRYPOINT ["/bin/sh","/entrypoint.sh"]
