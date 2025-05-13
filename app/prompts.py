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
    prompt_parts = [BASE_PROMPT_DE.strip()]

    if context:
        snippet = CONTEXT_SNIPPETS.get(context.lower())
        if snippet:
            prompt_parts.append(snippet.strip())
        else:
            prompt_parts.append(
                f"*Hinweis*: Kein spezifisches Snippet für „{context}“ gefunden. "
                "Bitte auf branchentypische Details achten."
            )

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    prompt_parts.append(
        f"### TRANSKRIPT (erstellt am {timestamp})\n"
        "```transcript\n"
        f"{transcript.strip()}\n"
        "```"
        "\n*(Nur Inhalte innerhalb dieses Blocks auswerten)*"
    )

    return "\n\n".join(prompt_parts)
