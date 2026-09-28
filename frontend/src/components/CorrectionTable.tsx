import React from 'react';
import { Check, X, Sparkles, HelpCircle, BookOpen } from 'lucide-react';
import { Correction, VocabularyFeedback } from '../types';

interface CorrectionTableProps {
  corrections: Correction[];
  vocabularyItems: VocabularyFeedback[];
  naturalnessTips: string[];
}

export const CorrectionTable: React.FC<CorrectionTableProps> = ({
  corrections,
  vocabularyItems,
  naturalnessTips,
}) => {
  return (
    <div className="space-y-8">
      {/* 1. Grammatical Corrections Table */}
      <div className="card-sand p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-rose-100 text-rose-700 flex items-center justify-center font-bold">
              !
            </div>
            <div>
              <h3 className="text-base font-bold text-clay-900 font-serif">
                Detailed Speech Corrections
              </h3>
              <p className="text-xs text-clay-500">
                Grounded corrections extracted from your actual spoken sentences.
              </p>
            </div>
          </div>
          <span className="text-xs font-semibold px-2.5 py-1 bg-sand-200 text-clay-700 rounded-full">
            {corrections.length} {corrections.length === 1 ? 'Correction' : 'Corrections'}
          </span>
        </div>

        {corrections.length === 0 ? (
          <div className="text-center py-6 bg-sand-50 rounded-xl border border-dashed border-sand-300">
            <Check className="w-8 h-8 text-emerald-600 mx-auto mb-2" />
            <p className="text-sm font-bold text-clay-800">Excellent Grammar!</p>
            <p className="text-xs text-clay-500">No major grammatical slips detected in this session.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-sand-200 text-clay-500 uppercase tracking-wider font-semibold">
                  <th className="py-3 px-3">What You Said</th>
                  <th className="py-3 px-3">Better Version</th>
                  <th className="py-3 px-3">Issue & Category</th>
                  <th className="py-3 px-3">Explanation</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-sand-100">
                {corrections.map((item, idx) => (
                  <tr key={idx} className="hover:bg-sand-50/60 transition-colors">
                    {/* User Said */}
                    <td className="py-3.5 px-3 align-top font-medium text-rose-800 bg-rose-50/40 rounded-l-md">
                      <div className="flex items-start gap-1.5">
                        <X className="w-4 h-4 text-rose-500 shrink-0 mt-0.5" />
                        <span>"{item.user_said}"</span>
                      </div>
                    </td>

                    {/* Better Version */}
                    <td className="py-3.5 px-3 align-top font-bold text-emerald-900 bg-emerald-50/40">
                      <div className="flex items-start gap-1.5">
                        <Check className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                        <span>"{item.better_version}"</span>
                      </div>
                    </td>

                    {/* Issue Category */}
                    <td className="py-3.5 px-3 align-top">
                      <span className="inline-block px-2 py-0.5 rounded text-[11px] font-bold bg-amber-100 text-amber-900 border border-amber-200">
                        {item.category || item.issue}
                      </span>
                    </td>

                    {/* Explanation */}
                    <td className="py-3.5 px-3 align-top text-clay-600 leading-relaxed rounded-r-md">
                      {item.explanation}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* 2. Vocabulary Enhancement Table */}
      {vocabularyItems.length > 0 && (
        <div className="card-sand p-6">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-8 h-8 rounded-lg bg-teal-100 text-teal-700 flex items-center justify-center">
              <BookOpen className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-base font-bold text-clay-900 font-serif">
                Vocabulary Enhancement
              </h3>
              <p className="text-xs text-clay-500">
                More natural, vivid alternatives to elevate your everyday word choice.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {vocabularyItems.map((vocab, i) => (
              <div key={i} className="p-4 rounded-xl bg-sand-50 border border-sand-200 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold line-through text-clay-400">
                    "{vocab.word_used}"
                  </span>
                  <span className="text-xs font-bold px-2 py-0.5 rounded bg-terracotta-100 text-terracotta-800">
                    Use: {vocab.better_alternative}
                  </span>
                </div>
                <p className="text-xs text-clay-700 leading-relaxed">
                  <span className="font-semibold text-clay-900">Why:</span> {vocab.reason}
                </p>
                {vocab.example && (
                  <p className="text-xs text-clay-500 italic bg-white p-2 rounded-md border border-sand-200">
                    e.g. "{vocab.example}"
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 3. Naturalness & Idiomatic Tips */}
      {naturalnessTips.length > 0 && (
        <div className="card-sand p-6 bg-gradient-to-br from-terracotta-50/40 to-sand-50">
          <div className="flex items-center gap-2 mb-3">
            <Sparkles className="w-5 h-5 text-terracotta-600" />
            <h3 className="text-base font-bold text-clay-900 font-serif">
              Conversational Naturalness Tips
            </h3>
          </div>
          <ul className="space-y-2">
            {naturalnessTips.map((tip, idx) => (
              <li key={idx} className="flex items-start gap-2 text-xs text-clay-700 leading-relaxed">
                <span className="w-1.5 h-1.5 rounded-full bg-terracotta-500 mt-1.5 shrink-0" />
                <span>{tip}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
