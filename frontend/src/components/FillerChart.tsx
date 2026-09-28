import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { Activity, Repeat } from 'lucide-react';

interface FillerChartProps {
  totalFillers: number;
  fillerRate: number;
  mostUsedFiller?: string;
  fillerBreakdown: Record<string, number>;
  repetitionAnalysis: Record<string, number>;
  totalSpeakingTime: number;
}

export const FillerChart: React.FC<FillerChartProps> = ({
  totalFillers,
  fillerRate,
  mostUsedFiller,
  fillerBreakdown,
  repetitionAnalysis,
  totalSpeakingTime,
}) => {
  const chartData = Object.entries(fillerBreakdown).map(([name, count]) => ({
    name: `"${name}"`,
    count,
  }));

  const colors = ['#C85A32', '#B54823', '#E47E68', '#A47D4C', '#9D8362'];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {/* 1. Filler Words Summary & Bar Chart */}
      <div className="card-sand p-6 flex flex-col justify-between">
        <div>
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Activity className="w-5 h-5 text-terracotta-600" />
              <h3 className="text-base font-bold text-clay-900 font-serif">
                Filler Word Frequency
              </h3>
            </div>
            <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-sand-200 text-clay-800">
              {totalFillers} total ({fillerRate}/min)
            </span>
          </div>

          <div className="grid grid-cols-3 gap-2 mb-4 text-center">
            <div className="p-3 bg-sand-100 rounded-xl">
              <span className="block text-[11px] font-semibold text-clay-500 uppercase">Total Count</span>
              <span className="text-lg font-bold text-clay-900">{totalFillers}</span>
            </div>
            <div className="p-3 bg-sand-100 rounded-xl">
              <span className="block text-[11px] font-semibold text-clay-500 uppercase">Rate / Min</span>
              <span className="text-lg font-bold text-clay-900">{fillerRate}</span>
            </div>
            <div className="p-3 bg-sand-100 rounded-xl">
              <span className="block text-[11px] font-semibold text-clay-500 uppercase">Top Filler</span>
              <span className="text-lg font-bold text-terracotta-700">"{mostUsedFiller || 'None'}"</span>
            </div>
          </div>
        </div>

        {chartData.length > 0 ? (
          <div className="h-44 w-full mt-2">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <XAxis dataKey="name" stroke="#947D5F" fontSize={11} tickLine={false} />
                <YAxis allowDecimals={false} stroke="#947D5F" fontSize={11} tickLine={false} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#FAF7F2', borderRadius: '8px', border: '1px solid #EAE1D2', fontSize: '12px' }}
                />
                <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                  {chartData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <div className="text-center py-8 text-xs text-clay-500">
            No excessive filler words detected! Clean speech delivery.
          </div>
        )}
      </div>

      {/* 2. Repetition Analysis */}
      <div className="card-sand p-6 flex flex-col justify-between">
        <div>
          <div className="flex items-center gap-2 mb-4">
            <Repeat className="w-5 h-5 text-terracotta-600" />
            <h3 className="text-base font-bold text-clay-900 font-serif">
              Repetitive Word Patterns
            </h3>
          </div>
          <p className="text-xs text-clay-600 leading-relaxed mb-4">
            Words repeated 3 or more times during this conversation. Expanding synonyms prevents repetitive phrasing.
          </p>

          {Object.keys(repetitionAnalysis).length > 0 ? (
            <div className="space-y-2.5">
              {Object.entries(repetitionAnalysis).map(([word, count]) => (
                <div key={word} className="flex items-center justify-between p-3 rounded-lg bg-sand-50 border border-sand-200">
                  <span className="text-xs font-bold text-clay-800">"{word}"</span>
                  <span className="text-xs font-semibold px-2 py-0.5 rounded bg-terracotta-100 text-terracotta-800">
                    {count} times
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-10 text-xs text-clay-500 bg-sand-50 rounded-xl border border-dashed border-sand-200">
              Great vocabulary balance! No overly repeated words.
            </div>
          )}
        </div>

        <p className="text-[11px] text-clay-400 mt-4">
          Calculated across {Math.round(totalSpeakingTime)}s of active speech.
        </p>
      </div>
    </div>
  );
};
