from ollama import AsyncClient
import asyncio
from .prompts import build_prompt
from .config import settings

async def _async_chat(prompt: str) -> str:
    client = AsyncClient(base_url=settings.ollama_base_url)
    response = await client.chat(model=settings.ollama_model, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"].strip()

def analyse_transcript(transcript: str, industry: str | None = None) -> str:
    """Synchronously run the LLM analysis."""
    prompt = build_prompt(transcript, industry)
    return asyncio.run(_async_chat(prompt))