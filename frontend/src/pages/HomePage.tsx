import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Mic,
  Compass,
  Award,
  Clock,
  CheckCircle2,
  ChevronRight,
  Sparkles,
  Zap,
  GraduationCap,
  Sun,
  ShoppingBag,
  Plane,
  Utensils,
  MessageCircle,
  Briefcase,
  Flame
} from 'lucide-react';
import { api } from '../services/api';
import { Genre, ProgressSummary, SessionHistoryItem } from '../types';

const GENRE_ICONS: Record<string, React.ElementType> = {
  'college-life': GraduationCap,
  'daily-life': Sun,
  'shopping': ShoppingBag,
  'travel': Plane,
  'cooking-food': Utensils,
  'casual-talks': MessageCircle,
  'professional-talks': Briefcase,
};

export const HomePage: React.FC = () => {
  const [genres, setGenres] = useState<Genre[]>([]);
  const [progress, setProgress] = useState<ProgressSummary | null>(null);
  const [recentHistory, setRecentHistory] = useState<SessionHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [genresData, progressData, historyData] = await Promise.all([
          api.getGenres(),
          api.getProgressSummary(),
          api.getSessionHistory(),
        ]);
        setGenres(genresData);
        setProgress(progressData);
        setRecentHistory(historyData.slice(0, 3));
      } catch (err) {
        console.error('Error fetching home data:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="space-y-12">
      {/* 1. HERO SECTION */}
      <section className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-sand-100 via-sand-200/50 to-terracotta-50/50 border border-sand-300/80 p-8 sm:p-12 lg:p-14 shadow-warm-md flex flex-col md:flex-row items-center justify-between gap-8">
        <div className="max-w-2xl space-y-5">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-terracotta-100/80 text-terracotta-800 text-xs font-bold border border-terracotta-200">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Voice-First AI English Conversation</span>
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-clay-900 tracking-tight font-serif leading-tight">
            Speak English.{' '}
            <span className="text-terracotta-600 block sm:inline">Naturally.</span>
          </h1>

          <p className="text-base sm:text-lg text-clay-700 leading-relaxed font-normal">
            Practice real, structured English conversations with your local AI speaking partner.
            Get instant feedback, natural Indian English voice responses, and evidence-based evaluations.
          </p>

          <div className="flex flex-wrap items-center gap-4 pt-2">
            <Link
              to="/genres"
              className="inline-flex items-center gap-2 px-7 py-3.5 rounded-xl bg-terracotta-600 hover:bg-terracotta-700 text-white font-bold text-sm shadow-warm-md hover:shadow-glow-terracotta transition-all hover:scale-105 active:scale-95"
            >
              <Mic className="w-4 h-4" />
              <span>Start Speaking</span>
            </Link>

            <Link
              to="/progress"
              className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-white hover:bg-sand-50 text-clay-800 font-semibold text-sm border border-sand-300 shadow-warm-sm transition-all"
            >
              <span>View Progress</span>
              <ChevronRight className="w-4 h-4 text-clay-400" />
            </Link>
          </div>
        </div>

        {/* Hero Logo Asset */}
        <div className="flex flex-col items-center justify-center shrink-0 p-2 sm:p-4">
          <div className="w-28 h-28 sm:w-36 sm:h-36 md:w-44 md:h-44 rounded-3xl overflow-hidden shadow-warm-lg border-2 border-sand-200/80 bg-white/90 p-2 backdrop-blur-sm transform hover:rotate-1 hover:scale-105 transition-all duration-300">
            <img src="/logo.png" alt="Velyra.ai" className="w-full h-full object-contain rounded-2xl" />
          </div>
        </div>
      </section>

      {/* 2. STATS & LEVEL OVERVIEW */}
      <section className="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        <div className="card-sand p-5 flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-terracotta-100 text-terracotta-700 flex items-center justify-center shrink-0">
            <Award className="w-6 h-6" />
          </div>
          <div>
            <span className="block text-xs font-semibold text-clay-500 uppercase">Current Level</span>
            <span className="text-xl font-bold text-clay-900 font-serif">
              {progress?.current_estimated_cefr || 'A1'}
            </span>
          </div>
        </div>

        <div className="card-sand p-5 flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center shrink-0">
            <Clock className="w-6 h-6" />
          </div>
          <div>
            <span className="block text-xs font-semibold text-clay-500 uppercase">Speaking Time</span>
            <span className="text-xl font-bold text-clay-900 font-serif">
              {progress?.total_speaking_time_minutes || 0} mins
            </span>
          </div>
        </div>

        <div className="card-sand p-5 flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-teal-100 text-teal-700 flex items-center justify-center shrink-0">
            <CheckCircle2 className="w-6 h-6" />
          </div>
          <div>
            <span className="block text-xs font-semibold text-clay-500 uppercase">Sessions Done</span>
            <span className="text-xl font-bold text-clay-900 font-serif">
              {progress?.total_sessions_completed || 0}
            </span>
          </div>
        </div>

        <div className="card-sand p-5 flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-rose-100 text-rose-700 flex items-center justify-center shrink-0">
            <Flame className="w-6 h-6" />
          </div>
          <div>
            <span className="block text-xs font-semibold text-clay-500 uppercase">Practice Streak</span>
            <span className="text-xl font-bold text-clay-900 font-serif">
              {progress?.streak_days || 0} Days
            </span>
          </div>
        </div>
      </section>

      {/* 3. SPEAKING GENRES */}
      <section className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-clay-900 font-serif">Choose a Practice Area</h2>
            <p className="text-xs sm:text-sm text-clay-600 mt-1">
              Real-world scenario genres authored for Indian college students and professionals.
            </p>
          </div>
          <Link
            to="/genres"
            className="text-xs font-bold text-terracotta-600 hover:text-terracotta-700 flex items-center gap-1"
          >
            <span>View All</span>
            <ChevronRight className="w-4 h-4" />
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {genres.slice(0, 6).map((genre) => {
            const Icon = GENRE_ICONS[genre.slug] || MessageCircle;
            return (
              <Link
                key={genre.id}
                to={`/genre/${genre.id}`}
                className="card-sand card-sand-hover p-6 flex flex-col justify-between group"
              >
                <div>
                  <div className="w-12 h-12 rounded-xl bg-sand-100 text-terracotta-600 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                    <Icon className="w-6 h-6" />
                  </div>

                  <h3 className="text-lg font-bold text-clay-900 group-hover:text-terracotta-600 transition-colors font-serif">
                    {genre.title}
                  </h3>
                  <p className="text-xs text-clay-600 mt-2 line-clamp-2 leading-relaxed">
                    {genre.description}
                  </p>
                </div>

                <div className="mt-6 pt-4 border-t border-sand-200 flex items-center justify-between text-xs text-clay-500">
                  <span>{genre.session_count} Scenarios</span>
                  <div className="flex items-center gap-1 font-semibold text-terracotta-700">
                    <span>Explore</span>
                    <ChevronRight className="w-3.5 h-3.5" />
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      </section>

      {/* 4. RECENT SESSIONS */}
      {recentHistory.length > 0 && (
        <section className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-clay-900 font-serif">Recent Practice Sessions</h2>
            <Link to="/history" className="text-xs font-bold text-terracotta-600 hover:text-terracotta-700">
              View History
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {recentHistory.map((item) => (
              <div key={item.attempt_id} className="card-sand p-4 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between text-xs text-clay-500 mb-2">
                    <span>{item.genre_title}</span>
                    <span className="font-bold text-clay-900 bg-sand-100 px-2 py-0.5 rounded">
                      {item.estimated_cefr || item.difficulty}
                    </span>
                  </div>
                  <h4 className="font-bold text-sm text-clay-900 line-clamp-1">{item.session_title}</h4>
                </div>

                <div className="mt-4 pt-3 border-t border-sand-100 flex items-center justify-between">
                  <span className="text-xs font-bold text-terracotta-700">
                    Score: {item.overall_score !== null ? `${item.overall_score}%` : 'Incomplete'}
                  </span>
                  <Link
                    to={`/session/${item.session_id}/results/${item.attempt_id}`}
                    className="text-xs font-semibold text-clay-700 hover:text-terracotta-600"
                  >
                    View Report →
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
};
