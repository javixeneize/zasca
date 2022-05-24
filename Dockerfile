FROM javidr/yasca_base:latest
COPY . yasca/
RUN cd yasca && python setup.py sdist bdist_wheel && pip install dist/*.whl
COPY entrypoint.sh .
ENTRYPOINT ["/bin/sh","/entrypoint.sh"]
