import json
import re
from typing import Optional, Dict, Any, Type
from pydantic import BaseModel, ValidationError
import logging

logger = logging.getLogger("angiyam.json_validation")


def extract_json_block(text: str) -> Optional[str]:
    """Extract JSON from raw LLM text (handling markdown code blocks or raw JSON)."""
    if not text:
        return None
    
    # 1. Try finding ```json ... ``` codeblock
    match = re.search(r"```(?:json)?\s*(\{[\s\S]*?\}|\[[\s\S]*?\])\s*```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # 2. Try finding outermost { ... }
    first_brace = text.find("{")
    last_brace = text.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        return text[first_brace:last_brace + 1].strip()
        
    return None


def parse_and_validate_json(raw_text: str, schema_class: Type[BaseModel]) -> Optional[BaseModel]:
    """Parse JSON text and validate with a Pydantic schema model."""
    json_str = extract_json_block(raw_text) or raw_text
    try:
        data = json.loads(json_str)
        return schema_class.model_validate(data)
    except (json.JSONDecodeError, ValidationError) as e:
        logger.warning(f"JSON validation error: {e}. Raw text: {raw_text[:200]}...")
        # Clean trailing commas
        cleaned = re.sub(r",\s*([\]}])", r"\1", json_str)
        try:
            data = json.loads(cleaned)
            return schema_class.model_validate(data)
        except Exception:
            return None
