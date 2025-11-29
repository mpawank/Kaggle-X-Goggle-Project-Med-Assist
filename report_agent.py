import textwrap

def make_report(intake, triage_result, info, mode='mock'):
    patient_summary = (
        f"You reported: {intake.get('chief_complaint')} for {intake.get('duration_days')} days. "
        f"Suggested urgency: {triage_result.get('level')}. Actions: {'; '.join(triage_result.get('actions', []))}."
    )
    clinician_note = textwrap.dedent(f"""    S: Patient reports {intake.get('chief_complaint')} for {intake.get('duration_days')} days. Severity {intake.get('severity')}.
    O: (No vitals in demo)
    A: Triage level: {triage_result.get('level')} - {triage_result.get('reason')}
    P: {', '.join(triage_result.get('actions', []))}
    Additional info: {info.get('summary')}
    References: {', '.join(info.get('references', []))}
    """)
    # Optionally use Gemini to polish (API mode)
    if mode == 'api':
        try:
            from llm import gemini, configure_from_env
            configure_from_env()
            prompt = f"""Create two sections:
1) Patient-friendly 3-sentence summary.
2) Clinician SOAP note using inputs below.

Intake: {intake}
Triage: {triage_result}
Info: {info}

Do not give diagnoses or treatment plans. Keep it conservative and factual."""
            polished = gemini(prompt, max_tokens=400)
            # heuristically split sections if possible
            parts = polished.strip().split('\n\n', 1)
            patient_summary = parts[0].strip() if parts else patient_summary
            clinician_note = parts[1].strip() if len(parts) > 1 else clinician_note
        except Exception as e:
            clinician_note = clinician_note + f"\n\n(Note: LLM polishing unavailable: {e})"

    return {'patient_summary': patient_summary, 'clinician_note': clinician_note}
