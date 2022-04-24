from jinja2 import Template
from datetime import datetime
import os

PATH_PROJECT = os.path.realpath(os.path.dirname(__file__))


def generate_html_report(data, appname):
    with open(PATH_PROJECT + '/template/report_template.html') as file:
        template = Template(file.read())
        template.globals['now'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    with open('sca_report.html', 'w') as file:
        file.write(template.render(report=data, appname=appname))
