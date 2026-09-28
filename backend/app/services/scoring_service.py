import re
from typing import List, Dict, Any, Tuple
from backend.app.utils.audio import detect_filler_words, detect_repeated_words_and_phrases


class ScoringService:
    """
    Computes evidence-based mathematical and linguistic scores from actual transcripts and timing metrics.
    """
    def calculate_turn_metrics(self, user_turns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate statistical aggregates over all user utterances."""
        total_words = 0
        total_speaking_time = 0.0
        total_fillers = 0
        filler_breakdown: Dict[str, int] = {}
        all_user_text = []

        for turn in user_turns:
            text = turn.get("transcript", "")
            duration = turn.get("audio_duration", 0.0)
            
            words = text.split()
            total_words += len(words)
            total_speaking_time += duration
            all_user_text.append(text)

            _, _, breakdown = detect_filler_words(text)
            for k, v in breakdown.items():
                filler_breakdown[k] = filler_breakdown.get(k, 0) + v
                total_fillers += v

        full_speech = " ".join(all_user_text)
        repetition_dict = detect_repeated_words_and_phrases(full_speech)
        
        turn_count = len(user_turns)
        avg_response_words = round(total_words / max(1, turn_count), 1)
        
        # Filler rate per minute
        speaking_minutes = max(0.2, total_speaking_time / 60.0)
        filler_rate = round(total_fillers / speaking_minutes, 1)

        most_used_filler = max(filler_breakdown, key=filler_breakdown.get) if filler_breakdown else "None"

        return {
            "total_words": total_words,
            "turn_count": turn_count,
            "total_speaking_time": round(total_speaking_time, 1),
            "avg_response_words": avg_response_words,
            "total_fillers": total_fillers,
            "filler_rate": filler_rate,
            "most_used_filler": most_used_filler,
            "filler_breakdown": filler_breakdown,
            "repetition_analysis": repetition_dict,
            "full_text": full_speech
        }

    def estimate_cefr_level(
        self,
        avg_words_per_turn: float,
        grammar_score: int,
        vocab_score: int,
        fluency_score: int
    ) -> Tuple[str, str]:
        """Estimate CEFR Level based on empirical metrics."""
        composite = (grammar_score * 0.35) + (vocab_score * 0.35) + (fluency_score * 0.30)
        
        if composite >= 88 and avg_words_per_turn >= 18:
            return "C1", "You speak with great fluency, sophisticated vocabulary, and natural conversational flow."
        elif composite >= 78 and avg_words_per_turn >= 12:
            return "B2", "You communicate effectively with strong sentence structures and good vocabulary variety."
        elif composite >= 65:
            return "B1", "You can comfortably maintain everyday conversations and explain experiences with basic accuracy."
        elif composite >= 50:
            return "A2", "You can express routine ideas and respond to direct questions, with developing vocabulary."
        else:
            return "A1", "You are building initial speaking confidence with simple words and short phrases."

    def calculate_fallback_metrics(self, stats: Dict[str, Any], target_level: str) -> Dict[str, Any]:
        """Calculate grounded baseline scores when LLM evaluation fails."""
        turn_count = stats["turn_count"]
        avg_words = stats["avg_response_words"]
        filler_rate = stats["filler_rate"]

        # Fluency: higher with more words per turn, lower with high filler rate
        base_fluency = min(92, max(50, int(55 + avg_words * 2.2 - filler_rate * 2.5)))
        
        # Accuracy & Grammar estimates
        base_accuracy = min(88, max(55, int(60 + min(turn_count * 4, 25))))
        base_grammar = min(86, max(52, int(58 + min(turn_count * 3, 24))))
        base_vocab = min(90, max(55, int(56 + avg_words * 2.0)))
        
        pronunciation = min(85, max(60, int((base_fluency + base_accuracy) / 2)))
        comprehension = min(92, max(65, int(70 + min(turn_count * 3.5, 22))))
        naturalness = min(88, max(50, int(base_fluency * 0.5 + base_vocab * 0.5)))
        relevance = min(95, max(70, int(80 + min(turn_count * 2.5, 15))))
        confidence = min(90, max(55, int(base_fluency * 0.6 + comprehension * 0.4)))

        overall = int((base_fluency + base_grammar + base_vocab + comprehension + naturalness) / 5)
        cefr, reasoning = self.estimate_cefr_level(avg_words, base_grammar, base_vocab, base_fluency)

        return {
            "overall_score": overall,
            "fluency": base_fluency,
            "accuracy": base_accuracy,
            "grammar": base_grammar,
            "vocabulary": base_vocab,
            "pronunciation_estimate": pronunciation,
            "comprehension": comprehension,
            "sentence_formation": int((base_grammar + base_accuracy) / 2),
            "naturalness": naturalness,
            "conversation_relevance": relevance,
            "confidence_estimate": confidence,
            "estimated_cefr": cefr,
            "cefr_reasoning": reasoning
        }


scoring_service = ScoringService()
