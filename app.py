import requests
import chainlit as cl

API_KEY = "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"
URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

@cl.on_message
async def main(message: cl.Message):
    system_prompt = """The chatbot will only respond to platform-relevant queries (orders, services, policies).
Out-of-scope or unrelated questions will be politely declined with a guided redirection to supported topics.
To avoid infinite loops:
The AI will attempt clarification only once or twice
If still unresolved, it will automatically suggest raising a support ticket
No hallucinated or speculative responses; the AI responds only when confidence is above a defined threshold."""
    payload = {
        "model": "openai/o4-mini",
        "messages": [
            # {"role": "system", "content": system_prompt},
            {"role": "user", "content": message.content} 
        ],
        "max_tokens": 256,
        "reasoning": {"enabled": True}
    }

    response = requests.post(URL, headers=HEADERS, json=payload)
    response_json = response.json()

   
    if "choices" not in response_json:
        await cl.Message(
            content="Sorry, I couldn’t process that request right now."
        ).send()
        return

    answer = response_json["choices"][0]["message"]["content"]

    await cl.Message(content=answer).send()
