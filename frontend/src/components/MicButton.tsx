import React from 'react';
import { Mic, MicOff, Loader2, Volume2, AlertCircle, Sparkles } from 'lucide-react';

export type MicState =
  | 'IDLE'
  | 'LISTENING'
  | 'PROCESSING'
  | 'AI_THINKING'
  | 'AI_SPEAKING'
  | 'ERROR';

interface MicButtonProps {
  state: MicState;
  onClick: () => void;
  disabled?: boolean;
  errorMessage?: string | null;
  mode?: 'auto_vad' | 'push_to_talk';
  onModeToggle?: () => void;
}

export const MicButton: React.FC<MicButtonProps> = ({
  state,
  onClick,
  disabled = false,
  errorMessage,
  mode = 'auto_vad',
  onModeToggle,
}) => {
  const getButtonConfig = () => {
    switch (state) {
      case 'LISTENING':
        return {
          bg: 'bg-emerald-600 hover:bg-emerald-700',
          ring: 'animate-voice-ripple ring-4 ring-emerald-300/60',
          icon: Mic,
          iconColor: 'text-white',
          label: 'Listening... (Speak naturally)',
          subLabel: mode === 'push_to_talk' ? 'Tap to finish speaking' : 'Speak or tap when done',
        };
      case 'PROCESSING':
        return {
          bg: 'bg-clay-700',
          ring: 'ring-4 ring-clay-300/50',
          icon: Loader2,
          iconColor: 'text-white animate-spin',
          label: 'Processing speech...',
          subLabel: 'Transcribing & analyzing turn',
        };
      case 'AI_THINKING':
        return {
          bg: 'bg-amber-600',
          ring: 'ring-4 ring-amber-300/50 animate-pulse',
          icon: Sparkles,
          iconColor: 'text-white animate-pulse',
          label: 'AI Thinking...',
          subLabel: 'Formulating in-character response',
        };
      case 'AI_SPEAKING':
        return {
          bg: 'bg-terracotta-600',
          ring: 'animate-pulse ring-4 ring-terracotta-300/70',
          icon: Volume2,
          iconColor: 'text-white',
          label: 'AI is Speaking...',
          subLabel: 'Listen carefully',
        };
      case 'ERROR':
        return {
          bg: 'bg-rose-600 hover:bg-rose-700',
          ring: 'ring-4 ring-rose-300/60',
          icon: AlertCircle,
          iconColor: 'text-white',
          label: 'Microphone Error',
          subLabel: errorMessage || 'Tap to retry access',
        };
      case 'IDLE':
      default:
        return {
          bg: 'bg-terracotta-600 hover:bg-terracotta-700 hover:scale-105 active:scale-95',
          ring: 'shadow-warm-xl hover:shadow-glow-terracotta',
          icon: Mic,
          iconColor: 'text-white',
          label: mode === 'push_to_talk' ? 'Tap to Speak' : 'Start Speaking',
          subLabel: 'Ready for your turn',
        };
    }
  };

  const config = getButtonConfig();
  const IconComponent = config.icon;

  return (
    <div className="flex flex-col items-center justify-center gap-3">
      {/* Primary Circular Button */}
      <button
        type="button"
        onClick={onClick}
        disabled={disabled || state === 'PROCESSING' || state === 'AI_THINKING'}
        className={`relative group w-24 h-24 sm:w-28 sm:h-28 rounded-full flex items-center justify-center transition-all duration-300 ${config.bg} ${config.ring} disabled:opacity-60 disabled:cursor-not-allowed`}
        aria-label={config.label}
      >
        <IconComponent className={`w-10 h-10 sm:w-12 sm:h-12 ${config.iconColor}`} />
      </button>

      {/* State Labels */}
      <div className="text-center">
        <p className="text-base font-bold text-clay-900 tracking-wide">
          {config.label}
        </p>
        <p className="text-xs font-medium text-clay-500 mt-0.5 max-w-xs">
          {config.subLabel}
        </p>
      </div>

      {/* Mode Switch Button */}
      {onModeToggle && (
        <button
          type="button"
          onClick={onModeToggle}
          className="mt-1 text-xs font-medium px-3 py-1 rounded-full bg-sand-200/80 hover:bg-sand-300 text-clay-700 transition-colors border border-sand-300"
        >
          Mode: <span className="font-semibold text-terracotta-700">{mode === 'auto_vad' ? 'Auto-Listening' : 'Push-to-Talk'}</span> (Toggle)
        </button>
      )}
    </div>
  );
};
