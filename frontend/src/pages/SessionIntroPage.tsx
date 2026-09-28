import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import {
  ArrowLeft,
  Clock,
  MessageSquare,
  Award,
  Target,
  User,
  Bot,
  Sparkles,
  BookOpen,
  Mic
} from 'lucide-react';
import { api } from '../services/api';
import { SessionDetail } from '../types';

export const SessionIntroPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [session, setSession] = useState<SessionDetail | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSession = async () => {
      if (!id) return;
      try {
        const data = await api.getSessionDetail(Number(id));
        setSession(data);
      } catch (err) {
        console.error('Error fetching session:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchSession();
  }, [id]);

  if (loading) {
    return <div className="py-20 text-center text-clay-500">Loading session briefing...</div>;
  }

  if (!session) {
    return <div className="py-20 text-center text-clay-500">Session not found.</div>;
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Breadcrumbs */}
      <div className="flex items-center gap-2 text-xs font-semibold text-clay-500">
        <Link to="/genres" className="hover:text-clay-900">Genres</Link>
        <span>/</span>
        <Link to={`/unit/${session.unit_id}`} className="hover:text-clay-900 flex items-center gap-1">
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>{session.unit_title}</span>
        </Link>
        <span>/</span>
        <span className="text-clay-900 font-bold">{session.title}</span>
      </div>

      {/* Main Header Briefing Card */}
      <div className="card-sand p-8 space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <span className="text-xs font-bold px-3 py-1 rounded-full bg-terracotta-100 text-terracotta-800 border border-terracotta-200">
            CEFR {session.cefr_level} • {session.difficulty}
          </span>
          <div className="flex items-center gap-4 text-xs font-medium text-clay-500">
            <span className="flex items-center gap-1.5">
              <Clock className="w-4 h-4 text-terracotta-600" />
              ~{session.estimated_duration} Minutes
            </span>
            <span className="flex items-center gap-1.5">
              <MessageSquare className="w-4 h-4 text-terracotta-600" />
              ~{session.target_turns} Conversational Turns
            </span>
          </div>
        </div>

        <div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-clay-900 font-serif">
            {session.title}
          </h1>
          <p className="text-sm sm:text-base text-clay-700 mt-2 leading-relaxed">
            {session.description}
          </p>
        </div>

        {/* Scenario Box */}
        <div className="p-5 rounded-2xl bg-sand-100/70 border border-sand-200 space-y-3">
          <span className="text-xs font-bold uppercase tracking-wider text-terracotta-700 block">
            The Situation / Scenario
          </span>
          <p className="text-sm text-clay-900 font-medium leading-relaxed">
            "{session.scenario}"
          </p>
        </div>

        {/* Roles Breakdown */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="p-4 rounded-xl bg-sand-50 border border-sand-200 flex items-start gap-3 shadow-warm-xs">
            <div className="w-10 h-10 rounded-xl overflow-hidden bg-sand-100 flex items-center justify-center shrink-0 border border-sand-300">
              <img src="/logo.png" alt="AI Partner" className="w-full h-full object-cover" />
            </div>
            <div>
              <span className="text-xs font-bold text-clay-500 uppercase">AI Partner Role</span>
              <p className="text-sm font-bold text-clay-900 mt-0.5">{session.ai_role}</p>
            </div>
          </div>

          <div className="p-4 rounded-xl bg-sand-50 border border-sand-200 flex items-start gap-3">
            <div className="w-10 h-10 rounded-xl bg-clay-800 text-white flex items-center justify-center shrink-0">
              <User className="w-5 h-5" />
            </div>
            <div>
              <span className="text-xs font-bold text-clay-500 uppercase">Your Role</span>
              <p className="text-sm font-bold text-clay-900 mt-0.5">{session.user_role}</p>
            </div>
          </div>
        </div>

        {/* Learning Objectives */}
        <div className="space-y-3 pt-2">
          <div className="flex items-center gap-2">
            <Target className="w-4 h-4 text-terracotta-600" />
            <h3 className="text-sm font-bold text-clay-900 font-serif">Learning Objectives</h3>
          </div>
          <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {session.learning_objectives.map((obj, i) => (
              <li key={i} className="flex items-start gap-2 text-xs text-clay-700 bg-sand-50/80 p-2.5 rounded-lg border border-sand-200">
                <span className="w-1.5 h-1.5 rounded-full bg-terracotta-500 mt-1.5 shrink-0" />
                <span>{obj}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Suggested Vocabulary */}
        {session.suggested_vocabulary && session.suggested_vocabulary.length > 0 && (
          <div className="space-y-3 pt-2">
            <div className="flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-terracotta-600" />
              <h3 className="text-sm font-bold text-clay-900 font-serif">Helpful Vocabulary Hints</h3>
            </div>
            <div className="flex flex-wrap gap-2">
              {session.suggested_vocabulary.map((word, i) => (
                <span
                  key={i}
                  className="px-3 py-1 rounded-lg text-xs font-semibold bg-clay-100 text-clay-800 border border-sand-300"
                >
                  {word}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Action Button */}
        <div className="pt-6 border-t border-sand-200 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs text-clay-500">
            Speak naturally through your microphone when the session begins.
          </p>

          <Link
            to={`/session/${session.id}/live`}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-4 rounded-xl bg-terracotta-600 hover:bg-terracotta-700 text-white font-bold text-base shadow-warm-md hover:shadow-glow-terracotta transition-all hover:scale-105 active:scale-95"
          >
            <Mic className="w-5 h-5" />
            <span>Start Conversation</span>
          </Link>
        </div>
      </div>
    </div>
  );
};
