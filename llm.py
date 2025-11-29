import os
import google.generativeai as genai

def configure_from_env():
    key = os.environ.get('GEMINI_API_KEY')
    if not key:
        raise EnvironmentError('GEMINI_API_KEY not set in environment. Set it in Kaggle Secrets.')
    genai.configure(api_key=key)

def gemini(prompt, model='gemini-1.5-flash', max_tokens=700):
    # Note: configure_from_env() should be called once by the notebook before using this.
    response = genai.GenerativeModel(model).generate_content(
        prompt,
        generation_config={"max_output_tokens": max_tokens}
    )
    # response may be an object; return its text representation
    text = getattr(response, 'text', None)
    if text is None:
        # try common alt attributes
        text = str(response)
    return text
