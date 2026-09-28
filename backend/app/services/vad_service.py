import logging
import numpy as np
from typing import Dict, Any

logger = logging.getLogger("angiyam.vad")


class VADService:
    """
    Voice Activity Detection service.
    Analyzes audio chunks to determine speech presence, energy, and end-of-speech silence.
    """
    def __init__(self, energy_threshold: float = 0.015):
        self.energy_threshold = energy_threshold

    def is_speech_present(self, audio_data: np.ndarray) -> bool:
        """Calculate Root Mean Square (RMS) energy to detect speech."""
        if audio_data is None or len(audio_data) == 0:
            return False
        
        rms = np.sqrt(np.mean(np.square(audio_data)))
        return float(rms) > self.energy_threshold

    def analyze_audio_stream(self, audio_bytes: bytes) -> Dict[str, Any]:
        """Analyze raw audio bytes for speech activity."""
        try:
            # Convert 16-bit PCM bytes to float array
            audio_array = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
            has_speech = self.is_speech_present(audio_array)
            rms = float(np.sqrt(np.mean(np.square(audio_array)))) if len(audio_array) > 0 else 0.0
            return {
                "has_speech": has_speech,
                "energy": round(rms, 4),
                "samples": len(audio_array)
            }
        except Exception as e:
            logger.debug(f"[VAD] Stream parse error: {e}")
            return {"has_speech": True, "energy": 0.05, "samples": 0}


vad_service = VADService()
