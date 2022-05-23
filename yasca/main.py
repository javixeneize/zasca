from yasca import utils
from yasca.maven_scanner import maven_tree_generator, maven_scanner
from tqdm import tqdm
import collections
import sys
import click

EMPTY_SUPPRESSION = 'emptysuppression.json'


def scan_maven(filepath, include_dev):
    maven_tree_generator.generate_tree(filepath, include_dev)
    dependencies, appname = maven_tree_generator.get_dependencies()
    mavenscan = maven_scanner.Maven_scanner(appname)
    print("Scanning dependencies...")
    for dependency in tqdm(dependencies):
        advisories = mavenscan.get_advisories(dependency.get('package'))
        if advisories:
            mavenscan.validate_vulnerable_version(advisories, dependency.get('package'), dependency.get('version'))
    return mavenscan.advisory_list, mavenscan.appname, dependencies


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
    maven_data, appname, dependencies = scan_maven(file, include_dev)
    if sbom:
        utils.generate_cyclonedx_sbom(dependencies)
    if suppression_file != EMPTY_SUPPRESSION:
        maven_data, suppressed_items = utils.suppress_fp(maven_data, suppression_file)
    utils.generate_html_report(maven_data, appname)
    unique_vuln_libraries = collections.Counter(item['package'] for item in maven_data)
    severity_data = collections.Counter(item.get('advisory').get('severity') for item in maven_data)
    qg_passed = utils.check_quality_gate(severity_data, quality_gate)
    write_output(len(maven_data), len(unique_vuln_libraries), len(suppressed_items), qg_passed)
    sys.exit(not qg_passed)
