FROM python:alpine3.15
ARG yasca_version
RUN apk update && \
    apk upgrade && \
    apk add maven
COPY dist/yasca-$yasca_version-py3-none-any.whl .
RUN pip install yasca-$yasca_version-py3-none-any.whl && rm yasca-$yasca_version-py3-none-any.whl
COPY entrypoint.sh .
ENTRYPOINT ["/bin/sh","/entrypoint.sh"]