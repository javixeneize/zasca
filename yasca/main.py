from yasca import maven_scanner, generate_report, tree_generator, sbom_generator, utils
from tqdm import tqdm
import collections
import click
import sys

def scan_maven(filepath, ignore_dev):
    tree_generator.generate_tree(filepath, ignore_dev)
    dependencies, appname = tree_generator.get_dependencies()
    mavenscan = maven_scanner.Maven_scanner(appname)
    print("Scanning dependencies...")
    for dependency in tqdm(dependencies):
        advisories = mavenscan.get_advisories(dependency.get('package'))
        if advisories:
            mavenscan.validate_vulnerable_version(advisories, dependency.get('package'), dependency.get('version'))
    return mavenscan.advisory_list, mavenscan.appname, dependencies

@click.command()
@click.argument('file', required=True)
@click.option('--sbom', help='Generates CycloneDX SBOM', is_flag=True, default=False)
@click.option('--include_dev', help='Include dev dependencies', is_flag=True, default=False)
@click.option('--quality_gate', help='Maximum severity allowed', default='LOW')
def run_cli(file, sbom, include_dev, quality_gate):
    maven_data, appname, dependencies = scan_maven(file, include_dev)
    generate_report.generate_html_report(maven_data, appname)
    if sbom:
        sbom_generator.generate_cyclonedx_sbom(dependencies)
    unique_vuln_libraries = collections.Counter(item['package'] for item in maven_data)
    print('{} vulnerabilities detected in {} vulnerable libraries'.format(len(maven_data), len(unique_vuln_libraries)))
    severity_data = collections.Counter(item.get('advisory').get('severity') for item in maven_data)
    qg_passed = utils.check_quality_gate(severity_data, quality_gate)
    print ('Quality gate passed: {}'.format(qg_passed))
    sys.exit(not qg_passed)