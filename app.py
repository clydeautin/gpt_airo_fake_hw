from openai import OpenAI
import os
import json
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

load_dotenv()

#initialize the client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#helps us load files from an outside file
def load_messages_from_file(path: str) -> list[dict]:
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"{path} not found")
    
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {path}") from e
    
SYSTEM_PROMPT = """

### ROLE
You are an intelligent email classifier for AirOps a company that helps marketing teams build ai-powered workflows that turn messy inputs
into structured, reliable outputs

### CATEGORIES & ACTION MAPPING
Classify the message into one of the following categories and assign the corresponding 'recommended_action':


1. "sales": Inquiries about pricing, security, enterprise features, or demo requests.
   - Action: "route_to_sales_ae"
2. "tech_support": Technical issues, API errors, integration failures, or "how-to" questions.
   - Action: "create_support_ticket"
3. "feedback": General praise, feature requests, or UI/UX suggestions.
   - Action: "log_to_product_backlog"
4. "other": Spam, out-of-office replies, or nonsensical text.
   - Action: "no_action_required"

### CONFIDENCE SCORING
- 0.90–1.00: Explicit intent and clear keywords.
- 0.70–0.89: Clear intent, but lacks specific details (e.g., "It's broken" without saying what).
- 0.50–0.69: Ambiguous; message could span two categories.
- < 0.50: Pure guesswork; default to "other".

### OUTPUT RULES
- Output ONLY valid JSON.
- Do not include markdown formatting or backticks (unless using a JSON-specific API mode).
- The 'reasoning' field should briefly explain the confidence score and category choice.

{
    "category": "string",
    "confidence_score": float,
    "recommended_action": "string",
    "reasoning": "string" 
}

"""

def classify_msg(message, model="gpt-4o-mini"):
    response = client.chat.completions.create(
        model = model,
        messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": message}
        ],
        temperature=0.5, # low but not too low becasue we still want the LLM to explain reasoning
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)

if __name__ == "__main__":
    cust_message = load_messages_from_file("cust_messages.json")
    for msg in cust_message:
        result = classify_msg(msg["text"])

        #manually adds the message id back into the json result instead of sending it to the LLM
        output = {
            "id": msg["id"],
            **result
        }
        print("\n--- new message ---")
        print(json.dumps(output, indent=2))