from ollama import AsyncClient
from .prompts import build_prompt
from .config import settings


async def analyse_transcript(transcript: str, industry: str | None = None) -> str:
    """Run the local Ollama model asynchronously and return the structured analysis."""
    prompt = build_prompt(transcript, industry)

    if settings.ollama_host:
        client = AsyncClient(host=settings.ollama_host)
    else:
        client = AsyncClient()

    response = await client.chat(
        model=settings.ollama_model,
        messages=[{"role": "user", "content": prompt}],
    )

    return response["message"]["content"].strip()
