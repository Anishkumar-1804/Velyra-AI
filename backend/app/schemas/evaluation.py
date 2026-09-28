from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict


class CorrectionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    user_said: str
    better_version: str
    issue: str
    explanation: str
    category: str = "Grammar"


class VocabularyFeedbackSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    word_used: str
    better_alternative: str
    reason: str
    example: str


class EvaluationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    attempt_id: int
    overall_score: int
    fluency: int
    accuracy: int
    grammar: int
    vocabulary: int
    pronunciation_estimate: int
    comprehension: int
    sentence_formation: int
    naturalness: int
    conversation_relevance: int
    confidence_estimate: int
    
    estimated_cefr: str
    cefr_reasoning: Optional[str] = None
    
    total_speaking_time: float
    turn_count: int
    avg_response_words: float
    
    filler_count: int
    filler_rate: float
    most_used_filler: Optional[str] = None
    filler_breakdown: Dict[str, int] = {}
    repetition_analysis: Dict[str, int] = {}
    
    strengths: List[str] = []
    improvements: List[str] = []
    naturalness_tips: List[str] = []
    recommendations: List[str] = []
    
    corrections: List[CorrectionSchema] = []
    vocabulary_items: List[VocabularyFeedbackSchema] = []
    
    created_at: datetime


class EvaluationLLMStructuredOutput(BaseModel):
    overall_score: int
    fluency: int
    accuracy: int
    grammar: int
    vocabulary: int
    pronunciation_estimate: int
    comprehension: int
    sentence_formation: int
    naturalness: int
    conversation_relevance: int
    confidence_estimate: int
    estimated_cefr: str
    cefr_reasoning: str
    strengths: List[str]
    improvements: List[str]
    corrections: List[Dict[str, str]]
    vocabulary_feedback: List[Dict[str, str]]
    naturalness_tips: List[str]
    recommendations: List[str]
