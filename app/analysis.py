from ollama import AsyncClient
from .prompts import build_prompt
from .config import settings
import httpx
import traceback


async def call_openai_async(prompt: str, **kwargs) -> dict:
    headers = {"Authorization": f"Bearer {settings.openai_api_key}"}
    payload = {
        "model": settings.openai_model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": settings.openai_temperature,
        "max_tokens": settings.openai_max_tokens,
        **kwargs,
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
        )
        r.raise_for_status()
        return r.json()


async def call_groq_async(prompt: str, **kwargs) -> dict:
    headers = {
        "Authorization": f"Bearer {settings.groq_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.groq_model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": settings.groq_temperature,
        "max_tokens": settings.groq_max_tokens,
        **kwargs,
    }
    async with httpx.AsyncClient(base_url="https://api.groq.com/openai/v1") as client:
        response = await client.post("/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()


async def analyse_transcript(
    transcript: str,
    industry: str | None,
    prompt_override: str | None = None,
    provider: str | None = None,
) -> str:
    prompt = prompt_override or build_prompt(transcript, industry)

    backends = ["openai", "groq", "ollama"]
    debug_log = []

    if provider in backends:
        # Move the chosen provider to the front
        backends.remove(provider)
        backends.insert(0, provider)
        debug_log.append(f"[info] Preferred provider requested: {provider}")

    debug_log.append(f"[info] Backend priority: {backends}")

    last_exception = None

    for backend in backends:
        debug_log.append(f"[debug] Attempting backend: {backend}")

        try:
            if backend == "openai" and settings.openai_api_key:
                data = await call_openai_async(
                    prompt,
                    max_tokens=settings.openai_max_tokens,
                    temperature=settings.openai_temperature,
                )
                content = data["choices"][0]["message"]["content"].strip()
                debug_log.append("OpenAI succeeded.")
                print("\n".join(debug_log))
                return content

            elif backend == "groq" and settings.groq_api_key:
                data = await call_groq_async(
                    prompt,
                    max_tokens=settings.groq_max_tokens,
                    temperature=settings.groq_temperature,
                )
                content = data["choices"][0]["message"]["content"].strip()
                debug_log.append("Groq succeeded.")
                print("\n".join(debug_log))
                return content

            elif backend == "ollama" and settings.ollama_host:
                client = AsyncClient(host=settings.ollama_host)
                resp = await client.chat(
                    model=settings.ollama_model,
                    messages=[{"role": "user", "content": prompt}],
                )
                content = resp["message"]["content"].strip()
                debug_log.append("Ollama succeeded.")
                print("\n".join(debug_log))
                return content

            else:
                debug_log.append(
                    f"[warning] Skipped {backend} - Missing credentials or config."
                )

        except Exception as e:
            tb_str = traceback.format_exc()
            debug_log.append(f"[error] {backend} failed with exception:\n{tb_str}")
            last_exception = e

    debug_log.append("[fatal] All backends failed.")
    print("\n".join(debug_log))

    raise RuntimeError(
        "All AI providers failed to process the transcript."
    ) from last_exception
