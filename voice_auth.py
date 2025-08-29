# voice_auth.py
import difflib
import time

try:
    import speech_recognition as sr
except Exception as e:
    raise ImportError(
        "speech_recognition not installed. Install with:\n"
        "pip install SpeechRecognition pyaudio\n\n"
        f"Original error: {e}"
    )

# Tunables
PHRASE_TIME_LIMIT = 5  # seconds to listen
SIMILARITY_THRESHOLD = 0.72  # 0..1; raise to be stricter


def _normalize(s: str) -> str:
    return " ".join((s or "").lower().strip().split())


def _similar(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, _normalize(a), _normalize(b)).ratio()


def verify_phrase(expected_phrase: str):
    """
    Records microphone input, recognizes English speech (Google Web API),
    compares to expected phrase, and returns (ok, similarity).
    """
    expected_phrase = expected_phrase or ""
    if not expected_phrase.strip():
        raise ValueError("Expected phrase is empty")

    r = sr.Recognizer()
    with sr.Microphone() as source:
        # calbration for ambient noise (short)
        r.adjust_for_ambient_noise(source, duration=0.7)
        # small cue beep using print (avoid extra deps)
        print("Beep! Please speak your phrase now…")
        audio = r.listen(source, timeout=6, phrase_time_limit=PHRASE_TIME_LIMIT)

    try:
        text = r.recognize_google(audio)  # requires internet
    except sr.UnknownValueError:
        # nothing recognized
        return (False, 0.0)
    except sr.RequestError as e:
        # API issue; surface a clean error so UI shows a dialog
        raise RuntimeError(f"Speech API error: {e}")

    sim = _similar(text, expected_phrase)
    return (sim >= SIMILARITY_THRESHOLD, float(sim))
