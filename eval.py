import csv, json
from orchestrator import pipeline_session

def load_cases(path):
    cases = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for r in reader:
            case = {
                'id': r['id'],
                'age': int(r.get('age', 0)),
                'sex': r.get('sex', 'U'),
                'chief_complaint': r.get('chief_complaint', ''),
                'duration_days': int(r.get('duration_days', 0)),
                'severity': int(r.get('severity', 1))
            }
            cases.append((case, r.get('expected_level', '')))
    return cases

if __name__ == '__main__':
    cases = load_cases('data/synthetic_cases.csv')
    results = []
    for case, expected in cases:
        out = pipeline_session(case['id'], case, mode='mock')
        predicted = out['triage']['level']
        results.append({'id': case['id'], 'predicted': predicted, 'expected': expected})
    print(json.dumps(results, indent=2))
