
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