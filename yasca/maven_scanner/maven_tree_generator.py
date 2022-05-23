import subprocess  # nosec
import sys
import os

PATH_PROJECT = os.path.realpath(os.path.dirname(__file__))
DEP_FILE = PATH_PROJECT + '/yasca_dep_tree.txt'


def generate_tree(filepath, include_dev):
    scope = '-Dscope=compile'
    exitcode = 0
    try:
        if include_dev:
            scope = '-Dscope=test'
        exitcode = subprocess.call(['mvn', 'dependency:tree', '-Doutput={}'.format(DEP_FILE), '-f',  # nosec
                                    filepath, scope],
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.STDOUT)
    except FileNotFoundError:
        print("Looks like maven is not correctly installed or the pom.xml file can't be resolved. Please check")
    if exitcode != 0:
        print("There has been an error building the tree")
        sys.exit(exitcode)
    else:
        return exitcode


def get_dependencies():
    dependencies = []
    dependency_info = {}
    with open(DEP_FILE) as f:
        data = f.read().replace('+-', '').replace('|', '').replace('\-', ''). \
            replace(' ', '').rstrip().split('\n')  # noqa: W605
    for dependency in data:
        dependency = dependency.replace('\n', '').split(':')
        if len(dependency) == 5 or len(dependency) == 4:
            dependency.pop(2)
        dependency_info['package'] = dependency[0] + ':' + dependency[1]
        dependency_info['group'] = dependency[0]
        dependency_info['name'] = dependency[1]
        dependency_info['version'] = dependency[2]
        dependencies.append(dependency_info.copy())
    appname = dependencies[0]
    del dependencies[0]
    os.remove(DEP_FILE)
    return dependencies, appname
