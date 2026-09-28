export interface Genre {
  id: number;
  slug: string;
  title: string;
  description: string;
  icon?: string;
  order_index: number;
  unit_count: number;
  session_count: number;
  completed_sessions: number;
  progress_percentage: number;
}

export interface Unit {
  id: number;
  genre_id: number;
  slug: string;
  title: string;
  description: string;
  order_index: number;
  session_count: number;
  completed_sessions: number;
  progress_percentage: number;
}

export interface SessionSummary {
  id: number;
  unit_id: number;
  genre_id: number;
  slug: string;
  title: string;
  description: string;
  difficulty: string;
  cefr_level: string;
  estimated_duration: number;
  target_turns: number;
  order_index: number;
  is_completed: boolean;
  best_score: number | null;
  attempt_count: number;
}

export interface SessionDetail extends SessionSummary {
  scenario: string;
  ai_role: string;
  user_role: string;
  learning_objectives: string[];
  allowed_topics: string[];
  forbidden_topics: string[];
  conversation_stages: string[];
  opening_message: string;
  completion_conditions: string[];
  suggested_vocabulary: string[];
  genre_title?: string;
  unit_title?: string;
}

export interface ConversationTurn {
  id: number;
  attempt_id: number;
  turn_index: number;
  speaker: 'user' | 'ai';
  transcript: string;
  audio_url?: string | null;
  audio_duration: number;
  confidence?: number | null;
  filler_count: number;
  detected_fillers: string[];
  pause_count: number;
  created_at: string;
}

export interface StartSessionResponse {
  attempt_id: number;
  session_id: number;
  status: string;
  opening_message: string;
  ai_role: string;
  user_role: string;
  scenario: string;
  target_turns: number;
  current_stage: number;
  total_stages: number;
  audio_url?: string | null;
  suggested_response?: string | null;
}

export interface UserTurnResponse {
  user_turn: ConversationTurn;
  ai_turn: ConversationTurn;
  current_stage: number;
  total_stages: number;
  turn_count: number;
  is_completed: boolean;
  session_status: string;
  session_guard_passed: boolean;
  ai_audio_url?: string | null;
  suggested_response?: string | null;
}


export interface Correction {
  id?: number;
  user_said: string;
  better_version: string;
  issue: string;
  explanation: string;
  category: string;
}

export interface VocabularyFeedback {
  id?: number;
  word_used: string;
  better_alternative: string;
  reason: string;
  example: string;
}

export interface EvaluationReport {
  id: number;
  attempt_id: number;
  overall_score: number;
  fluency: number;
  accuracy: number;
  grammar: number;
  vocabulary: number;
  pronunciation_estimate: number;
  comprehension: number;
  sentence_formation: number;
  naturalness: number;
  conversation_relevance: number;
  confidence_estimate: number;
  
  estimated_cefr: string;
  cefr_reasoning?: string;
  
  total_speaking_time: number;
  turn_count: number;
  avg_response_words: number;
  
  filler_count: number;
  filler_rate: number;
  most_used_filler?: string;
  filler_breakdown: Record<string, number>;
  repetition_analysis: Record<string, number>;
  
  strengths: string[];
  improvements: string[];
  naturalness_tips: string[];
  recommendations: string[];
  
  corrections: Correction[];
  vocabulary_items: VocabularyFeedback[];
  created_at: string;
}

export interface ProgressSummary {
  total_sessions_completed: number;
  total_speaking_time_minutes: number;
  average_score: number;
  best_score: number;
  latest_score: number;
  current_estimated_cefr: string;
  streak_days: number;
  score_trend: Array<{
    session_num: number;
    overall: number;
    fluency: number;
    accuracy: number;
    grammar: number;
    vocabulary: number;
    date: string;
  }>;
  genre_progress: Array<{
    id: number;
    title: string;
    total_sessions: number;
    completed_sessions: number;
    percentage: number;
  }>;
}

export interface SessionHistoryItem {
  attempt_id: number;
  session_id: number;
  session_title: string;
  genre_title: string;
  unit_title: string;
  difficulty: string;
  status: string;
  started_at: string;
  duration_seconds: number;
  turn_count: number;
  overall_score: number | null;
  estimated_cefr: string | null;
  has_evaluation: boolean;
}

export interface AppSettings {
  stt_model: string;
  llm_model: string;
  tts_voice: string;
  tts_speed: string;
  input_mode: string;
  auto_play_audio: string;
  store_audio: string;
  available_devices: string[];
  current_device: string;
  is_cuda_available: boolean;
}
