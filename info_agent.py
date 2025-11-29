INFO_BANK = {
    'fever and cough': {
        'summary': 'Common causes include viral infections (e.g., common cold, influenza), COVID-19, or bacterial infections.',
        'when_to_seek_care': 'If fever > 38.5°C, difficulty breathing, chest pain, or symptoms persist >7 days, seek medical care.',
        'references': ['WHO', 'CDC: Respiratory infections']
    },
    'default': {
        'summary': 'General medical information: If new or worsening symptoms occur, contact a healthcare professional.',
        'when_to_seek_care': 'Follow local guidance and seek urgent care for red-flag symptoms.',
        'references': ['WHO', 'CDC']
    }
}

def fetch_info(topic, mode='mock'):
    key = topic.strip().lower()
    if mode == 'mock':
        return INFO_BANK.get(key, INFO_BANK['default'])
    # API mode -> use Gemini to produce a short, cited educational summary
    try:
        from llm import gemini, configure_from_env
        configure_from_env()
        prompt = f"""Provide a SAFE, neutral, evidence-backed medical education summary about: {topic}
- 3-4 bullet points (plain language)
- When to seek care (1 line)
- List 2 reputable references (CDC/WHO/NHS)
Do NOT provide diagnoses or personalized treatment."""
        text = gemini(prompt, max_tokens=300)
        return {'summary': text.strip(), 'when_to_seek_care': 'See text above.', 'references': ['See generated text (CDC/WHO)']}
    except Exception as e:
        return INFO_BANK.get(key, INFO_BANK['default'])
