import json
from operator import itemgetter

SEVERITY = {'CRITICAL': 4, 'HIGH': 3, 'MODERATE': 2, 'LOW': 1}

def check_quality_gate(severity_data, threshold):
    qg_passed = True
    try:
        threshold_value = SEVERITY.get(threshold)
        for k,v in severity_data.items():
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
                if vuln['package'] == fp.get('package') and fp.get('vulnerability') in map(itemgetter('value'), advisory_list):
                    report.remove(vuln)
                    suppressed_issues.append(vuln.copy())
    except FileNotFoundError:
        print ("File not found. Skipping suppression process..")
    except json.decoder.JSONDecodeError:
        print("JSON malformed. Skipping suppression process..")
    return report, suppressed_issues