import React from 'react';

interface AudioVisualizerProps {
  energy: number; // 0 to 100
  isActive: boolean;
  mode?: 'user' | 'ai';
  barCount?: number;
}

export const AudioVisualizer: React.FC<AudioVisualizerProps> = ({
  energy,
  isActive,
  mode = 'user',
  barCount = 16,
}) => {
  return (
    <div className="flex items-center justify-center gap-1.5 h-12 px-4 py-2 bg-sand-100/60 rounded-2xl border border-sand-200">
      {Array.from({ length: barCount }).map((_, i) => {
        // Calculate variable bar height based on energy and position
        const centerDist = Math.abs(i - barCount / 2) / (barCount / 2);
        const factor = Math.max(0.2, 1 - centerDist * 0.6);
        
        let heightPct = 15;
        if (isActive) {
          const pseudoRandom = Math.sin((i + 1) * 1.5 + Date.now() / 200) * 0.3 + 0.7;
          heightPct = Math.min(100, Math.max(20, (energy * factor * pseudoRandom)));
        }

        const barColor =
          mode === 'ai'
            ? 'bg-gradient-to-t from-terracotta-500 to-terracotta-400'
            : isActive
            ? 'bg-gradient-to-t from-emerald-500 to-teal-400'
            : 'bg-sand-300';

        return (
          <div
            key={i}
            className={`w-1.5 rounded-full transition-all duration-75 ${barColor}`}
            style={{
              height: `${heightPct}%`,
            }}
          />
        );
      })}
    </div>
  );
};
