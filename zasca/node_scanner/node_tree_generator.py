import json

dependency_list = []


def get_dependencies(data, parent=''):
    for dependency, depdata in data.get('dependencies').items():
        item = {'package': dependency, 'version': depdata.get('version')}
        if parent:
            item['parent'] = '{}@{}'.format(parent, data.get('version'))
        if 'dependencies' in depdata:
            get_dependencies(depdata, dependency)
        dependency_list.append(item)


def generate_tree(filepath):
    with open(filepath) as f:
        data = json.loads(f.read())
    get_dependencies(data)
    appname = {'package': data.get('name'), 'version': data.get('version')}
    return dependency_list, appname
