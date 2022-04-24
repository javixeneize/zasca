import json
import os

PATH_PROJECT = os.path.realpath(os.path.dirname(__file__))


def generate_cyclonedx_sbom(dependencies):
    with open(PATH_PROJECT + '/template/cyclonedx_template.json') as file:
        cyclone_data = json.loads(file.read())

    for item in dependencies:
        del item['package']
        item['type'] = 'library'
        cyclone_data['components'].append(item.copy())

    with open('cyclonedx_report.json', 'w') as file:
        file.write(json.dumps(cyclone_data))
