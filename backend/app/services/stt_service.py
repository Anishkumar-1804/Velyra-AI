import io
import os
import tempfile
import logging
from typing import Dict, Any, Optional
from backend.app.config import settings
from backend.app.utils.audio import detect_filler_words, estimate_speech_duration_from_words
from backend.app.utils.timing import timed_block

logger = logging.getLogger("angiyam.stt")


class STTService:
    """
    Local Speech-To-Text Service using faster-whisper.
    Lazy loads the model on first audio transcription.
    """
    def __init__(self):
        self._model = None
        self.model_name = settings.STT_MODEL

    def _get_model(self):
        if self._model is None:
            logger.info(f"[STT] Loading faster-whisper model '{self.model_name}' on device '{settings.DEVICE}'...")
            try:
                from faster_whisper import WhisperModel
                # Auto compute type: float16 on CUDA, int8 on CPU
                device = "cuda" if settings.DEVICE == "cuda" else ("cpu" if settings.DEVICE == "cpu" else "auto")
                compute_type = "float16" if device == "cuda" else "int8"
                
                self._model = WhisperModel(
                    self.model_name,
                    device=device,
                    compute_type=compute_type,
                    download_root=str(settings.MODELS_DIR)
                )
                logger.info("[STT] faster-whisper model loaded successfully.")
            except Exception as e:
                logger.warning(f"[STT] Could not initialize faster-whisper ({e}). Using robust fallback processor.")
                self._model = "fallback"
        return self._model

    def warmup(self):
        """Warm up STT model."""
        try:
            self._get_model()
            logger.info("[STT] STT warmup completed.")
        except Exception as e:
            logger.warning(f"[STT] Warmup notice: {e}")



    def transcribe_audio(self, audio_bytes: bytes, filename: str = "audio.wav") -> Dict[str, Any]:
        """
        Transcribe raw audio bytes into text, calculate duration, and extract filler words.
        """
        if not audio_bytes or len(audio_bytes) < 100:
            return {
                "transcript": "",
                "duration": 0.0,
                "confidence": 0.0,
                "filler_count": 0,
                "detected_fillers": [],
                "filler_breakdown": {},
                "pause_count": 0,
            }

        with timed_block("STT_Transcription"):
            model = self._get_model()
            
            # Save bytes to a temp file for faster-whisper
            suffix = os.path.splitext(filename)[1] or ".wav"
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                tmp.write(audio_bytes)
                tmp_path = tmp.name

            try:
                transcript_text = ""
                avg_confidence = 0.85
                duration = 0.0
                pause_count = 0

                if model != "fallback":
                    segments, info = model.transcribe(
                        tmp_path,
                        beam_size=5,
                        language="en",
                        vad_filter=True,
                        vad_parameters=dict(min_silence_duration_ms=500)
                    )
                    
                    seg_list = list(segments)
                    transcript_text = " ".join([seg.text.strip() for seg in seg_list]).strip()
                    duration = info.duration if hasattr(info, "duration") else 0.0
                    
                    if seg_list:
                        confs = [getattr(seg, "avg_logprob", -0.2) for seg in seg_list]
                        avg_confidence = max(0.5, min(1.0, 1.0 + sum(confs) / (len(confs) * 2)))
                        # Count pauses between segments > 1.2 seconds
                        for i in range(len(seg_list) - 1):
                            gap = seg_list[i + 1].start - seg_list[i].end
                            if gap > 1.2:
                                pause_count += 1
                else:
                    # If faster-whisper is not initialized, calculate duration from audio bytes with no synthetic text
                    logger.info("[STT] Audio received without faster-whisper binary. Returning silence/unrecognized audio.")
                    duration = max(1.0, len(audio_bytes) / 32000.0)
                    transcript_text = ""

                if duration <= 0.0:
                    duration = estimate_speech_duration_from_words(transcript_text)

                filler_count, detected_fillers, filler_breakdown = detect_filler_words(transcript_text)

                logger.info(f"[STT] Transcript: '{transcript_text}' ({duration:.1f}s, {filler_count} fillers)")

                return {
                    "transcript": transcript_text,
                    "duration": round(duration, 2),
                    "confidence": round(avg_confidence, 2),
                    "filler_count": filler_count,
                    "detected_fillers": detected_fillers,
                    "filler_breakdown": filler_breakdown,
                    "pause_count": pause_count,
                }
            except Exception as e:
                logger.error(f"[STT] Error during transcription: {e}")
                duration = estimate_speech_duration_from_words("")
                return {
                    "transcript": "",
                    "duration": 0.0,
                    "confidence": 0.0,
                    "filler_count": 0,
                    "detected_fillers": [],
                    "filler_breakdown": {},
                    "pause_count": 0,
                }
            finally:
                if os.path.exists(tmp_path):
                    try:
                        os.remove(tmp_path)
                    except Exception:
                        pass


stt_service = STTService()
