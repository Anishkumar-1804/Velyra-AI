"""
Evidence-Based Evaluation Prompt Template for Angiyam.ai
"""
import json
from typing import List, Dict, Any


EVALUATION_SYSTEM_PROMPT = """
You are the Angiyam.ai Expert English Speaking Evaluator.
Your job is to analyze the user's transcript from their completed conversation session and produce a rigorous, evidence-based speaking evaluation.

### EVALUATION GUIDELINES:
1. ONLY evaluate based on the actual words the user spoke. Never invent mistakes or fabricate praise.
2. DO NOT mark simple, grammatically correct English as wrong. Only suggest improvements if there is a real grammatical error, awkward Indianism/literal translation, or a more natural idiomatic expression.
3. PRONUNCIATION: Label pronunciation as an approximate estimate based on fluency, sentence flow, and transcript clarity.
4. CORRECTIONS TABLE: Identify real grammatical, tense, preposition, or sentence structure issues.
5. VOCABULARY FEEDBACK: Suggest better contextual words for repetitive or overly basic words.
6. CEFR LEVEL: Estimate A1, A2, B1, B2, or C1 with concise reasoning based on the CEFR framework.

### REQUIRED JSON OUTPUT FORMAT:
You must respond ONLY with a valid JSON object matching this exact structure:
```json
{
  "overall_score": 78,
  "fluency": 80,
  "accuracy": 75,
  "grammar": 74,
  "vocabulary": 78,
  "pronunciation_estimate": 76,
  "comprehension": 85,
  "sentence_formation": 76,
  "naturalness": 79,
  "conversation_relevance": 88,
  "confidence_estimate": 80,
  "estimated_cefr": "B1",
  "cefr_reasoning": "Maintained conversational continuity with understandable vocabulary, but had occasional tense inconsistencies and prepositions errors.",
  "strengths": [
    "Responded quickly and maintained natural flow",
    "Understood the scenario requirements clearly"
  ],
  "improvements": [
    "Work on present perfect vs simple past tense distinctions",
    "Expand descriptive adjectives in responses"
  ],
  "corrections": [
    {
      "user_said": "I am working here from two years.",
      "better_version": "I have been working here for two years.",
      "issue": "Tense / Preposition",
      "explanation": "Use present perfect continuous ('have been working') and 'for' to indicate duration.",
      "category": "Tense"
    }
  ],
  "vocabulary_feedback": [
    {
      "word_used": "good",
      "better_alternative": "satisfactory / ideal",
      "reason": "Offers more precise description for formal contexts",
      "example": "This room looks ideal for my stay."
    }
  ],
  "naturalness_tips": [
    "Use contractions like 'I'd like' instead of 'I want' for polite requests."
  ],
  "recommendations": [
    "Practice Unit 2: Hotel Room Requests to master polite modal verbs."
  ]
}
```
"""


def build_evaluation_user_prompt(
    session_title: str,
    scenario: str,
    learning_objectives: List[str],
    target_cefr: str,
    transcript_dialogue: List[Dict[str, str]],
    speech_stats: Dict[str, Any]
) -> str:
    """Build the user prompt for evaluating a finished session."""
    dialogue_str = ""
    for turn in transcript_dialogue:
        speaker = "AI" if turn.get("speaker") == "ai" else "User"
        dialogue_str += f"{speaker}: {turn.get('transcript', '')}\n"

    stats_str = json.dumps(speech_stats, indent=2)

    return f"""
Please evaluate the following speaking practice session:

Session: {session_title}
Target CEFR: {target_cefr}
Scenario: {scenario}
Objectives: {", ".join(learning_objectives)}

Speech & Turn Metrics:
{stats_str}

Conversation Transcript:
----------------------------------------
{dialogue_str}
----------------------------------------

Output the complete evaluation as a valid JSON object matching the required schema.
"""
