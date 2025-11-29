RED_FLAG_KEYWORDS = [
    "chest pain", "shortness of breath", "loss of consciousness", "severe bleeding", "sudden weakness",
    "slurred speech", "sudden vision loss", "severe allergic reaction"
]

def check_red_flags(intake):
    flags = []
    text = (intake.get('chief_complaint', '') + ' ' + ' '.join(intake.get('red_flags', []))).lower()
    for kw in RED_FLAG_KEYWORDS:
        if kw in text:
            flags.append(kw)
    return flags

def action_map(level):
    return {
        "Low": ["Self-care: rest, hydration; see GP if symptoms persist"],
        "Moderate": ["Schedule GP within 48-72 hours; monitor symptoms"],
        "High": ["Contact your provider today; consider urgent care"],
        "Emergency": ["Call emergency services (112/911) and go to nearest ER immediately"] 
    }[level]

def triage(intake, mode='mock'):
    flags = check_red_flags(intake)
    if flags:
        return {
            'level': 'Emergency',
            'reason': f"Red flags detected: {', '.join(flags)}",
            'actions': action_map('Emergency')
        }
    if intake.get('duration_days', 0) > 14 or intake.get('severity', 0) >= 8:
        level = 'High'
    elif intake.get('severity', 0) >= 5:
        level = 'Moderate'
    else:
        level = 'Low'
    rationale = f"Determined {level} based on duration {intake.get('duration_days')} days and severity {intake.get('severity')} (deterministic rules)."

    # If api mode, you can optionally call Gemini to produce a short rationale (not required for safety)
    if mode == 'api':
        try:
            from llm import gemini, configure_from_env
            configure_from_env()
            prompt = f"""You are a conservative medical triage assistant. Classify urgency as Emergency/High/Moderate/Low and give a 1-2 line rationale.
Intake: {intake}"""
            llm_text = gemini(prompt, max_tokens=200)
            rationale = llm_text.strip().split('\n')[0]
        except Exception as e:
            # fallback to deterministic rationale if Gemini call fails
            rationale = rationale + f" (LLM unavailable: {e})"

    return {'level': level, 'reason': rationale, 'actions': action_map(level)}
