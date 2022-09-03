FROM javidr/yasca_base:latest
COPY . zasca/
RUN cd zasca && python setup.py sdist bdist_wheel && pip install dist/*.whl
COPY entrypoint.sh .
ENTRYPOINT ["/bin/sh","/entrypoint.sh"]
