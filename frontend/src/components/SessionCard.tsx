import React from 'react';
import { Link } from 'react-router-dom';
import { Clock, MessageSquare, Award, CheckCircle2, ChevronRight, Play } from 'lucide-react';
import { SessionSummary } from '../types';

interface SessionCardProps {
  session: SessionSummary;
}

export const SessionCard: React.FC<SessionCardProps> = ({ session }) => {
  const getDifficultyColor = (level: string) => {
    switch (level?.toUpperCase()) {
      case 'A1':
      case 'BEGINNER':
        return 'bg-emerald-100 text-emerald-800 border-emerald-200';
      case 'A2':
      case 'ELEMENTARY':
        return 'bg-teal-100 text-teal-800 border-teal-200';
      case 'B1':
      case 'INTERMEDIATE':
        return 'bg-amber-100 text-amber-800 border-amber-200';
      case 'B2':
      case 'UPPER INTERMEDIATE':
        return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'C1':
      case 'ADVANCED':
        return 'bg-rose-100 text-rose-800 border-rose-200';
      default:
        return 'bg-sand-200 text-clay-800 border-sand-300';
    }
  };

  return (
    <div className="card-sand card-sand-hover p-5 flex flex-col justify-between group">
      <div>
        {/* Header Badges */}
        <div className="flex items-center justify-between gap-2 mb-3">
          <span className={`text-[11px] font-bold px-2.5 py-0.5 rounded-full border ${getDifficultyColor(session.cefr_level || session.difficulty)}`}>
            {session.cefr_level} • {session.difficulty}
          </span>

          {session.is_completed && (
            <div className="flex items-center gap-1 text-emerald-600 text-xs font-semibold">
              <CheckCircle2 className="w-4 h-4" />
              <span>Completed</span>
            </div>
          )}
        </div>

        {/* Title & Description */}
        <h4 className="text-base font-bold text-clay-900 group-hover:text-terracotta-600 transition-colors font-serif">
          {session.title}
        </h4>
        <p className="text-xs text-clay-600 mt-1.5 line-clamp-2 leading-relaxed">
          {session.description}
        </p>
      </div>

      {/* Footer Metrics & Action */}
      <div className="mt-5 pt-4 border-t border-sand-200 flex items-center justify-between">
        <div className="flex items-center gap-3 text-xs text-clay-500 font-medium">
          <span className="flex items-center gap-1">
            <Clock className="w-3.5 h-3.5" />
            {session.estimated_duration}m
          </span>
          <span className="flex items-center gap-1">
            <MessageSquare className="w-3.5 h-3.5" />
            {session.target_turns} turns
          </span>
          {session.best_score !== null && session.best_score !== undefined && (
            <span className="flex items-center gap-1 text-terracotta-700 font-bold bg-terracotta-50 px-2 py-0.5 rounded-md border border-terracotta-200">
              <Award className="w-3.5 h-3.5" />
              {session.best_score}%
            </span>
          )}
        </div>

        <Link
          to={`/session/${session.id}`}
          className="flex items-center gap-1 px-3.5 py-1.5 rounded-lg bg-terracotta-600 hover:bg-terracotta-700 text-white text-xs font-semibold shadow-warm-sm transition-all group-hover:gap-1.5"
        >
          <span>{session.is_completed ? 'Practice Again' : 'Start'}</span>
          <ChevronRight className="w-3.5 h-3.5" />
        </Link>
      </div>
    </div>
  );
};
