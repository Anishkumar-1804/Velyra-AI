import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import confetti from 'canvas-confetti';
import {
  Award,
  CheckCircle2,
  TrendingUp,
  RotateCcw,
  ChevronRight,
  ArrowRight,
  Sparkles,
  Target,
  BookOpen
} from 'lucide-react';
import { api } from '../services/api';
import { EvaluationReport, SessionDetail } from '../types';
import { MetricsCard } from '../components/MetricsCard';
import { CorrectionTable } from '../components/CorrectionTable';
import { FillerChart } from '../components/FillerChart';

export const ResultsPage: React.FC = () => {
  const { id, attemptId } = useParams<{ id: string; attemptId: string }>();
  const navigate = useNavigate();

  const [evaluation, setEvaluation] = useState<EvaluationReport | null>(null);
  const [session, setSession] = useState<SessionDetail | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchResults = async () => {
      if (!attemptId || !id) return;
      try {
        const [evalData, sessionData] = await Promise.all([
          api.getEvaluation(Number(attemptId)),
          api.getSessionDetail(Number(id)),
        ]);
        setEvaluation(evalData);
        setSession(sessionData);

        // Confetti celebration if user scored well
        if (evalData.overall_score >= 70) {
          confetti({
            particleCount: 80,
            spread: 60,
            origin: { y: 0.6 },
            colors: ['#C85A32', '#B54823', '#F6D7CB', '#10B981'],
          });
        }
      } catch (err) {
        console.error('Error loading evaluation report:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchResults();
  }, [id, attemptId]);

  if (loading) {
    return (
      <div className="py-24 text-center space-y-4">
        <Sparkles className="w-10 h-10 text-terracotta-600 animate-spin mx-auto" />
        <h2 className="text-xl font-bold text-clay-900 font-serif">Analyzing Your Speech...</h2>
        <p className="text-xs text-clay-500">Evaluating grammar accuracy, fluency, filler frequency, and naturalness.</p>
      </div>
    );
  }

  if (!evaluation || !session) {
    return (
      <div className="py-20 text-center text-clay-500">
        Evaluation report not found.
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* 1. Header Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3.5">
          <div className="w-12 h-12 rounded-2xl overflow-hidden bg-sand-100 flex items-center justify-center shrink-0 border border-sand-300 shadow-warm-sm">
            <img src="/logo.png" alt="KuralMozhi.ai" className="w-full h-full object-cover" />
          </div>
          <div>
            <span className="text-xs font-bold uppercase tracking-widest text-terracotta-600">
              Session Report
            </span>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-clay-900 mt-0.5 font-serif">
              {session.title}
            </h1>
            <p className="text-xs text-clay-500 mt-0.5">
              Target CEFR: {session.cefr_level} • Completed across {evaluation.turn_count} speech turns ({Math.round(evaluation.total_speaking_time)}s speaking time)
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Link
            to={`/session/${session.id}/live`}
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-sand-200 hover:bg-sand-300 text-clay-800 text-xs font-bold transition-all"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Repeat Session</span>
          </Link>

          <Link
            to={`/unit/${session.unit_id}`}
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-terracotta-600 hover:bg-terracotta-700 text-white text-xs font-bold shadow-warm-sm transition-all"
          >
            <span>Next Scenario</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>

      {/* 2. Core Metrics & CEFR Level Card */}
      <MetricsCard
        overallScore={evaluation.overall_score}
        cefrLevel={evaluation.estimated_cefr}
        cefrReasoning={evaluation.cefr_reasoning}
        metrics={{
          fluency: evaluation.fluency,
          accuracy: evaluation.accuracy,
          grammar: evaluation.grammar,
          vocabulary: evaluation.vocabulary,
          pronunciation: evaluation.pronunciation_estimate,
          comprehension: evaluation.comprehension,
          naturalness: evaluation.naturalness,
        }}
      />

      {/* 3. Strengths & Improvements Highlights */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Strengths */}
        <div className="card-sand p-6 bg-emerald-50/30 border-emerald-200/60">
          <div className="flex items-center gap-2 mb-4">
            <CheckCircle2 className="w-5 h-5 text-emerald-600" />
            <h3 className="text-base font-bold text-clay-900 font-serif">
              What You Did Well
            </h3>
          </div>
          <ul className="space-y-2.5">
            {evaluation.strengths.map((point, i) => (
              <li key={i} className="flex items-start gap-2 text-xs text-clay-800 leading-relaxed">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 mt-1.5 shrink-0" />
                <span>{point}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Areas to Improve */}
        <div className="card-sand p-6 bg-amber-50/30 border-amber-200/60">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp className="w-5 h-5 text-amber-600" />
            <h3 className="text-base font-bold text-clay-900 font-serif">
              Areas to Strengthen
            </h3>
          </div>
          <ul className="space-y-2.5">
            {evaluation.improvements.map((point, i) => (
              <li key={i} className="flex items-start gap-2 text-xs text-clay-800 leading-relaxed">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-500 mt-1.5 shrink-0" />
                <span>{point}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* 4. Detailed Speech Corrections & Vocabulary Table */}
      <CorrectionTable
        corrections={evaluation.corrections}
        vocabularyItems={evaluation.vocabulary_items}
        naturalnessTips={evaluation.naturalness_tips}
      />

      {/* 5. Filler Words and Repetition Analysis */}
      <FillerChart
        totalFillers={evaluation.filler_count}
        fillerRate={evaluation.filler_rate}
        mostUsedFiller={evaluation.most_used_filler}
        fillerBreakdown={evaluation.filler_breakdown || {}}
        repetitionAnalysis={evaluation.repetition_analysis || {}}
        totalSpeakingTime={evaluation.total_speaking_time}
      />

      {/* 6. Recommendations & Action Footer */}
      {evaluation.recommendations.length > 0 && (
        <div className="card-sand p-6 bg-gradient-to-br from-sand-100 to-terracotta-50/50 border border-sand-300">
          <div className="flex items-center gap-2 mb-3">
            <Target className="w-5 h-5 text-terracotta-600" />
            <h3 className="text-base font-bold text-clay-900 font-serif">
              Recommended Next Practice
            </h3>
          </div>
          <ul className="space-y-2 mb-6">
            {evaluation.recommendations.map((rec, i) => (
              <li key={i} className="text-xs text-clay-700 leading-relaxed flex items-start gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-terracotta-600 mt-1.5 shrink-0" />
                <span>{rec}</span>
              </li>
            ))}
          </ul>

          <div className="flex flex-wrap items-center gap-3">
            <Link
              to={`/session/${session.id}/live`}
              className="px-5 py-2.5 rounded-xl bg-sand-200 hover:bg-sand-300 text-clay-800 text-xs font-bold transition-colors"
            >
              Repeat Scenario
            </Link>

            <Link
              to={`/unit/${session.unit_id}`}
              className="px-6 py-2.5 rounded-xl bg-terracotta-600 hover:bg-terracotta-700 text-white text-xs font-bold shadow-warm-sm transition-colors"
            >
              Continue to Next Scenario →
            </Link>

            <Link
              to="/progress"
              className="px-5 py-2.5 rounded-xl bg-white hover:bg-sand-50 text-clay-800 text-xs font-semibold border border-sand-300 transition-colors"
            >
              View Full Progress
            </Link>
          </div>
        </div>
      )}
    </div>
  );
};
