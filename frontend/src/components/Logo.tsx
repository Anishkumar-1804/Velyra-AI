import React from 'react';

interface LogoProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  showText?: boolean;
  className?: string;
}

export const Logo: React.FC<LogoProps> = ({
  size = 'md',
  showText = true,
  className = '',
}) => {
  const sizeMap = {
    sm: { icon: 'w-7 h-7', text: 'text-base', sub: 'text-[9px]' },
    md: { icon: 'w-9 h-9 sm:w-10 sm:h-10', text: 'text-lg sm:text-xl', sub: 'text-[10px]' },
    lg: { icon: 'w-14 h-14', text: 'text-2xl', sub: 'text-xs' },
    xl: { icon: 'w-24 h-24 sm:w-32 sm:h-32', text: 'text-4xl', sub: 'text-sm' },
  };

  const currentSize = sizeMap[size];

  return (
    <div className={`flex items-center gap-2.5 sm:gap-3 group ${className}`}>
      {/* Modern Velyra Soundwave Icon */}
      <div
        className={`${currentSize.icon} rounded-xl bg-gradient-to-br from-sand-100 to-terracotta-50 flex items-center justify-center shadow-warm-sm group-hover:scale-105 transition-all duration-300 border border-sand-300/80 p-1.5 shrink-0 overflow-hidden relative`}
      >
        <svg
          viewBox="0 0 100 100"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="w-full h-full transform transition-transform group-hover:rotate-2"
        >
          {/* Ambient Resonance Arcs */}
          <circle
            cx="50"
            cy="50"
            r="44"
            stroke="currentColor"
            className="text-sand-300"
            strokeWidth="2.5"
            strokeDasharray="4 4"
            opacity="0.6"
          />
          <circle
            cx="50"
            cy="50"
            r="35"
            stroke="url(#velyra_terracotta)"
            strokeWidth="3"
            opacity="0.35"
          />
          <circle
            cx="50"
            cy="50"
            r="26"
            stroke="url(#velyra_indigo)"
            strokeWidth="3"
            opacity="0.4"
          />

          {/* Stylized 'V' Soundwave Geometry */}
          <path
            d="M26 30 L40 70 L50 48 L60 70 L74 30"
            stroke="url(#velyra_grad)"
            strokeWidth="6.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          />

          {/* Voice Wave Pulse */}
          <path
            d="M14 50 Q 32 50 40 40 T 50 62 T 60 40 T 86 50"
            stroke="url(#velyra_pulse)"
            strokeWidth="4"
            strokeLinecap="round"
            fill="none"
          />

          {/* Core Energy Accent */}
          <circle cx="50" cy="48" r="3.5" fill="#C85A32" />

          {/* Gradients */}
          <defs>
            <linearGradient id="velyra_grad" x1="20" y1="20" x2="80" y2="80" gradientUnits="userSpaceOnUse">
              <stop stopColor="#312E81" />
              <stop offset="0.5" stopColor="#6366F1" />
              <stop offset="1" stopColor="#C85A32" />
            </linearGradient>
            <linearGradient id="velyra_pulse" x1="10" y1="50" x2="90" y2="50" gradientUnits="userSpaceOnUse">
              <stop stopColor="#4F46E5" />
              <stop offset="0.5" stopColor="#C85A32" />
              <stop offset="1" stopColor="#E07A5F" />
            </linearGradient>
            <linearGradient id="velyra_terracotta" x1="0" y1="0" x2="100" y2="100" gradientUnits="userSpaceOnUse">
              <stop stopColor="#E07A5F" />
              <stop offset="1" stopColor="#C85A32" />
            </linearGradient>
            <linearGradient id="velyra_indigo" x1="0" y1="0" x2="100" y2="100" gradientUnits="userSpaceOnUse">
              <stop stopColor="#4338CA" />
              <stop offset="1" stopColor="#6366F1" />
            </linearGradient>
          </defs>
        </svg>
      </div>

      {showText && (
        <div className="flex flex-col">
          <span className={`${currentSize.text} font-extrabold tracking-tight text-clay-900 font-serif leading-none`}>
            Velyra<span className="text-terracotta-600 font-sans">.ai</span>
          </span>
          <span className={`hidden sm:block ${currentSize.sub} font-semibold text-clay-500 tracking-wider uppercase mt-1`}>
            Speak English. Naturally.
          </span>
        </div>
      )}
    </div>
  );
};
