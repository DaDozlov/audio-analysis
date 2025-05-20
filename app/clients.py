import openai
import groq
from .config import settings


# openai

openai.api_key = settings.openai_api_key


def call_openai(messages: list[dict], **kwargs):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, **kwargs
    )


# groq

client = groq.Groq(api_key=settings.groq_api_key)


def call_groq(messages: list[dict], **kwargs):
    return client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct", messages=messages, **kwargs
    )
