import re
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.orm import Session as DBSession

from backend.app.models.attempt import SessionAttempt
from backend.app.models.conversation import ConversationTurn
from backend.app.models.evaluation import Evaluation
from backend.app.models.correction import Correction, VocabularyFeedback
from backend.app.models.settings import ProgressSnapshot
from backend.app.services.scoring_service import scoring_service

logger = logging.getLogger("angiyam.evaluation")


class EvaluationService:
    """
    Evaluates completed speaking sessions using real transcript evidence,
    calculates empirical CEFR scores, detects authentic grammar/syntax issues,
    and returns comprehensive reports in sub-second response time.
    """

    def analyze_real_corrections(self, user_turns: List[Dict[str, Any]]) -> Tuple[List[Dict[str, str]], List[Dict[str, str]], List[str]]:
        """
        Analyze the user's actual spoken utterances for genuine grammatical,
        prepositional, tense, article, and conversational naturalness issues.
        Returns (corrections_list, vocabulary_items, naturalness_tips).
        GUARANTEE: Only outputs real corrections for actual patterns present in the user's text.
        """
        corrections: List[Dict[str, str]] = []
        seen_issues = set()

        # Common rule-based checks on real user utterances
        rules = [
            # 1. Subject-Verb Agreement (Singular third person with bare verb)
            (
                r"\b(he|she|it)\s+(go)\b",
                "he/she goes",
                "Subject-Verb Agreement",
                "Singular third-person subjects ('he', 'she', 'it') take the verb form 'goes'.",
                "Grammar"
            ),
            (
                r"\b(he|she|it)\s+(don't)\b",
                "doesn't",
                "Subject-Verb Agreement",
                "Use 'doesn't' (does not) with third-person singular subjects ('he', 'she', 'it').",
                "Grammar"
            ),
            (
                r"\b(he|she|it)\s+(have)\b",
                "has",
                "Subject-Verb Agreement",
                "Use 'has' with third-person singular subjects ('he', 'she', 'it').",
                "Grammar"
            ),
            (
                r"\b(i)\s+(has)\b",
                "I have",
                "Subject-Verb Agreement",
                "The first-person pronoun 'I' pairs with 'have', not 'has'.",
                "Grammar"
            ),
            (
                r"\b(they|we|you)\s+(is|was)\b",
                "are / were",
                "Subject-Verb Agreement",
                "Plural pronouns ('they', 'we', 'you') require plural verb forms ('are' or 'were').",
                "Grammar"
            ),
            
            # 2. Preposition & Collocation Errors
            (
                r"\b(working|living|staying|studying)?(?:\s+\w+)?\s+from\s+(\d+|two|three|four|five|several|many|a\s+few)\s+(years?|months?|days?|weeks?)\b",
                r"for \2 \3",
                "Preposition of Duration",
                "Use 'for' to indicate the duration of an ongoing period (e.g., 'for 2 years'), rather than 'from'.",
                "Preposition"
            ),
            (
                r"\b(listen)\s+(music|songs?|to\s+songs?|him|her|them)\b",
                r"listen to \2",
                "Missing Preposition",
                "'Listen' requires the preposition 'to' before its object (e.g., 'listen to music').",
                "Preposition"
            ),
            (
                r"\b(good|bad|expert)\s+in\s+(speaking|english|coding|sports|writing)\b",
                r"good at \2",
                "Preposition Collocation",
                "When expressing proficiency or skill, use 'good at' instead of 'good in'.",
                "Preposition"
            ),
            (
                r"\b(discuss|discussing)\s+about\b",
                r"\1",
                "Redundant Preposition",
                "'Discuss' is a transitive verb that directly takes an object without 'about' (e.g., 'discuss the project').",
                "Preposition"
            ),
            (
                r"\b(cope\s+up\s+with)\b",
                "cope with",
                "Redundant Particle",
                "The standard English idiom is 'cope with', not 'cope up with'.",
                "Idiom & Phrasing"
            ),
            (
                r"\b(revert\s+back)\b",
                "revert / reply",
                "Redundancy",
                "'Revert' already means to return or reply; 'revert back' is redundant. Use 'reply' or 'get back to you'.",
                "Phrasing"
            ),
            (
                r"\b(out\s+of\s+station)\b",
                "out of town / away",
                "Regional Phrasing",
                "In global professional contexts, use 'out of town' or 'away on travel' instead of 'out of station'.",
                "Naturalness"
            ),
            
            # 3. Double Past Tense / Auxiliary Form
            (
                r"\b(didn't|did\s+not)\s+(knew|went|saw|came|had|bought|told|took|spoke)\b",
                "did not + base verb",
                "Past Tense Auxiliary",
                "After auxiliary 'did not' or 'didn't', always use the base form of the verb (e.g., 'didn't know', 'didn't go').",
                "Grammar"
            ),
            
            # 4. Articles and Quantifiers
            (
                r"\b(a)\s+(apple|elephant|interview|opportunity|engineer|hour|email|order|application)\b",
                r"an \2",
                "Indefinite Article",
                "Use 'an' before words starting with a vowel sound.",
                "Grammar"
            ),
            (
                r"\b(an)\s+(university|user|useful|unique|uniform)\b",
                r"a \2",
                "Indefinite Article",
                "Words like 'university' begin with a consonant 'yu' sound, so use 'a' instead of 'an'.",
                "Grammar"
            ),
            (
                r"\b(informations|furnitures|feedbacks|equipments|advices)\b",
                "uncountable noun",
                "Uncountable Nouns",
                "Nouns like 'information', 'feedback', and 'equipment' are uncountable and do not take plural '-s'. Use 'some feedback' or 'pieces of equipment'.",
                "Vocabulary"
            ),
            
            # 5. Missing Auxiliary Verb
            (
                r"\b(i)\s+(working|going|planning|looking)\b",
                r"I am \2",
                "Missing Auxiliary Verb",
                "Continuous actions require the auxiliary verb 'am' (e.g., 'I am working').",
                "Grammar"
            ),
            (
                r"\b(he|she)\s+(working|going|planning|looking)\b",
                r"\1 is \2",
                "Missing Auxiliary Verb",
                "Present continuous tense requires 'is' before the '-ing' verb (e.g., 'he is working').",
                "Grammar"
            ),
            (
                r"\b(we|they)\s+(working|going|planning|looking)\b",
                r"\1 are \2",
                "Missing Auxiliary Verb",
                "Plural continuous tense requires 'are' before the '-ing' verb (e.g., 'they are working').",
                "Grammar"
            ),
            
            # 6. Naturalness & Hospitality / Conversational Collocations
            (
                r"\b(i\s+want\s+room|give\s+me\s+room)\b",
                "I would like to check into my room, please.",
                "Politeness & Naturalness",
                "Using polite modals like 'I would like to check in...' sounds much more natural and professional in hospitality situations.",
                "Naturalness"
            ),
            (
                r"\b(give\s+me\s+the\s+bill|bring\s+bill)\b",
                "Could we please have the bill?",
                "Polite Request Phrasing",
                "Phrasing requests as questions with 'Could I please have...' sounds cordial and natural.",
                "Naturalness"
            ),
            (
                r"\b(myself\s+[A-Za-z]+)\b",
                "My name is / I am",
                "Self-Introduction",
                "Avoid introducing yourself with 'Myself...'. Use 'I am [Name]' or 'My name is [Name]'.",
                "Naturalness"
            ),
        ]

        # Scan each user utterance against rules
        for turn in user_turns:
            raw_text = turn.get("transcript", "").strip()
            if not raw_text or raw_text.startswith("["):
                continue

            for pattern, better_replacement, issue_title, explanation, category in rules:
                match = re.search(pattern, raw_text, re.IGNORECASE)
                if match and issue_title not in seen_issues:
                    seen_issues.add(issue_title)
                    matched_str = match.group(0)
                    
                    # Generate improved version of the sentence
                    if callable(better_replacement):
                        better_text = re.sub(pattern, better_replacement, raw_text, count=1, flags=re.IGNORECASE)
                    elif "\\" in better_replacement:
                        better_text = re.sub(pattern, better_replacement, raw_text, count=1, flags=re.IGNORECASE)
                    else:
                        better_text = raw_text.replace(matched_str, better_replacement)

                    corrections.append({
                        "user_said": raw_text,
                        "better_version": better_text,
                        "issue": issue_title,
                        "explanation": explanation,
                        "category": category
                    })

        # Vocabulary enhancement items based on words actually spoken by user
        all_user_words = " ".join([t.get("transcript", "") for t in user_turns]).lower()
        vocab_suggestions_map = [
            ("good", "exceptional / pleasant", "Expands descriptive quality beyond basic adjectives.", "The service was exceptional and very pleasant."),
            ("bad", "sub-optimal / unfavorable", "Adds nuance to critical feedback.", "The weather conditions were unfavorable today."),
            ("happy", "delighted / thrilled", "Conveys vivid emotion in casual and professional dialog.", "I was thrilled to hear about the opportunity."),
            ("problem", "challenge / obstacle", "Frames difficulties constructively in professional conversations.", "We encountered a minor technical challenge."),
            ("big", "substantial / extensive", "Provides precise scale in descriptions.", "We made substantial progress on the deliverable."),
            ("nice", "agreeable / charming", "Enriches descriptive vocabulary.", "It was a very agreeable and charming venue."),
            ("help", "assist / facilitate", "Offers polished phrasing in business contexts.", "I would be happy to facilitate the discussion."),
            ("like", "prefer / appreciate", "Expresses preferences with greater elegance.", "I would appreciate a quiet workspace on the 4th floor.")
        ]

        vocabulary_items: List[Dict[str, str]] = []
        for word, better, reason, example in vocab_suggestions_map:
            if re.search(rf"\b{word}\b", all_user_words, re.IGNORECASE):
                vocabulary_items.append({
                    "word_used": word,
                    "better_alternative": better,
                    "reason": reason,
                    "example": example
                })
                if len(vocabulary_items) >= 3:
                    break

        # Naturalness tips
        naturalness_tips = [
            "Use modal verbs like 'Could you please...' or 'Would it be possible...' for polite requests.",
            "Incorporate linking phrases like 'Furthermore', 'On the other hand', and 'As a result' to connect multi-sentence ideas.",
            "Pause slightly instead of using filler sounds like 'uh' or 'um' to project confidence."
        ]

        return corrections, vocabulary_items, naturalness_tips

    def evaluate_attempt(self, db: DBSession, attempt_id: int) -> Evaluation:
        """Evaluate an attempt and return the persisted Evaluation record with sub-second execution."""
        existing = db.query(Evaluation).filter(Evaluation.attempt_id == attempt_id).first()
        if existing:
            return existing

        attempt = db.query(SessionAttempt).filter(SessionAttempt.id == attempt_id).first()
        if not attempt:
            raise ValueError(f"Attempt {attempt_id} not found.")

        session = attempt.session
        turns = (
            db.query(ConversationTurn)
            .filter(ConversationTurn.attempt_id == attempt.id)
            .order_by(ConversationTurn.turn_index.asc())
            .all()
        )

        user_turns = [
            {
                "speaker": t.speaker,
                "transcript": t.transcript,
                "audio_duration": t.audio_duration,
                "confidence": t.confidence,
                "filler_count": t.filler_count
            }
            for t in turns if t.speaker == "user" and t.transcript and not t.transcript.startswith("[")
        ]

        # 1. Compute accurate empirical metrics
        stats = scoring_service.calculate_turn_metrics(user_turns)
        metrics = scoring_service.calculate_fallback_metrics(stats, session.cefr_level if session else "B1")

        # 2. Analyze real corrections on user's actual speech
        corrections_list, vocab_list, naturalness_tips = self.analyze_real_corrections(user_turns)

        # Adjust grammar score if genuine grammatical errors were detected
        grammar_score = metrics["grammar"]
        if corrections_list:
            deduction = min(len(corrections_list) * 5, 20)
            grammar_score = max(50, grammar_score - deduction)
            accuracy_score = max(52, metrics["accuracy"] - deduction // 2)
        else:
            accuracy_score = metrics["accuracy"]

        overall_score = int((metrics["fluency"] + grammar_score + metrics["vocabulary"] + metrics["comprehension"] + metrics["naturalness"]) / 5)

        # 3. Dynamic Strengths & Areas for Improvement based on actual performance
        strengths = []
        improvements = []

        if stats["turn_count"] > 0:
            strengths.append(f"Successfully completed {stats['turn_count']} interactive conversation turns with prompt responses")
        if stats["avg_response_words"] >= 10:
            strengths.append(f"Demonstrated good phrase length with an average of {stats['avg_response_words']} words per turn")
        elif stats["avg_response_words"] > 0:
            strengths.append("Maintained clear and concise dialogue responses")

        if stats["filler_rate"] < 2.0:
            strengths.append("Excellent speech cleanliness with minimal filler word usage")
        else:
            improvements.append(f"Work on reducing filler word frequency (currently {stats['filler_rate']} fillers/min)")

        if corrections_list:
            improvements.append("Review detected grammar patterns (subject-verb agreement and prepositions) for enhanced precision")
        else:
            strengths.append("Maintained strong grammatical accuracy with no major structural mistakes")

        if stats["avg_response_words"] < 10:
            improvements.append("Try elaborating on your points by adding a reason or example to each response")

        if not improvements:
            improvements.append("Continue practicing varied conversational topics to further broaden idiomatic fluency")

        recommendations = [
            f"Practice similar real-life scenarios in {session.unit.title if session and session.unit else 'this unit'} to solidify confidence.",
            "Focus on smooth sentence transitions without filler pauses.",
            "Repeat this scenario to practice the suggested vocabulary enhancements."
        ]

        # 4. Save Evaluation Record
        evaluation = Evaluation(
            attempt_id=attempt.id,
            overall_score=overall_score,
            fluency=metrics["fluency"],
            accuracy=accuracy_score,
            grammar=grammar_score,
            vocabulary=metrics["vocabulary"],
            pronunciation_estimate=metrics["pronunciation_estimate"],
            comprehension=metrics["comprehension"],
            sentence_formation=int((grammar_score + accuracy_score) / 2),
            naturalness=metrics["naturalness"],
            conversation_relevance=metrics["conversation_relevance"],
            confidence_estimate=metrics["confidence_estimate"],
            estimated_cefr=metrics["estimated_cefr"],
            cefr_reasoning=metrics["cefr_reasoning"],
            total_speaking_time=stats["total_speaking_time"],
            turn_count=stats["turn_count"],
            avg_response_words=stats["avg_response_words"],
            filler_count=stats["total_fillers"],
            filler_rate=stats["filler_rate"],
            most_used_filler=stats["most_used_filler"],
            filler_breakdown=stats["filler_breakdown"],
            repetition_analysis=stats["repetition_analysis"],
            strengths=strengths,
            improvements=improvements,
            naturalness_tips=naturalness_tips,
            recommendations=recommendations,
            raw_analysis_json={"status": "complete", "analyzed_turns": len(user_turns)}
        )
        db.add(evaluation)
        db.flush()

        # 5. Save Real Corrections
        for c in corrections_list:
            corr = Correction(
                evaluation_id=evaluation.id,
                user_said=c.get("user_said", ""),
                better_version=c.get("better_version", ""),
                issue=c.get("issue", "Grammar"),
                explanation=c.get("explanation", ""),
                category=c.get("category", "Grammar")
            )
            db.add(corr)

        # 6. Save Vocabulary Feedback
        for v in vocab_list:
            v_item = VocabularyFeedback(
                evaluation_id=evaluation.id,
                word_used=v.get("word_used", ""),
                better_alternative=v.get("better_alternative", ""),
                reason=v.get("reason", ""),
                example=v.get("example", "")
            )
            db.add(v_item)

        # 7. Update progress snapshot
        self._record_progress_snapshot(db, evaluation)

        db.commit()
        db.refresh(evaluation)
        logger.info(f"[Evaluation] Completed sub-second evaluation for attempt {attempt_id} (Score: {overall_score}, CEFR: {metrics['estimated_cefr']})")
        return evaluation

    def _record_progress_snapshot(self, db: DBSession, latest_eval: Evaluation):
        """Record overall progress snapshot for analytics."""
        all_evals = db.query(Evaluation).all()
        total_evals = len(all_evals)
        avg_score = int(sum(e.overall_score for e in all_evals) / max(1, total_evals))
        fluency_avg = int(sum(e.fluency for e in all_evals) / max(1, total_evals))
        grammar_avg = int(sum(e.grammar for e in all_evals) / max(1, total_evals))
        vocab_avg = int(sum(e.vocabulary for e in all_evals) / max(1, total_evals))
        total_seconds = int(sum(e.total_speaking_time for e in all_evals))

        snapshot = ProgressSnapshot(
            timestamp=datetime.utcnow(),
            total_speaking_time=total_seconds,
            total_sessions_completed=total_evals,
            current_estimated_cefr=latest_eval.estimated_cefr,
            avg_score=avg_score,
            fluency_avg=fluency_avg,
            grammar_avg=grammar_avg,
            vocab_avg=vocab_avg
        )
        db.add(snapshot)


evaluation_service = EvaluationService()
