import React, { useEffect, useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend
} from 'recharts';
import { BarChart2, Award, Clock, Flame, CheckCircle2, TrendingUp } from 'lucide-react';
import { api } from '../services/api';
import { ProgressSummary } from '../types';

export const ProgressPage: React.FC = () => {
  const [progress, setProgress] = useState<ProgressSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProgress = async () => {
      try {
        const data = await api.getProgressSummary();
        setProgress(data);
      } catch (err) {
        console.error('Error fetching progress summary:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchProgress();
  }, []);

  if (loading) {
    return <div className="py-20 text-center text-clay-500">Loading progress analytics...</div>;
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <span className="text-xs uppercase font-bold tracking-widest text-terracotta-600">Analytics</span>
        <h1 className="text-3xl font-extrabold text-clay-900 mt-1 font-serif">
          Speaking Progress Dashboard
        </h1>
        <p className="text-sm text-clay-600 mt-2 max-w-2xl">
          Track your conversational growth, fluency improvements, and CEFR speaking milestones over time.
        </p>
      </div>

      {/* 4 Summary Stat Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        <div className="card-sand p-6 flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-clay-500 uppercase">Average Score</span>
            <Award className="w-5 h-5 text-terracotta-600" />
          </div>
          <span className="text-3xl font-extrabold text-clay-900 font-serif mt-3">
            {progress?.average_score || 0}%
          </span>
          <span className="text-xs text-clay-500 mt-1">Best: {progress?.best_score || 0}%</span>
        </div>

        <div className="card-sand p-6 flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-clay-500 uppercase">Total Speaking Time</span>
            <Clock className="w-5 h-5 text-amber-600" />
          </div>
          <span className="text-3xl font-extrabold text-clay-900 font-serif mt-3">
            {progress?.total_speaking_time_minutes || 0}m
          </span>
          <span className="text-xs text-clay-500 mt-1">Active speech minutes</span>
        </div>

        <div className="card-sand p-6 flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-clay-500 uppercase">Completed Scenarios</span>
            <CheckCircle2 className="w-5 h-5 text-emerald-600" />
          </div>
          <span className="text-3xl font-extrabold text-clay-900 font-serif mt-3">
            {progress?.total_sessions_completed || 0}
          </span>
          <span className="text-xs text-clay-500 mt-1">Across 7 genres</span>
        </div>

        <div className="card-sand p-6 flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-clay-500 uppercase">Estimated CEFR</span>
            <Flame className="w-5 h-5 text-rose-600" />
          </div>
          <span className="text-3xl font-extrabold text-terracotta-700 font-serif mt-3">
            {progress?.current_estimated_cefr || 'A1'}
          </span>
          <span className="text-xs text-clay-500 mt-1">AI Speaking Assessment</span>
        </div>
      </div>

      {/* Historical Score Trend Line Chart */}
      <div className="card-sand p-6 sm:p-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-base font-bold text-clay-900 font-serif">
              Skill Trends Over Time
            </h3>
            <p className="text-xs text-clay-500">
              Evolution of your Fluency, Accuracy, and Grammar across completed sessions.
            </p>
          </div>
        </div>

        {progress?.score_trend && progress.score_trend.length > 0 ? (
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={progress.score_trend} margin={{ top: 10, right: 20, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#EFE6D8" />
                <XAxis dataKey="session_num" tickFormatter={(val) => `S${val}`} stroke="#947D5F" fontSize={11} />
                <YAxis domain={[0, 100]} stroke="#947D5F" fontSize={11} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#FAF7F2', borderRadius: '8px', border: '1px solid #EAE1D2', fontSize: '12px' }}
                />
                <Legend wrapperStyle={{ fontSize: '12px' }} />
                <Line type="monotone" dataKey="overall" name="Overall Score" stroke="#C85A32" strokeWidth={3} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="fluency" name="Fluency" stroke="#10B981" strokeWidth={2} dot={{ r: 3 }} />
                <Line type="monotone" dataKey="accuracy" name="Accuracy" stroke="#3B82F6" strokeWidth={2} dot={{ r: 3 }} />
                <Line type="monotone" dataKey="grammar" name="Grammar" stroke="#F59E0B" strokeWidth={2} dot={{ r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <div className="text-center py-16 text-xs text-clay-500 bg-sand-50 rounded-xl border border-dashed border-sand-300">
            Complete your first speaking session to unlock your progress curve!
          </div>
        )}
      </div>

      {/* Genre Progress Breakdown */}
      <div className="card-sand p-6 sm:p-8">
        <h3 className="text-base font-bold text-clay-900 font-serif mb-4">
          Curriculum Completion by Genre
        </h3>
        <div className="space-y-4">
          {progress?.genre_progress.map((gp) => (
            <div key={gp.id} className="space-y-1.5">
              <div className="flex items-center justify-between text-xs">
                <span className="font-bold text-clay-800">{gp.title}</span>
                <span className="text-clay-500 font-medium">
                  {gp.completed_sessions} / {gp.total_sessions} ({gp.percentage}%)
                </span>
              </div>
              <div className="w-full bg-sand-200 h-2.5 rounded-full overflow-hidden">
                <div
                  className="bg-terracotta-600 h-full rounded-full transition-all duration-500"
                  style={{ width: `${gp.percentage}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
