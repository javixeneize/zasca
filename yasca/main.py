from yasca import maven_scanner, generate_report, tree_generator, sbom_generator
from tqdm import tqdm
import collections
import argparse


def scan_maven(filepath):
    tree_generator.generate_tree(filepath)
    dependencies, appname = tree_generator.get_dependencies()
    mavenscan = maven_scanner.Maven_scanner(appname)
    print("Scanning dependencies...")
    for dependency in tqdm(dependencies):
        advisories = mavenscan.get_advisories(dependency.get('package'))
        if advisories:
            mavenscan.validate_vulnerable_version(advisories, dependency.get('package'), dependency.get('version'))
    return mavenscan.advisory_list, mavenscan.appname, dependencies


def run_cli_scan(file, html, sbom):
    maven_data, appname, dependencies = scan_maven(file)
    if html:
        generate_report.generate_html_report(maven_data, appname)
    if sbom:
        sbom_generator.generate_cyclonedx_sbom(dependencies)

    unique_vuln_libraries = collections.Counter(item['package'] for item in maven_data)

    print('{} vulnerabilities detected in {} vulnerable libraries'.format(len(maven_data), len(unique_vuln_libraries)))


def run_cli():
    parser = argparse.ArgumentParser(description='SCApegoat, an opensource SCA tool')
    parser.add_argument('file', type=str, help='Path for the pom.xml file')
    parser.add_argument('--html', type=bool, default=True, help='Generates a html report')
    parser.add_argument('--sbom', type=bool, default=False, help='Generates a SBOM')
    args = parser.parse_args()
    run_cli_scan(args.file, args.html, args.sbom)
