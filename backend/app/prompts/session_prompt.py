"""
Session Prompt Builders & Message Formatting
"""
from typing import List, Dict, Any


def format_conversation_history(turns: List[Dict[str, Any]], max_turns: int = 10) -> List[Dict[str, str]]:
    """
    Format recent conversation turns into standard chat messages format for LLM.
    Limits context to the last `max_turns` to optimize inference and avoid context drift.
    """
    messages = []
    # Take the latest turns
    recent_turns = turns[-max_turns:] if len(turns) > max_turns else turns
    
    for t in recent_turns:
        role = "assistant" if t.get("speaker") == "ai" else "user"
        content = t.get("transcript", "").strip()
        if content:
            messages.append({"role": role, "content": content})
            
    return messages


def build_guard_regeneration_prompt(original_response: str, violation_reason: str, ai_role: str, scenario: str) -> str:
    """Prompt to force the LLM to rewrite a non-compliant or off-topic response."""
    return f"""
Your previous response violated the active session boundary!
Violation: {violation_reason}
Previous response: "{original_response}"

Rewrite your response immediately:
1. Stay strictly in character as "{ai_role}" in scenario: "{scenario}".
2. Do not answer off-topic questions.
3. Keep it within 1 to 3 sentences.
4. Output ONLY your rewritten character dialogue.
"""
