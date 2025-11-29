def run_intake(raw_input=None):
    if raw_input is None:
        return {
            "age": 35,
            "sex": "F",
            "chief_complaint": "Fever and cough",
            "duration_days": 3,
            "severity": 5,
            "red_flags": []
        }
    intake = {
        "age": int(raw_input.get('age', 0)),
        "sex": raw_input.get('sex', 'U'),
        "chief_complaint": str(raw_input.get('chief_complaint', '')).strip(),
        "duration_days": int(raw_input.get('duration_days', 0)),
        "severity": int(raw_input.get('severity', 1)),
        "red_flags": raw_input.get('red_flags', [])
    }
    return intake
