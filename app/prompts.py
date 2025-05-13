from datetime import datetime
from typing import Optional

from .variables import BASE_PROMPT_DE, CONTEXT_SNIPPETS


def build_prompt(
    transcript: str,
    context: Optional[str] = None,
) -> str:
    """
    Build a prompt for transcript analysis, optionally injecting context‑specific hints.

    Parameters
    ----------
    transcript : str
        The conversation transcript to analyse.
    context : str | None
        Industry or meeting context (e.g. "bank", "autowerkstatt", "hr").

    Returns
    -------
    str
        A fully composed prompt ready to be sent to the LLM.
    """
    # base prompts
    prompt_parts: list[str] = [BASE_PROMPT_DE.strip()]

    # if a recognised context is provided, append its guidance
    if context and context.lower() in CONTEXT_SNIPPETS:
        prompt_parts.append(CONTEXT_SNIPPETS[context.lower()].strip())

    # add timestamp and the raw transcript
    timestamp = datetime.utcnow().isoformat(timespec="seconds")
    prompt_parts.append(f"Transkript (erstellt am {timestamp} UTC):\n{transcript}")

    return "\n\n".join(prompt_parts)
