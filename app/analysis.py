from ollama import AsyncClient
from .prompts import build_prompt
from .config import settings
import httpx

async def call_openai_async(prompt: str, **kwargs) -> dict:
    headers = {"Authorization": f"Bearer {settings.openai_api_key}"}
    json = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        **kwargs,
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=json
        )
        r.raise_for_status()
        return r.json()


async def call_groq_async(prompt: str, **kwargs) -> dict:
    headers = {
        "Authorization": f"Bearer {settings.groq_api_key}",
        "Content-Type": "application/json"
    }
    json_payload = {
        "model": settings.groq_model,
        "messages": [{"role": "user", "content": prompt}],
        **kwargs
    }
    async with httpx.AsyncClient(base_url="https://api.groq.com/openai/v1") as client:
        response = await client.post("/chat/completions", headers=headers, json=json_payload)
        response.raise_for_status()
        return response.json()


async def analyse_transcript(
    transcript: str, industry: str | None, prompt_override: str | None = None
) -> str:
    prompt = prompt_override or build_prompt(transcript, industry)

    # OpenAI
    if settings.openai_api_key:
        try:
            data = await call_openai_async(prompt, max_tokens=1024, temperature=0.2)
            return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"OpenAI API failed: {e}")

    # Groq
    if settings.groq_api_key:
        try:
            data = await call_groq_async(prompt, max_tokens=1024)
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Groq API failed: {e}")

    # Ollama
        try:
            client = AsyncClient(host=settings.ollama_host)
            resp = await client.chat(
                model=settings.ollama_model,
                messages=[{"role": "user", "content": prompt}]
            )
            return resp["message"]["content"].strip()
        except Exception as e:
            print(f"Ollama API failed: {e}")

    # if all fail
    raise RuntimeError("All AI providers failed to process the transcript.")
