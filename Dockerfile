FROM python:alpine3.15
RUN apk update && \
    apk upgrade && \
    apk add maven
RUN pip install yasca
COPY entrypoint.sh .
ENTRYPOINT ["/bin/sh","/entrypoint.sh"]
