import { useState, useRef, useEffect, useCallback } from 'react';

interface UseAudioRecorderOptions {
  onSpeechEnd?: (blob: Blob | null, transcript: string) => void;
  onInactivityTimeout?: () => void;
  silenceThresholdMs?: number;
  inactivityTimeoutMs?: number;
}

interface AudioRecorderHook {
  isRecording: boolean;
  liveTranscript: string;
  audioBlob: Blob | null;
  audioUrl: string | null;
  audioEnergy: number;
  duration: number;
  error: string | null;
  startRecording: () => Promise<void>;
  stopRecording: () => Promise<{ blob: Blob | null; transcript: string }>;
  resetAudio: () => void;
  stopAll: () => void;
}

export function useAudioRecorder(options?: UseAudioRecorderOptions): AudioRecorderHook {
  const [isRecording, setIsRecording] = useState(false);
  const [liveTranscript, setLiveTranscript] = useState<string>('');
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [audioEnergy, setAudioEnergy] = useState<number>(0);
  const [duration, setDuration] = useState<number>(0);
  const [error, setError] = useState<string | null>(null);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const streamRef = useRef<MediaStream | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const animFrameRef = useRef<number | null>(null);
  const timerRef = useRef<number | null>(null);

  // Silence & Inactivity detection timers
  const speechEndTimerRef = useRef<number | null>(null);
  const inactivityTimerRef = useRef<number | null>(null);
  const hasSpokenRef = useRef<boolean>(false);

  // Live Web Speech Recognition
  const speechRecognitionRef = useRef<any>(null);
  const finalTranscriptRef = useRef<string>('');

  const isStoppingRef = useRef<boolean>(false);
  const silenceThresholdMs = options?.silenceThresholdMs ?? 1500;
  const inactivityTimeoutMs = options?.inactivityTimeoutMs ?? 9500;

  // Fully stop all audio capture, recognition, and tracks
  const stopAll = useCallback(() => {
    isStoppingRef.current = true;
    hasSpokenRef.current = false;

    if (speechEndTimerRef.current) {
      clearTimeout(speechEndTimerRef.current);
      speechEndTimerRef.current = null;
    }
    if (inactivityTimerRef.current) {
      clearTimeout(inactivityTimerRef.current);
      inactivityTimerRef.current = null;
    }

    if (speechRecognitionRef.current) {
      try {
        speechRecognitionRef.current.onresult = null;
        speechRecognitionRef.current.onerror = null;
        speechRecognitionRef.current.onend = null;
        speechRecognitionRef.current.stop();
      } catch (e) {}
      speechRecognitionRef.current = null;
    }

    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      try {
        mediaRecorderRef.current.stop();
      } catch (e) {}
    }
    mediaRecorderRef.current = null;

    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => {
        try {
          track.stop();
        } catch (e) {}
      });
      streamRef.current = null;
    }

    if (audioContextRef.current && audioContextRef.current.state !== 'closed') {
      try {
        audioContextRef.current.close();
      } catch (e) {}
      audioContextRef.current = null;
    }

    if (animFrameRef.current) {
      cancelAnimationFrame(animFrameRef.current);
      animFrameRef.current = null;
    }

    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }

    setIsRecording(false);
    setAudioEnergy(0);
  }, []);

  const stopRecording = useCallback(async (): Promise<{ blob: Blob | null; transcript: string }> => {
    return new Promise((resolve) => {
      // Clear timers
      if (speechEndTimerRef.current) {
        clearTimeout(speechEndTimerRef.current);
        speechEndTimerRef.current = null;
      }
      if (inactivityTimerRef.current) {
        clearTimeout(inactivityTimerRef.current);
        inactivityTimerRef.current = null;
      }

      // Stop Speech Recognition
      if (speechRecognitionRef.current) {
        try {
          speechRecognitionRef.current.stop();
        } catch (e) {}
      }

      const capturedTranscript = (finalTranscriptRef.current || liveTranscript).trim();

      if (!mediaRecorderRef.current || mediaRecorderRef.current.state === 'inactive') {
        setIsRecording(false);
        resolve({ blob: null, transcript: capturedTranscript });
        return;
      }

      mediaRecorderRef.current.onstop = () => {
        const blob = audioChunksRef.current.length > 0 ? new Blob(audioChunksRef.current, { type: 'audio/wav' }) : null;
        if (blob) {
          const url = URL.createObjectURL(blob);
          setAudioBlob(blob);
          setAudioUrl(url);
        }
        setIsRecording(false);
        setAudioEnergy(0);

        if (streamRef.current) {
          streamRef.current.getTracks().forEach((track) => track.stop());
          streamRef.current = null;
        }

        if (animFrameRef.current) {
          cancelAnimationFrame(animFrameRef.current);
          animFrameRef.current = null;
        }

        if (timerRef.current) {
          clearInterval(timerRef.current);
          timerRef.current = null;
        }

        resolve({ blob, transcript: capturedTranscript });
      };

      try {
        mediaRecorderRef.current.stop();
      } catch (err) {
        console.error('Error stopping MediaRecorder:', err);
        setIsRecording(false);
        resolve({ blob: null, transcript: capturedTranscript });
      }
    });
  }, [liveTranscript]);

  const triggerSpeechEnd = useCallback(async () => {
    if (isStoppingRef.current || !hasSpokenRef.current) return;
    isStoppingRef.current = true;

    // Clear timers
    if (speechEndTimerRef.current) {
      clearTimeout(speechEndTimerRef.current);
      speechEndTimerRef.current = null;
    }
    if (inactivityTimerRef.current) {
      clearTimeout(inactivityTimerRef.current);
      inactivityTimerRef.current = null;
    }

    const result = await stopRecording();
    const transcript = (result.transcript || '').trim();

    // STRICT CHECK: Only dispatch turn if actual real words were spoken (>2 chars)
    if (transcript.length >= 2) {
      console.log('[AudioRecorder] Real speech detected. Submitting turn:', transcript);
      options?.onSpeechEnd?.(result.blob, transcript);
    } else {
      console.log('[AudioRecorder] Silence or ambient noise detected without speech. Resetting listener...');
      // Reset state for new utterance
      hasSpokenRef.current = false;
      isStoppingRef.current = false;
      finalTranscriptRef.current = '';
      setLiveTranscript('');
      audioChunksRef.current = [];
    }
  }, [options, stopRecording]);

  const startRecording = useCallback(async () => {
    // Stop any existing stream / recognition first to prevent cross-turn leak
    if (speechRecognitionRef.current) {
      try {
        speechRecognitionRef.current.abort();
      } catch (e) {}
      speechRecognitionRef.current = null;
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }

    setError(null);
    setAudioBlob(null);
    setAudioUrl(null);
    setLiveTranscript('');
    finalTranscriptRef.current = '';
    hasSpokenRef.current = false;
    isStoppingRef.current = false;
    setDuration(0);
    audioChunksRef.current = [];

    // Clear any previous timers
    if (speechEndTimerRef.current) {
      clearTimeout(speechEndTimerRef.current);
      speechEndTimerRef.current = null;
    }
    if (inactivityTimerRef.current) {
      clearTimeout(inactivityTimerRef.current);
      inactivityTimerRef.current = null;
    }

    // Inactivity prompt timer
    if (options?.onInactivityTimeout) {
      inactivityTimerRef.current = window.setTimeout(() => {
        if (!hasSpokenRef.current && !isStoppingRef.current) {
          console.log('[AudioRecorder] Inactivity timeout reached. Triggering nudge...');
          options.onInactivityTimeout?.();
        }
      }, inactivityTimeoutMs);
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      });
      streamRef.current = stream;

      // Initialize Web Speech API for fresh turn recognition
      const SpeechRecognition =
        (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

      if (SpeechRecognition) {
        try {
          const recognition = new SpeechRecognition();
          recognition.continuous = true;
          recognition.interimResults = true;
          recognition.lang = 'en-IN';

          recognition.onresult = (event: any) => {
            if (isStoppingRef.current) return;

            let interim = '';
            let final = '';

            for (let i = 0; i < event.results.length; ++i) {
              const transcriptPiece = event.results[i][0].transcript;
              if (event.results[i].isFinal) {
                final += transcriptPiece + ' ';
              } else {
                interim += transcriptPiece;
              }
            }

            finalTranscriptRef.current = final;
            const fullLive = (final + ' ' + interim).trim();
            setLiveTranscript(fullLive);

            if (fullLive.length >= 2) {
              hasSpokenRef.current = true;
              if (inactivityTimerRef.current) {
                clearTimeout(inactivityTimerRef.current);
                inactivityTimerRef.current = null;
              }

              if (speechEndTimerRef.current) {
                clearTimeout(speechEndTimerRef.current);
              }

              speechEndTimerRef.current = window.setTimeout(() => {
                triggerSpeechEnd();
              }, silenceThresholdMs);
            }
          };

          recognition.onerror = (e: any) => {
            console.debug('Speech recognition event:', e.error);
          };

          recognition.start();
          speechRecognitionRef.current = recognition;
        } catch (err) {
          console.debug('Speech init notice:', err);
        }
      }

      // AudioContext for Energy/Visualizer
      const AudioCtx = window.AudioContext || (window as any).webkitAudioContext;
      const audioCtx = new AudioCtx();
      audioContextRef.current = audioCtx;
      const source = audioCtx.createMediaStreamSource(stream);
      const analyser = audioCtx.createAnalyser();
      analyser.fftSize = 256;
      source.connect(analyser);
      analyserRef.current = analyser;

      const bufferLength = analyser.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);

      const updateEnergy = () => {
        if (!analyserRef.current || isStoppingRef.current) return;
        analyserRef.current.getByteFrequencyData(dataArray);

        let sum = 0;
        for (let i = 0; i < bufferLength; i++) {
          sum += dataArray[i];
        }
        const avg = sum / bufferLength;
        const normalized = Math.min(100, Math.round((avg / 128) * 100));
        setAudioEnergy(normalized);

        // Track voice energy
        if (normalized > 25 && finalTranscriptRef.current.trim().length >= 2) {
          hasSpokenRef.current = true;
          if (inactivityTimerRef.current) {
            clearTimeout(inactivityTimerRef.current);
            inactivityTimerRef.current = null;
          }
        }

        animFrameRef.current = requestAnimationFrame(updateEnergy);
      };
      updateEnergy();

      // Setup MediaRecorder
      const options_mr = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
        ? { mimeType: 'audio/webm;codecs=opus' }
        : {};

      const mediaRecorder = new MediaRecorder(stream, options_mr);
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.start(100);
      setIsRecording(true);

      timerRef.current = window.setInterval(() => {
        setDuration((prev) => prev + 1);
      }, 1000);
    } catch (err: any) {
      console.error('Microphone error:', err);
      if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
        setError('Microphone permission was denied. Please allow microphone access in your browser settings.');
      } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
        setError('No microphone found. Please connect a working microphone.');
      } else {
        setError('Could not access microphone. Please check your browser audio settings.');
      }
      setIsRecording(false);
    }
  }, [inactivityTimeoutMs, options, silenceThresholdMs, triggerSpeechEnd]);

  const resetAudio = useCallback(() => {
    setAudioBlob(null);
    setAudioUrl(null);
    setLiveTranscript('');
    finalTranscriptRef.current = '';
    hasSpokenRef.current = false;
    setDuration(0);
    setError(null);
    setAudioEnergy(0);
    if (speechEndTimerRef.current) clearTimeout(speechEndTimerRef.current);
    if (inactivityTimerRef.current) clearTimeout(inactivityTimerRef.current);
  }, []);

  // Teardown cleanup on hook unmount
  useEffect(() => {
    return () => {
      stopAll();
    };
  }, [stopAll]);

  return {
    isRecording,
    liveTranscript,
    audioBlob,
    audioUrl,
    audioEnergy,
    duration,
    error,
    startRecording,
    stopRecording,
    resetAudio,
    stopAll,
  };
}
