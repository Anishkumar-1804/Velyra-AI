import React from 'react';
import { Award, Zap, BookOpen, MessageCircle, Volume2, ShieldCheck, HelpCircle } from 'lucide-react';

interface MetricItem {
  label: string;
  score: number;
  icon: React.ElementType;
  description: string;
  isEstimate?: boolean;
}

interface MetricsCardProps {
  overallScore: number;
  cefrLevel: string;
  cefrReasoning?: string;
  metrics: {
    fluency: number;
    accuracy: number;
    grammar: number;
    vocabulary: number;
    pronunciation: number;
    comprehension: number;
    naturalness: number;
  };
}

export const MetricsCard: React.FC<MetricsCardProps> = ({
  overallScore,
  cefrLevel,
  cefrReasoning,
  metrics,
}) => {
  const metricList: MetricItem[] = [
    { label: 'Fluency', score: metrics.fluency, icon: Zap, description: 'Speaking pace, flow, and continuous sentence delivery.' },
    { label: 'Grammar Accuracy', score: metrics.grammar, icon: ShieldCheck, description: 'Proper tense usage, prepositions, and grammatical structure.' },
    { label: 'Vocabulary Variety', score: metrics.vocabulary, icon: BookOpen, description: 'Use of descriptive, appropriate contextual words.' },
    { label: 'Pronunciation (AI Estimate)', score: metrics.pronunciation, icon: Volume2, description: 'Phonetic clarity approximation based on acoustic transcription.', isEstimate: true },
    { label: 'Comprehension', score: metrics.comprehension, icon: MessageCircle, description: 'Understanding of the scenario prompts and context.' },
    { label: 'Naturalness', score: metrics.naturalness, icon: Award, description: 'Polite, idiomatic conversational expressions.' },
  ];

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'bg-emerald-500';
    if (score >= 65) return 'bg-amber-500';
    return 'bg-rose-500';
  };

  return (
    <div className="card-sand p-6 lg:p-8">
      {/* Overall Score Header */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-6 pb-6 border-b border-sand-200">
        <div className="flex items-center gap-5">
          <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-terracotta-500 to-terracotta-700 flex flex-col items-center justify-center text-white shadow-warm-md">
            <span className="text-3xl font-extrabold tracking-tight font-serif">{overallScore}</span>
            <span className="text-[10px] uppercase font-bold tracking-widest text-terracotta-100">/ 100</span>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs uppercase font-bold tracking-widest text-clay-500">Speaking Level</span>
              <span className="px-2.5 py-0.5 rounded-md bg-clay-900 text-sand-50 font-bold text-xs tracking-wider">
                CEFR {cefrLevel}
              </span>
            </div>
            <h3 className="text-xl font-bold text-clay-900 mt-1 font-serif">
              {cefrLevel === 'C1' ? 'Advanced Speaker' :
               cefrLevel === 'B2' ? 'Upper Intermediate' :
               cefrLevel === 'B1' ? 'Independent Speaker' :
               cefrLevel === 'A2' ? 'Elementary Speaker' : 'Beginner Speaker'}
            </h3>
            {cefrReasoning && (
              <p className="text-xs text-clay-600 mt-1 max-w-lg leading-relaxed">
                "{cefrReasoning}"
              </p>
            )}
          </div>
        </div>

        <div className="text-center sm:text-right">
          <span className="text-xs font-semibold text-emerald-700 bg-emerald-50 px-3 py-1.5 rounded-full border border-emerald-200">
            Evidence-Based Evaluation
          </span>
        </div>
      </div>

      {/* 6 Metric Breakdown Bars */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-5 mt-6">
        {metricList.map((m) => {
          const Icon = m.icon;
          return (
            <div key={m.label} className="space-y-1.5">
              <div className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-1.5 font-bold text-clay-800">
                  <Icon className="w-4 h-4 text-terracotta-600" />
                  <span>{m.label}</span>
                </div>
                <span className="font-extrabold text-clay-900 text-sm">{m.score}%</span>
              </div>

              {/* Progress Bar */}
              <div className="w-full bg-sand-200 h-2.5 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-700 ${getScoreColor(m.score)}`}
                  style={{ width: `${m.score}%` }}
                />
              </div>

              <p className="text-[11px] text-clay-500 flex items-center justify-between">
                <span>{m.description}</span>
                {m.isEstimate && (
                  <span className="text-[10px] text-clay-400 italic">Approx.</span>
                )}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
};
