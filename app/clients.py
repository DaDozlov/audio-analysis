import os, openai, groq

from .config import settings

if settings.openai_api_key:
    openai.api_key = settings.openai_api_key


def call_openai(prompt: str, **kwargs):
    return openai.ChatCompletion.create(model="gpt-3.5-turbo", prompt=prompt, **kwargs)


def call_groq(prompt: str, **kwargs):
    # Beispiel-Wrapper, anpassen auf tatsächliche Groq-Client-Lib
    client = groq.Client(api_key=settings.groq_api_key)
    return client.completions.create(model="groq-model", prompt=prompt, **kwargs)
