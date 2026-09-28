import axios from 'axios';
import {
  Genre,
  Unit,
  SessionSummary,
  SessionDetail,
  StartSessionResponse,
  UserTurnResponse,
  ConversationTurn,
  EvaluationReport,
  ProgressSummary,
  SessionHistoryItem,
  AppSettings
} from '../types';

const API_BASE = '/api';

const client = axios.create({
  baseURL: API_BASE,
  timeout: 60000,
});

export const api = {
  // Genres & Curriculum
  getGenres: async (): Promise<Genre[]> => {
    const res = await client.get('/genres');
    return res.data;
  },

  getGenre: async (id: number): Promise<Genre & { units: Unit[] }> => {
    const res = await client.get(`/genres/${id}`);
    return res.data;
  },

  getUnit: async (id: number): Promise<Unit & { genre_title?: string; sessions: SessionSummary[] }> => {
    const res = await client.get(`/units/${id}`);
    return res.data;
  },

  getSessionDetail: async (id: number): Promise<SessionDetail> => {
    const res = await client.get(`/sessions/${id}`);
    return res.data;
  },

  // Conversation Live Loop
  startSession: async (sessionId: number): Promise<StartSessionResponse> => {
    const res = await client.post('/conversation/start', { session_id: sessionId });
    return res.data;
  },

  sendAudioTurn: async (attemptId: number, audioBlob: Blob, liveTranscript?: string): Promise<UserTurnResponse> => {
    const formData = new FormData();
    formData.append('attempt_id', attemptId.toString());
    formData.append('audio_file', audioBlob, 'mic_recording.wav');
    if (liveTranscript && liveTranscript.trim()) {
      formData.append('transcript', liveTranscript.trim());
    }
    
    const res = await client.post('/conversation/turn/audio', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return res.data;
  },

  sendTextTurn: async (attemptId: number, transcript: string): Promise<UserTurnResponse> => {
    const formData = new FormData();
    formData.append('attempt_id', attemptId.toString());
    formData.append('transcript', transcript);
    
    const res = await client.post('/conversation/turn/text', formData);
    return res.data;
  },

  endSessionAttempt: async (attemptId: number): Promise<{ message: string; attempt_id: number }> => {
    const res = await client.post(`/conversation/attempt/${attemptId}/end`);
    return res.data;
  },

  getAttemptTurns: async (attemptId: number): Promise<ConversationTurn[]> => {
    const res = await client.get(`/conversation/attempt/${attemptId}/turns`);
    return res.data;
  },

  getSilenceNudge: async (attemptId: number): Promise<{ nudge_text: string; audio_url: string }> => {
    const res = await client.post(`/conversation/attempt/${attemptId}/nudge`);
    return res.data;
  },


  // Evaluation & Results
  evaluateAttempt: async (attemptId: number): Promise<EvaluationReport> => {
    const res = await client.post(`/evaluation/attempt/${attemptId}`);
    return res.data;
  },

  getEvaluation: async (attemptId: number): Promise<EvaluationReport> => {
    const res = await client.get(`/evaluation/attempt/${attemptId}`);
    return res.data;
  },

  // Progress & History
  getProgressSummary: async (): Promise<ProgressSummary> => {
    const res = await client.get('/progress/summary');
    return res.data;
  },

  getSessionHistory: async (): Promise<SessionHistoryItem[]> => {
    const res = await client.get('/progress/history');
    return res.data;
  },

  // Settings & Management
  getSettings: async (): Promise<AppSettings> => {
    const res = await client.get('/settings');
    return res.data;
  },

  updateSettings: async (updates: Partial<AppSettings>): Promise<AppSettings> => {
    const res = await client.put('/settings', updates);
    return res.data;
  },

  resetAllProgress: async (): Promise<{ message: string }> => {
    const res = await client.delete('/settings/reset');
    return res.data;
  }
};
