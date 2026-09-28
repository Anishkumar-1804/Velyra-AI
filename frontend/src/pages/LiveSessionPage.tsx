import React, { useEffect, useState, useRef, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Volume2,
  Sparkles,
  User,
  Bot,
  Send,
  Clock,
  ArrowRight,
  Mic,
  Radio,
  Lightbulb,
  Check
} from 'lucide-react';
import { api } from '../services/api';
import { SessionDetail, ConversationTurn, StartSessionResponse } from '../types';
import { useAudioRecorder } from '../hooks/useAudioRecorder';
import { AudioVisualizer } from '../components/AudioVisualizer';

export const LiveSessionPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [session, setSession] = useState<SessionDetail | null>(null);
  const [attemptId, setAttemptId] = useState<number | null>(null);
  const [turns, setTurns] = useState<ConversationTurn[]>([]);
  const [currentStage, setCurrentStage] = useState<number>(0);
  const [totalStages, setTotalStages] = useState<number>(5);
  
  const [micState, setMicState] = useState<'IDLE' | 'LISTENING' | 'PROCESSING' | 'AI_THINKING' | 'AI_SPEAKING' | 'ERROR'>('IDLE');
  const [elapsedSeconds, setElapsedSeconds] = useState<number>(0);
  const [isCompleted, setIsCompleted] = useState<boolean>(false);
  const [typedMessage, setTypedMessage] = useState<string>('');
  const [isAiSpeaking, setIsAiSpeaking] = useState<boolean>(false);
  const [nudgeMessage, setNudgeMessage] = useState<string | null>(null);
  const [suggestedResponse, setSuggestedResponse] = useState<string | null>(null);

  const audioPlayerRef = useRef<HTMLAudioElement | null>(null);
  const chatScrollRef = useRef<HTMLDivElement | null>(null);
  const hasInitializedRef = useRef<boolean>(false);
  const isSubmittingRef = useRef<boolean>(false);
  const attemptIdRef = useRef<number | null>(null);
  attemptIdRef.current = attemptId;

  // Refs for stable function calls
  const startRecordingRef = useRef<() => Promise<void>>(async () => {});
  const handleAudioUploadRef = useRef<(blob: Blob | null, transcript: string) => Promise<void>>(async () => {});

  // Callback when user finishes speaking (silence after speech)
  const handleSpeechEnd = useCallback(async (blob: Blob | null, transcript: string) => {
    if (isSubmittingRef.current) return;
    const cleanText = (transcript || '').trim();
    if (!cleanText || cleanText.length < 2) return;

    console.log('[LiveSession] Spoken speech detected. Submitting turn:', cleanText);
    setNudgeMessage(null);
    if (handleAudioUploadRef.current) {
      await handleAudioUploadRef.current(blob, cleanText);
    }
  }, []);

  // Callback when user is silent without speaking (inactivity timeout)
  const handleInactivityTimeout = useCallback(async () => {
    const attId = attemptIdRef.current;
    if (!attId || isAiSpeaking || isSubmittingRef.current) return;
    console.log('[LiveSession] Inactivity detected. Requesting nudge...');
    try {
      const nudge = await api.getSilenceNudge(attId);
      if (nudge && nudge.nudge_text) {
        setNudgeMessage(nudge.nudge_text);
        if (nudge.audio_url || nudge.nudge_text) {
          playAiAudioRef.current(nudge.audio_url, nudge.nudge_text);
        }
      }
    } catch (e) {
      console.debug('Nudge notice:', e);
    }
  }, [isAiSpeaking]);

  const {
    isRecording,
    liveTranscript,
    audioEnergy,
    error: recorderError,
    startRecording,
    stopRecording,
    resetAudio,
    stopAll,
  } = useAudioRecorder({
    onSpeechEnd: handleSpeechEnd,
    onInactivityTimeout: handleInactivityTimeout,
    silenceThresholdMs: 1500,
    inactivityTimeoutMs: 9500,
  });

  startRecordingRef.current = startRecording;

  const speakBrowserTTS = useCallback((text: string, onEnd: () => void) => {
    try {
      if (!('speechSynthesis' in window)) {
        onEnd();
        return;
      }
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'en-IN';
      utterance.rate = 1.0;
      utterance.pitch = 1.0;
      const voices = window.speechSynthesis.getVoices();
      const indianVoice = voices.find(
        (v) => v.lang.includes('en-IN') || v.name.toLowerCase().includes('india') || v.name.toLowerCase().includes('neerja') || v.name.toLowerCase().includes('prabhat')
      );
      if (indianVoice) {
        utterance.voice = indianVoice;
      }
      utterance.onend = () => onEnd();
      utterance.onerror = () => onEnd();
      window.speechSynthesis.speak(utterance);
    } catch (e) {
      onEnd();
    }
  }, []);

  // Stable audio player with live synthesis fallback
  const playAiAudio = useCallback((url?: string | null, text?: string) => {
    setIsAiSpeaking(true);
    setMicState('AI_SPEAKING');

    if (audioPlayerRef.current) {
      audioPlayerRef.current.pause();
    }

    const resumeListening = async () => {
      setIsAiSpeaking(false);
      try {
        setMicState('LISTENING');
        await startRecordingRef.current();
      } catch (err) {
        console.warn('Auto resume recording notice:', err);
        setMicState('IDLE');
      }
    };

    if (url) {
      const audio = new Audio(url);
      audioPlayerRef.current = audio;

      audio.onended = () => {
        resumeListening();
      };

      audio.onerror = () => {
        if (text) {
          speakBrowserTTS(text, resumeListening);
        } else {
          resumeListening();
        }
      };

      audio.play().catch((err) => {
        if (text) {
          speakBrowserTTS(text, resumeListening);
        } else {
          resumeListening();
        }
      });
    } else if (text) {
      speakBrowserTTS(text, resumeListening);
    } else {
      resumeListening();
    }
  }, [speakBrowserTTS]);

  const playAiAudioRef = useRef(playAiAudio);
  playAiAudioRef.current = playAiAudio;

  // Unmount cleanup to immediately stop audio playback and microphone capture on navigation
  useEffect(() => {
    return () => {
      console.log('[LiveSession] Navigating away. Stopping all agent audio & microphone streams...');
      if (audioPlayerRef.current) {
        audioPlayerRef.current.pause();
        audioPlayerRef.current.src = '';
        audioPlayerRef.current = null;
      }
      stopAll();
      setIsAiSpeaking(false);
      setMicState('IDLE');
    };
  }, [stopAll]);

  // Upload user audio & live transcript to backend and receive AI response
  const handleAudioUpload = useCallback(async (blob: Blob | null, transcript: string) => {
    const currentAttId = attemptIdRef.current;
    if (!currentAttId || isSubmittingRef.current) return;

    const userText = (transcript || '').trim();
    if (!userText || userText.length < 2) {
      setMicState('LISTENING');
      await startRecordingRef.current();
      return;
    }

    isSubmittingRef.current = true;
    const optimisticId = Date.now();
    const optimisticTurn: ConversationTurn = {
      id: optimisticId,
      attempt_id: currentAttId,
      turn_index: 9999,
      speaker: 'user',
      transcript: userText,
      audio_duration: 2.0,
      filler_count: 0,
      detected_fillers: [],
      pause_count: 0,
      created_at: new Date().toISOString(),
    };

    setTurns((prev) => [...prev, optimisticTurn]);
    setMicState('AI_THINKING');
    setNudgeMessage(null);

    try {
      let response;
      if (blob && blob.size > 500) {
        response = await api.sendAudioTurn(currentAttId, blob, userText);
      } else {
        response = await api.sendTextTurn(currentAttId, userText);
      }

      setTurns((prev) => {
        const withoutOptimistic = prev.filter((t) => t.id !== optimisticId);
        const seenIds = new Set(withoutOptimistic.map((t) => t.id));
        const newTurns = [response.user_turn, response.ai_turn].filter((t) => !seenIds.has(t.id));
        return [...withoutOptimistic, ...newTurns];
      });
      setCurrentStage(response.current_stage);

      if (response.suggested_response) {
        setSuggestedResponse(response.suggested_response);
      }

      if (response.is_completed) {
        setIsCompleted(true);
      }

      if (response.ai_audio_url || response.ai_turn?.transcript) {
        playAiAudioRef.current(response.ai_audio_url, response.ai_turn?.transcript);
      } else {
        setMicState('LISTENING');
        await startRecordingRef.current();
      }
    } catch (err) {
      console.error('Error in speech turn:', err);
      setMicState('ERROR');
    } finally {
      isSubmittingRef.current = false;
    }
  }, []);

  handleAudioUploadRef.current = handleAudioUpload;

  // Initialize speaking session ONCE on mount
  useEffect(() => {
    if (!id || hasInitializedRef.current) return;
    hasInitializedRef.current = true;

    const initSession = async () => {
      try {
        const sessionDetail = await api.getSessionDetail(Number(id));
        setSession(sessionDetail);

        const startData = await api.startSession(Number(id));
        setAttemptId(startData.attempt_id);
        attemptIdRef.current = startData.attempt_id;
        setCurrentStage(startData.current_stage);
        setTotalStages(startData.total_stages);

        if (startData.suggested_response) {
          setSuggestedResponse(startData.suggested_response);
        }

        // Record opening AI message
        const openingTurn: ConversationTurn = {
          id: 0,
          attempt_id: startData.attempt_id,
          turn_index: 0,
          speaker: 'ai',
          transcript: startData.opening_message,
          audio_url: startData.audio_url,
          audio_duration: 3.5,
          filler_count: 0,
          detected_fillers: [],
          pause_count: 0,
          created_at: new Date().toISOString(),
        };
        setTurns([openingTurn]);

        // Auto-play AI opening audio (which auto-triggers startRecording on finish)
        if (startData.audio_url || startData.opening_message) {
          playAiAudioRef.current(startData.audio_url, startData.opening_message);
        } else {
          setMicState('LISTENING');
          await startRecordingRef.current();
        }
      } catch (err) {
        console.error('Error starting live session:', err);
        setMicState('ERROR');
      }
    };
    initSession();
  }, [id]);

  // Scroll to bottom on new turn or live speech
  useEffect(() => {
    if (chatScrollRef.current) {
      chatScrollRef.current.scrollTop = chatScrollRef.current.scrollHeight;
    }
  }, [turns, micState, liveTranscript, nudgeMessage]);

  // Session timer
  useEffect(() => {
    const timer = setInterval(() => {
      setElapsedSeconds((prev) => prev + 1);
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  // Handle Typed Message Fallback
  const handleSendTextTurn = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!typedMessage.trim() || !attemptId || isSubmittingRef.current) return;

    const userText = typedMessage.trim();
    setTypedMessage('');
    isSubmittingRef.current = true;

    const optimisticId = Date.now();
    const optimisticTurn: ConversationTurn = {
      id: optimisticId,
      attempt_id: attemptId,
      turn_index: 9999,
      speaker: 'user',
      transcript: userText,
      audio_duration: 1.5,
      filler_count: 0,
      detected_fillers: [],
      pause_count: 0,
      created_at: new Date().toISOString(),
    };

    setTurns((prev) => [...prev, optimisticTurn]);
    setMicState('AI_THINKING');
    setNudgeMessage(null);

    try {
      const response = await api.sendTextTurn(attemptId, userText);
      setTurns((prev) => {
        const withoutOptimistic = prev.filter((t) => t.id !== optimisticId);
        const seenIds = new Set(withoutOptimistic.map((t) => t.id));
        const newTurns = [response.user_turn, response.ai_turn].filter((t) => !seenIds.has(t.id));
        return [...withoutOptimistic, ...newTurns];
      });
      setCurrentStage(response.current_stage);

      if (response.suggested_response) {
        setSuggestedResponse(response.suggested_response);
      }

      if (response.is_completed) {
        setIsCompleted(true);
      }

      if (response.ai_audio_url || response.ai_turn?.transcript) {
        playAiAudioRef.current(response.ai_audio_url, response.ai_turn?.transcript);
      } else {
        setMicState('LISTENING');
        await startRecordingRef.current();
      }
    } catch (err) {
      console.error('Error sending text turn:', err);
      setMicState('ERROR');
    } finally {
      isSubmittingRef.current = false;
    }
  };

  // Click Suggested Sentence to use it
  const handleUseSuggestion = (suggestion: string) => {
    setTypedMessage(suggestion);
  };

  // End Speaking Session and navigate to Results
  const handleFinishSession = async () => {
    if (!attemptId || !id) return;
    
    // Stop agent and audio immediately on finish
    if (audioPlayerRef.current) {
      audioPlayerRef.current.pause();
      audioPlayerRef.current.src = '';
    }
    stopAll();

    try {
      await api.endSessionAttempt(attemptId);
      navigate(`/session/${id}/results/${attemptId}`);
    } catch (err) {
      console.error('Error finishing session:', err);
      navigate(`/session/${id}/results/${attemptId}`);
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  };

  const latestAiTurn = turns.filter((t) => t.speaker === 'ai').slice(-1)[0];

  return (
    <div className="max-w-3xl mx-auto space-y-4">
      {/* 1. Clean Scenario & Title Header */}
      <div className="card-sand p-5 space-y-3">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[11px] font-bold uppercase tracking-widest text-terracotta-600">
                {session?.genre_title || 'Speaking Practice'}
              </span>
              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 text-[10px] font-bold">
                <Radio className="w-3 h-3 animate-pulse text-emerald-600" />
                Hands-Free Auto Mode
              </span>
              <span className="px-2 py-0.5 rounded-md bg-sand-200 text-clay-700 text-[10px] font-bold">
                {session?.cefr_level || 'B1'}
              </span>
            </div>
            <h1 className="text-xl font-bold text-clay-900 font-serif mt-1">
              {session?.title || 'Speaking Session'}
            </h1>
          </div>

          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-sand-100 text-clay-700 text-xs font-semibold border border-sand-200">
              <Clock className="w-3.5 h-3.5 text-terracotta-600" />
              <span>{formatTime(elapsedSeconds)}</span>
            </div>

            <button
              onClick={handleFinishSession}
              className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-clay-800 hover:bg-clay-900 text-white text-xs font-bold transition-all shadow-warm-sm"
            >
              <span>Finish</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Situation / Scenario Description */}
        <div className="p-3.5 rounded-xl bg-terracotta-50/80 border border-terracotta-200/80 text-xs text-clay-800 leading-relaxed">
          <span className="font-bold text-terracotta-800 block mb-0.5">
            📍 Your Situation:
          </span>
          <p>{session?.scenario || 'Speak naturally with your AI partner to practice conversational English.'}</p>
        </div>
      </div>

      {/* 2. Unified Voice Chat Section */}
      <div className="card-sand p-5 flex flex-col h-[460px] shadow-warm-md">
        {/* Chat Header with AI Avatar & Replay Voice */}
        <div className="flex items-center justify-between pb-3 border-b border-sand-200">
          <div className="flex items-center gap-2.5">
            <div className={`w-9 h-9 rounded-xl overflow-hidden flex items-center justify-center transition-all ${
              isAiSpeaking
                ? 'ring-4 ring-terracotta-300 shadow-glow-terracotta animate-pulse'
                : 'ring-1 ring-sand-300 shadow-warm-sm'
            }`}>
              <img src="/logo.png" alt="AI Partner" className="w-full h-full object-cover" />
            </div>
            <div>
              <span className="font-bold text-xs text-clay-900 block">{session?.ai_role || 'AI Partner'}</span>
              <span className="text-[10px] text-clay-500">
                {isAiSpeaking ? 'Speaking...' : micState === 'AI_THINKING' ? 'Typing...' : micState === 'LISTENING' ? 'Listening to you...' : 'Ready'}
              </span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {(latestAiTurn?.audio_url || latestAiTurn?.transcript) && (
              <button
                onClick={() => playAiAudioRef.current(latestAiTurn.audio_url || null, latestAiTurn.transcript)}
                className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-sand-100 hover:bg-sand-200 text-clay-700 text-[11px] font-semibold border border-sand-200 transition-colors cursor-pointer"
              >
                <Volume2 className="w-3 h-3 text-terracotta-600" />
                <span>Replay AI</span>
              </button>
            )}
          </div>
        </div>

        {/* Message Feed */}
        <div ref={chatScrollRef} className="flex-1 overflow-y-auto py-4 space-y-4 pr-1.5">
          {turns.map((turn, i) => {
            const isAi = turn.speaker === 'ai';
            return (
              <div
                key={i}
                className={`flex items-start gap-2.5 ${isAi ? 'justify-start' : 'justify-end'}`}
              >
                {isAi && (
                  <div className="w-7 h-7 rounded-lg overflow-hidden shrink-0 mt-0.5 border border-sand-300 shadow-xs">
                    <img src="/logo.png" alt="AI" className="w-full h-full object-cover" />
                  </div>
                )}

                <div
                  className={`max-w-[85%] rounded-2xl p-3.5 text-xs sm:text-sm leading-relaxed ${
                    isAi
                      ? 'bg-sand-100 text-clay-900 rounded-tl-none border border-sand-200'
                      : 'bg-clay-800 text-sand-50 rounded-tr-none shadow-warm-sm'
                  }`}
                >
                  <p>{turn.transcript}</p>
                  {turn.filler_count > 0 && !isAi && (
                    <span className="block text-[10px] text-amber-300 mt-1">
                      Detected {turn.filler_count} filler {turn.filler_count === 1 ? 'word' : 'words'}
                    </span>
                  )}
                </div>

                {!isAi && (
                  <div className="w-6 h-6 rounded-full bg-clay-700 text-white flex items-center justify-center shrink-0 mt-0.5">
                    <User className="w-3.5 h-3.5" />
                  </div>
                )}
              </div>
            );
          })}

          {/* LIVE STREAMING SPEECH BUBBLE */}
          {micState === 'LISTENING' && liveTranscript && (
            <div className="flex items-start justify-end gap-2.5">
              <div className="max-w-[85%] rounded-2xl p-3 text-xs sm:text-sm leading-relaxed bg-emerald-900/90 text-emerald-100 rounded-tr-none shadow-warm-md border border-emerald-500/50 animate-pulse">
                <div className="flex items-center gap-1.5 text-[10px] font-bold text-emerald-300 uppercase tracking-wider mb-1">
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                  <span>Transcribing live speech...</span>
                </div>
                <p className="font-medium">"{liveTranscript}"</p>
              </div>
              <div className="w-6 h-6 rounded-full bg-emerald-700 text-white flex items-center justify-center shrink-0 mt-0.5">
                <Mic className="w-3.5 h-3.5" />
              </div>
            </div>
          )}

          {/* WHATSAPP-STYLE TYPING ANIMATION */}
          {micState === 'AI_THINKING' && (
            <div className="flex items-start gap-2.5 justify-start animate-fade-in">
              <div className="w-7 h-7 rounded-lg overflow-hidden shrink-0 mt-0.5 border border-sand-300 shadow-xs">
                <img src="/logo.png" alt="AI" className="w-full h-full object-cover" />
              </div>
              <div className="bg-sand-100 text-clay-700 rounded-2xl rounded-tl-none px-4 py-3 border border-sand-200 shadow-sm flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-terracotta-500 animate-bounce [animation-delay:-0.3s]"></span>
                <span className="w-2 h-2 rounded-full bg-terracotta-500 animate-bounce [animation-delay:-0.15s]"></span>
                <span className="w-2 h-2 rounded-full bg-terracotta-500 animate-bounce"></span>
              </div>
            </div>
          )}

          {/* INACTIVITY NUDGE */}
          {nudgeMessage && (
            <div className="flex items-start justify-start gap-2.5">
              <div className="w-6 h-6 rounded-full bg-terracotta-100 text-terracotta-700 flex items-center justify-center shrink-0 mt-0.5">
                <Bot className="w-3.5 h-3.5" />
              </div>
              <div className="max-w-[85%] rounded-2xl p-3 text-xs sm:text-sm bg-amber-50 text-amber-900 rounded-tl-none border border-amber-200">
                <span className="block text-[10px] font-bold uppercase text-amber-700 mb-0.5">Tutor Prompt</span>
                <p>{nudgeMessage}</p>
              </div>
            </div>
          )}
        </div>

        {/* LLM SUGGESTED RESPONSE HINT */}
        {suggestedResponse && !isAiSpeaking && micState !== 'AI_THINKING' && (
          <div className="pt-2 pb-1">
            <button
              type="button"
              onClick={() => handleUseSuggestion(suggestedResponse)}
              className="w-full text-left p-2.5 rounded-xl bg-amber-50/90 hover:bg-amber-100/90 border border-amber-200/90 transition-all flex items-start gap-2 group cursor-pointer"
            >
              <Lightbulb className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
              <div className="flex-1 min-w-0">
                <span className="block text-[10px] font-bold uppercase tracking-wider text-amber-800">
                  💡 What you could say (Suggestion):
                </span>
                <p className="text-xs text-clay-800 font-medium truncate group-hover:whitespace-normal">
                  "{suggestedResponse}"
                </p>
              </div>
            </button>
          </div>
        )}
      </div>

      {/* 3. Streamlined Hands-Free Voice Control Bar */}
      <div className="card-sand p-4 flex flex-col items-center justify-center space-y-3 bg-gradient-to-t from-sand-100/50 to-white">
        {/* Real-time Voice Waveform Visualizer */}
        <div className="w-full max-w-sm">
          <AudioVisualizer
            energy={micState === 'LISTENING' ? Math.max(audioEnergy, 18) : isAiSpeaking ? 65 : 0}
            isActive={micState === 'LISTENING' || isAiSpeaking}
            mode={isAiSpeaking ? 'ai' : 'user'}
          />
        </div>

        {/* Hands-free Status Pill */}
        <div className="flex items-center gap-2 text-xs font-semibold">
          {micState === 'LISTENING' ? (
            <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200 shadow-sm animate-pulse">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
              <span>{liveTranscript ? `Speaking: "${liveTranscript}"` : 'Listening automatically — speak when ready'}</span>
            </span>
          ) : micState === 'AI_THINKING' ? (
            <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-sand-100 text-clay-700 border border-sand-300">
              <span className="w-2 h-2 rounded-full bg-terracotta-500 animate-ping"></span>
              <span>Partner is replying...</span>
            </span>
          ) : isAiSpeaking ? (
            <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-sand-100 text-clay-700 border border-sand-300">
              <Volume2 className="w-3.5 h-3.5 text-terracotta-600 animate-bounce" />
              <span>AI partner is speaking...</span>
            </span>
          ) : (
            <span className="text-clay-500 text-[11px]">Hands-free auto speech detection active</span>
          )}
        </div>

        {/* Direct Text Form */}
        <form onSubmit={handleSendTextTurn} className="w-full max-w-lg flex items-center gap-2 pt-1">
          <input
            type="text"
            value={typedMessage}
            onChange={(e) => setTypedMessage(e.target.value)}
            placeholder="Speak into your microphone or type a response..."
            className="flex-1 px-4 py-2 text-xs sm:text-sm rounded-xl bg-sand-50 border border-sand-300 focus:outline-none focus:border-terracotta-500 focus:ring-1 focus:ring-terracotta-500"
          />
          <button
            type="submit"
            disabled={!typedMessage.trim() || micState === 'PROCESSING' || micState === 'AI_THINKING'}
            className="p-2.5 rounded-xl bg-terracotta-600 hover:bg-terracotta-700 text-white disabled:opacity-50 transition-colors shadow-warm-sm"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
};
