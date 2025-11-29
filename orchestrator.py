import json, os
from intake_agent import run_intake
from triage_agent import triage
from info_agent import fetch_info
from report_agent import make_report

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def pipeline_session(session_id, raw_input=None, mode="mock"):
    intake = run_intake(raw_input)
    triage_result = triage(intake, mode=mode)
    info = fetch_info(intake.get('chief_complaint', ''), mode=mode)
    report = make_report(intake, triage_result, info, mode=mode)

    out = {
        "session_id": session_id,
        "intake": intake,
        "triage": triage_result,
        "info": info,
        "report": report
    }
    with open(f"{LOG_DIR}/{session_id}.json", "w") as f:
        json.dump(out, f, indent=2)
    return out

if __name__ == '__main__':
    sample = {
        "age": 58,
        "sex": "M",
        "chief_complaint": "Chest pain and shortness of breath",
        "duration_days": 0,
        "severity": 9,
        "red_flags": []
    }
    res = pipeline_session("sample_chestpain", sample, mode='mock')
    print(json.dumps(res, indent=2))
