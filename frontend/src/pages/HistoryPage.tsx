import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Search, Clock, Award, RotateCcw, ChevronRight, CheckCircle2, History } from 'lucide-react';
import { api } from '../services/api';
import { SessionHistoryItem } from '../types';

export const HistoryPage: React.FC = () => {
  const [history, setHistory] = useState<SessionHistoryItem[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const data = await api.getSessionHistory();
        setHistory(data);
      } catch (err) {
        console.error('Error fetching history:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  const filteredHistory = history.filter((item) => {
    const q = searchQuery.toLowerCase();
    return (
      item.session_title.toLowerCase().includes(q) ||
      item.genre_title.toLowerCase().includes(q) ||
      item.unit_title.toLowerCase().includes(q)
    );
  });

  const formatDate = (isoStr?: string) => {
    if (!isoStr) return 'N/A';
    const d = new Date(isoStr);
    return d.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <span className="text-xs uppercase font-bold tracking-widest text-terracotta-600">Archive</span>
          <h1 className="text-3xl font-extrabold text-clay-900 mt-1 font-serif">
            Practice History
          </h1>
          <p className="text-sm text-clay-600 mt-1">
            Review past conversations, evidence reports, and repeat earlier scenarios.
          </p>
        </div>

        {/* Search Input */}
        <div className="relative w-full sm:w-72">
          <Search className="w-4 h-4 text-clay-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search past sessions..."
            className="w-full pl-9 pr-4 py-2 text-xs rounded-xl bg-white border border-sand-300 focus:outline-none focus:border-terracotta-500 focus:ring-1 focus:ring-terracotta-500"
          />
        </div>
      </div>

      {/* History Items List */}
      {loading ? (
        <div className="py-20 text-center text-clay-500">Loading history...</div>
      ) : filteredHistory.length === 0 ? (
        <div className="card-sand p-12 text-center space-y-3">
          <History className="w-10 h-10 text-clay-400 mx-auto" />
          <h3 className="font-bold text-base text-clay-800">No practice attempts found</h3>
          <p className="text-xs text-clay-500">
            {searchQuery ? 'Try a different search keyword.' : 'Start speaking in any genre to record your attempts!'}
          </p>
          <Link
            to="/genres"
            className="inline-flex items-center gap-1 px-5 py-2.5 rounded-xl bg-terracotta-600 text-white text-xs font-bold mt-2"
          >
            Explore Scenarios
          </Link>
        </div>
      ) : (
        <div className="space-y-3">
          {filteredHistory.map((item) => (
            <div
              key={item.attempt_id}
              className="card-sand card-sand-hover p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4"
            >
              <div className="space-y-1">
                <div className="flex items-center gap-2 text-xs text-clay-500">
                  <span className="font-semibold text-clay-700">{item.genre_title}</span>
                  <span>•</span>
                  <span>{item.unit_title}</span>
                  <span>•</span>
                  <span>{formatDate(item.started_at)}</span>
                </div>

                <h3 className="text-base font-bold text-clay-900 font-serif">
                  {item.session_title}
                </h3>

                <div className="flex items-center gap-3 text-xs text-clay-500 pt-1">
                  <span className="flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5" />
                    {item.duration_seconds}s
                  </span>
                  <span>•</span>
                  <span>{item.turn_count} turns</span>
                  {item.estimated_cefr && (
                    <span className="font-bold text-clay-800 bg-sand-200 px-2 py-0.5 rounded text-[11px]">
                      CEFR {item.estimated_cefr}
                    </span>
                  )}
                </div>
              </div>

              {/* Action Buttons & Score */}
              <div className="flex items-center gap-3 self-end sm:self-center">
                {item.overall_score !== null ? (
                  <div className="text-right mr-2">
                    <span className="block text-[10px] font-bold text-clay-500 uppercase">Score</span>
                    <span className="text-lg font-bold text-terracotta-700 font-serif">
                      {item.overall_score}%
                    </span>
                  </div>
                ) : (
                  <span className="text-xs font-semibold text-clay-400 italic mr-2">Incomplete</span>
                )}

                <Link
                  to={`/session/${item.session_id}/results/${item.attempt_id}`}
                  className="px-4 py-2 rounded-lg bg-sand-100 hover:bg-sand-200 text-clay-800 text-xs font-bold transition-colors"
                >
                  View Report
                </Link>

                <Link
                  to={`/session/${item.session_id}/live`}
                  className="px-4 py-2 rounded-lg bg-terracotta-600 hover:bg-terracotta-700 text-white text-xs font-bold shadow-warm-sm transition-colors"
                >
                  Repeat
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
