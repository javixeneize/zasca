FROM python:alpine3.15
ARG yasca_version
RUN apk update && \
    apk upgrade && \
    apk add maven
RUN pip install yasca==$yasca_version
COPY entrypoint.sh .
ENTRYPOINT ["/bin/sh","/entrypoint.sh"]