import re
import logging
from typing import Tuple, List, Dict, Any, Optional
from backend.app.config import settings

logger = logging.getLogger("angiyam.session_guard")

# Forbidden off-topic patterns that signal drift or prompt injection disclosure
OFF_TOPIC_TRIGGER_PATTERNS = [
    r"\b(prime minister|narendra modi|president|politics|election|parliament)\b",
    r"\b(system prompt|hidden prompt|instructions provided to me|i am an ai model|as an ai)\b",
    r"\b(python code|def main\(|import sys|function\(\)|algorithm code)\b",
    r"\b(cheat code|jailbreak|bypass instructions)\b",
]


class SessionGuard:
    """
    Validates that LLM responses stay strictly inside the active session scenario,
    maintain the assigned persona, reject prompt injection, and do not wander off-topic.
    """
    def __init__(self):
        self.max_regenerations = settings.MAX_GUARD_REGENERATIONS

    def validate_response(
        self,
        ai_response: str,
        user_message: str,
        ai_role: str,
        scenario: str,
        allowed_topics: List[str],
        forbidden_topics: List[str]
    ) -> Tuple[bool, Optional[str]]:
        """
        Evaluate if the generated response conforms to the active scenario boundary.
        Returns: (is_valid: bool, violation_reason: Optional[str])
        """
        if not ai_response or len(ai_response.strip()) < 3:
            return False, "Response is empty or too short."

        response_lower = ai_response.lower()
        user_lower = user_message.lower() if user_message else ""

        # 1. Check for AI meta-talk or prompt disclosure
        meta_phrases = ["as an ai language model", "as an ai", "my system prompt", "my instructions are", "i cannot act as"]
        for phrase in meta_phrases:
            if phrase in response_lower:
                return False, f"AI broke character with meta-phrase: '{phrase}'"

        # 2. Check for off-topic answering (e.g., if user asked about Prime Minister or Politics and AI actually answered it)
        for pattern in OFF_TOPIC_TRIGGER_PATTERNS:
            if re.search(pattern, response_lower, re.IGNORECASE):
                # If user asked off-topic, did the AI answer it instead of redirecting?
                # A valid response should be a polite redirection, not answering factual trivia.
                if any(kw in response_lower for kw in ["is the prime minister", "won the election", "here is the code"]):
                    return False, f"AI answered off-topic query matching pattern '{pattern}'."

        # 3. Check for explicitly forbidden session topics
        for forbidden in forbidden_topics:
            if forbidden.lower() in response_lower and forbidden.lower() not in [t.lower() for t in allowed_topics]:
                return False, f"Response referenced strictly forbidden topic '{forbidden}'."

        # 4. Length check: Responses must not be excessive lectures
        words = ai_response.split()
        if len(words) > 75:
            return False, "Response exceeds maximum conversational length (too verbose)."

        return True, None

    def get_safe_stage_fallback(
        self,
        ai_role: str,
        scenario: str,
        current_stage_name: str,
        user_message: str = ""
    ) -> str:
        """
        Deterministic, safe in-character fallback response mapped to the current scenario & stage.
        """
        scenario_lower = scenario.lower()

        if "hotel" in scenario_lower or "receptionist" in ai_role.lower():
            if "greet" in current_stage_name.lower() or "reservation" in current_stage_name.lower():
                return "Welcome! Could you please share your booking name so I can pull up your reservation details?"
            elif "room" in current_stage_name.lower() or "card" in current_stage_name.lower():
                return "I have prepared your room key card. Our complimentary breakfast is served from 7 to 10 AM. Do you have any other questions?"
            else:
                return "I'm your hotel receptionist for this check-in. Let's make sure your stay is set up comfortably. Could we confirm your details?"

        if "interview" in scenario_lower or "interviewer" in ai_role.lower():
            return "As your interviewer today, I'd like to hear more about your relevant experience and projects. Could you give me an example?"

        if "restaurant" in scenario_lower or "server" in ai_role.lower():
            return "I'm happy to help with your order today! Would you like to hear our specials or are you ready for the main course?"

        if "classmate" in scenario_lower or "campus" in scenario_lower:
            return "That's great! What department or major are you studying in this semester?"

        # General scenario redirection fallback
        return f"Let's focus on our conversation today. As the {ai_role}, what would you like to discuss next regarding our scenario?"


session_guard = SessionGuard()
