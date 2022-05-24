import json
from operator import itemgetter
import os
from jinja2 import Template
from datetime import datetime

PATH_PROJECT = os.path.realpath(os.path.dirname(__file__))
SEVERITY = {'CRITICAL': 4, 'HIGH': 3, 'MODERATE': 2, 'LOW': 1, 'OFF': 5}


def check_quality_gate(severity_data, threshold):
    qg_passed = True
    try:
        threshold_value = SEVERITY.get(threshold)
        for k, v in severity_data.items():
            if SEVERITY.get(k) >= threshold_value:
                qg_passed = False
        return qg_passed
    except TypeError:
        print("Quality gate not valid. It has to be CRITICAL, HIGH, MODERATE or LOW")
        return False


def suppress_fp(report, suppression_file):
    suppressed_issues = []
    try:
        with open(suppression_file) as file:
            fp_list = json.loads(file.read())
        for fp in fp_list:
            for vuln in report:
                advisory_list = vuln.get('advisory').get('advisory').get('identifiers')
                if vuln['package'] == fp.get('package') and fp.get('vulnerability') in map(itemgetter('value'),
                                                                                           advisory_list):
                    report.remove(vuln)
                    suppressed_issues.append(vuln.copy())
    except FileNotFoundError:
        print("File not found. Skipping suppression process..")
    except json.decoder.JSONDecodeError:
        print("JSON malformed. Skipping suppression process..")
    return report, suppressed_issues


def generate_cyclonedx_sbom(dependencies):
    with open(PATH_PROJECT + '/template/cyclonedx_template.json') as file:
        cyclone_data = json.loads(file.read())

    for item in dependencies:
        del item['package']
        item['type'] = 'library'
        cyclone_data['components'].append(item.copy())

    with open('cyclonedx_report.json', 'w') as file:
        file.write(json.dumps(cyclone_data))


def generate_html_report(data, appname):
    with open(PATH_PROJECT + '/template/report_template.html') as file:
        template = Template(file.read())
        template.globals['now'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    with open('sca_report.html', 'w') as file:
        file.write(template.render(report=data, appname=appname))
