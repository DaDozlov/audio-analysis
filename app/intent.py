import asyncio
import logging

logger = logging.getLogger(__name__)


async def analyze_intent(llm, email_body: str) -> str:
    logger.debug("Analyzing user intent")

    prompt = f"""
IMPORTANT: Your response must ONLY contain either:

1. The original query exactly as provided (if no prefix applies)
2. A prefix followed by a space and then the original query (if a prefix applies)

DO NOT include any explanations, analysis, or additional text.

Analyze the core user request/query from the following input, ignoring any system responses, command outputs, or conditional statements:

For the intent analysis ignore any text that appears to be conditional statements (if X then Y) but do not remove it from the query.

User Query: {email_body}

Available prefixes:
1. '/web' if any of these conditions are met:
   - The user explicitly asks to search or check the internet/web
   - The user's query requires weather information
   - The query contains phrases like "Suche im Internet", "im Internet suchen", "online", "Internet", "search the web", "search the internet"
2. '/excel' if both these conditions are met:
   - The user is clearly asking to retrieve something from an Excel file.
   - The word "excel" is present in the query.
3. '/generate_excel' if the user is requesting to create an Excel file.
4. '/web /generate_excel' if the user is requesting to create a Excel file from web-scraped information.
5. '/generate_powerpoint' if the user is requesting to create a PowerPoint presentation.
6. '/web /generate_powerpoint' if the user is requesting to create a PowerPoint presentation from web-scraped information.
7. '/generate_word' if the user is requesting to create a Word document.
8. '/web /generate_word' if the user is requesting to create a Word document from web-scraped information.
9. '/call' if the user is requesting to make a call.
10. '/booking' if the user is requesting to make a booking (meeting).
11. '/calendar' if the user is asking about calendar information (for example free slots or booked slots).
12. '/cancel' if the user is requesting to cancel a booking (meeting).
13. '/reschedule' if the user is requesting to reschedule a booking (meeting).
14. '/note_create' if the user is requesting to create a OneNote note.
15. '/note_get' if the user is requesting to retrieve a OneNote note.
16. '/note_create /web' if both these conditions are met:
    - The user is requesting to create a OneNote note.
    - The query requires gathering information from the internet.
17. '/hedge' if the user is requesting to analyze a stock, fund, or anything related to stock market analysis or investing.

Special cases:
- If the query contains '/PA' or '/web /PA' or '/pdf', return it unchanged
- If the query contains '/adjust_email' and is not about Excel, return it unchanged
- If the query contains '/adjust_email' and is about Excel, use '/excel' prefix and extract text between 'User Request:' and 'Relevant files for reference:'
- If the query contains 'Relevant files for reference:' and is about Excel, remove that part and what follows
- If the query contains 'Relevant files for reference:' and is not about Excel, return it unchanged

REMEMBER: Return ONLY the prefix (if applicable) and query. NO explanations or additional text.
"""

    # Run the llm.invoke call in a thread so we stay async
    response = await asyncio.to_thread(llm.invoke, prompt, True, category="chat")
    logger.debug(f"Detected intent: {response}")
    return response.strip()
