import os
import hashlib
import asyncio
import logging
from typing import Optional, Dict
from backend.app.config import settings
from backend.app.utils.timing import timed_block

logger = logging.getLogger("angiyam.tts")


class TTSService:
    """
    Text-to-Speech Service providing natural Indian English voices.
    Uses edge-tts Neural voices with pyttsx3 offline fallback and local audio caching.
    """
    def __init__(self):
        self.default_voice = settings.TTS_VOICE  # 'en-IN-NeerjaNeural' or 'en-IN-PrabhatNeural'
        self.cache_dir = settings.AUDIO_DIR / "tts_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_key(self, text: str, voice: str, rate: float) -> str:
        """Create unique hash for audio caching."""
        h = hashlib.md5(f"{text}_{voice}_{rate}".encode("utf-8")).hexdigest()
        return f"{h}.mp3"

    async def generate_speech_async(self, text: str, voice: Optional[str] = None, speed: float = 1.0) -> Optional[str]:
        """
        Generate natural Indian English speech audio and return the relative static URL.
        """
        if not text or not text.strip():
            return None

        clean_text = text.strip()
        selected_voice = voice or self.default_voice
        filename = self._get_cache_key(clean_text, selected_voice, speed)
        filepath = self.cache_dir / filename

        # Check cache
        if filepath.exists() and filepath.stat().st_size > 500:
            return f"/api/audio/file/{filename}"

        with timed_block("TTS_Generation"):
            # Format speed rate for edge-tts (e.g. "+0%", "+25%", "-25%")
            rate_percent = int((speed - 1.0) * 100)
            rate_str = f"+{rate_percent}%" if rate_percent >= 0 else f"{rate_percent}%"

            # 1. Try edge-tts for natural Indian English neural audio
            try:
                import edge_tts
                communicate = edge_tts.Communicate(clean_text, selected_voice, rate=rate_str)
                await communicate.save(str(filepath))
                logger.info(f"[TTS] Generated neural voice audio for: '{clean_text[:40]}...' using {selected_voice}")
                return f"/api/audio/file/{filename}"
            except Exception as e:
                logger.warning(f"[TTS] edge-tts error ({e}). Trying offline system TTS fallback...")

            # 2. Offline pyttsx3 fallback
            try:
                wav_filename = filename.replace(".mp3", ".wav")
                wav_filepath = self.cache_dir / wav_filename
                
                import pyttsx3
                engine = pyttsx3.init()
                # Adjust speech rate (pyttsx3 default is ~200)
                engine.setProperty("rate", int(175 * speed))
                
                # Check available voices for Indian English or standard English
                voices = engine.getProperty("voices")
                for v in voices:
                    v_name = v.name.lower()
                    if "india" in v_name or "hindi" in v_name or "en-in" in v_name:
                        engine.setProperty("voice", v.id)
                        break
                        
                engine.save_to_file(clean_text, str(wav_filepath))
                engine.runAndWait()
                logger.info(f"[TTS] pyttsx3 offline speech generated: {wav_filename}")
                return f"/api/audio/file/{wav_filename}"
            except Exception as e2:
                logger.error(f"[TTS] All TTS engines failed: {e2}")
                return None

    def generate_speech(self, text: str, voice: Optional[str] = None, speed: float = 1.0) -> Optional[str]:
        """Synchronous wrapper for generate_speech_async."""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # In an existing async event loop
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    future = pool.submit(asyncio.run, self.generate_speech_async(text, voice, speed))
                    return future.result()
            else:
                return loop.run_until_complete(self.generate_speech_async(text, voice, speed))
        except Exception:
            return asyncio.run(self.generate_speech_async(text, voice, speed))


tts_service = TTSService()
