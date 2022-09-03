from zasca import utils, scanner
from zasca.maven_scanner import maven_tree_generator
from zasca.node_scanner import node_tree_generator
from tqdm import tqdm
import collections
import sys
import click

EMPTY_SUPPRESSION = 'emptysuppression.json'


def scan_maven(filepath, include_dev):
    maven_tree_generator.generate_tree(filepath, include_dev)
    dependencies, appname = maven_tree_generator.get_dependencies()
    mavenscan = scanner.Scanner(appname)
    trigger_scan(dependencies, mavenscan, 'MAVEN')
    return mavenscan.advisory_list, mavenscan.appname, dependencies


def scan_node(filepath):
    dependencies, appname = node_tree_generator.generate_tree(filepath)
    nodescan = scanner.Scanner(appname)
    trigger_scan(dependencies, nodescan, 'NPM')
    return nodescan.advisory_list, nodescan.appname, dependencies


def trigger_scan(dependencies, scanner, ecosystem):
    print("Scanning dependencies...")
    for dependency in tqdm(dependencies[0:3]):
        advisories = scanner.get_advisories(dependency.get('package'), ecosystem)
        if advisories:
            scanner.validate_vulnerable_version(advisories, dependency.get('package'), dependency.get('version'))


def write_output(num_issues, unique_libraries, num_fp, qg):
    print('{} vulnerabilities detected in {} vulnerable libraries'.format(num_issues, unique_libraries))
    if num_fp:
        print('{} vulnerabilities supressed'.format(num_fp))
    print('Quality gate passed: {}'.format(qg))


@click.command()
@click.argument('file', required=True)
@click.option('--sbom', help='Generates CycloneDX SBOM', default=True)
@click.option('--include_dev', help='Include dev dependencies', default=False)
@click.option('--quality_gate', help='Maximum severity allowed', default='LOW')
@click.option('--suppression_file', help='False positives to remove', default=EMPTY_SUPPRESSION)
def run_cli(file, sbom, include_dev, quality_gate, suppression_file):
    suppressed_items = []
    if file == 'pom.xml':
        data, appname, dependencies = scan_maven(file, include_dev)
    if file == 'package-lock.json':
        data, appname, dependencies = scan_node(file)
    if sbom:
        utils.generate_cyclonedx_sbom(dependencies)
    if suppression_file != EMPTY_SUPPRESSION:
        maven_data, suppressed_items = utils.suppress_fp(data, suppression_file)
    utils.generate_html_report(data, appname)
    unique_vuln_libraries = collections.Counter(item['package'] for item in data)
    severity_data = collections.Counter(item.get('advisory').get('severity') for item in data)
    qg_passed = utils.check_quality_gate(severity_data, quality_gate)
    write_output(len(data), len(unique_vuln_libraries), len(suppressed_items), qg_passed)
    sys.exit(not qg_passed)
