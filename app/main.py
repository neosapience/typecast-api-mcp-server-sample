import os
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Optional

import httpx
import sounddevice as sd
import soundfile as sf
from mcp.server.fastmcp import FastMCP

API_HOST = os.environ.get("TYPECAST_API_HOST", "https://api.typecast.ai")
API_KEY = os.environ.get("TYPECAST_API_KEY")
OUTPUT_DIR = Path(os.environ.get("TYPECAST_OUTPUT_DIR", os.path.expanduser("~/Downloads/typecast_output")))

# FastMCP 서버 인스턴스 생성
mcp = FastMCP(
    "typecast-api-mcp-server",
    host="0.0.0.0",
    port=8000,
)


class TTSModel(str, Enum):
    SSFM_V21 = "ssfm-v21"


class EmotionEnum(str, Enum):
    NORMAL = "normal"
    SAD = "sad"
    HAPPY = "happy"
    ANGRY = "angry"
    REGRET = "regret"
    URGENT = "urgent"
    WHISPER = "whisper"
    SCREAM = "scream"
    SHOUT = "shout"
    TRUSTFUL = "trustful"
    SOFT = "soft"
    COLD = "cold"
    SARCASM = "sarcasm"
    INSPIRE = "inspire"
    CUTE = "cute"
    CHEER = "cheer"
    CASUAL = "casual"
    TUNELV1 = "tunelv1"
    TUNELV2 = "tunelv2"
    TONEMID = "tonemid"
    TONEUP = "toneup"
    TONEDOWN = "tonedown"


class EmotionPreset(str, Enum):
    HAPPY = "happy"
    SAD = "sad"
    NORMAL = "normal"
    ANGRY = "angry"


@dataclass
class Prompt:
    emotion_preset: EmotionPreset = EmotionPreset.NORMAL
    emotion_intensity: float = 1.0


@dataclass
class Output:
    volume: int = 100
    audio_pitch: int = 0
    audio_tempo: float = 1.0
    audio_format: str = "wav"


@dataclass
class Voice:
    voice_id: str
    voice_name: str
    model: TTSModel
    emotions: List[EmotionEnum]


@dataclass
class TTSRequest:
    voice_id: str
    text: str
    model: TTSModel
    language: Optional[str] = None
    prompt: Optional[Prompt] = None
    output: Optional[Output] = None
    seed: Optional[int] = None


@mcp.tool("get_voices", "Get a list of available voices for text-to-speech")
async def get_voices(model: str = "ssfm-v21") -> dict:
    """Get a list of available voices for text-to-speech

    Args:
        model: Optional filter for specific TTS models.

    Returns:
        List of available voices.
    """
    # 실제 구현에서는 API에서 음성 목록을 가져와야 합니다
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_HOST}/v1/voices?model={model}")
        if response.status_code != 200:
            raise Exception(f"Failed to get voices: {response.status_code}")
        return response.json()


@mcp.tool("text_to_speech", "Convert text to speech using the specified voice and parameters")
async def text_to_speech(voice_id: str, text: str, model: str, emotion_preset: str = EmotionPreset.NORMAL, emotion_intensity: float = 1.0) -> str:
    """Convert text to speech using the specified voice and parameters

    Args:
        voice_id: ID of the voice to use
        text: Text to convert to speech
        model: TTS model to use
        emotion_preset: Emotion preset to use
        emotion_intensity: Emotion intensity to use

    Returns:
        Path to the saved audio file
    """
    # 출력 디렉토리가 없으면 생성
    if not OUTPUT_DIR.exists():
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    headers = {
        "X-API-KEY": API_KEY,
    }
    prompt = {
        "emotion_preset": emotion_preset,
        "emotion_intensity": emotion_intensity,
    }
    payload = {
        "voice_id": voice_id,
        "text": text,
        "model": model,
        "prompt": prompt,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_HOST}/v1/text-to-speech",
            json=payload,
            headers=headers,
        )
        if response.status_code != 200:
            raise Exception(f"Failed to generate speech: {response.status_code}, {response.text}")

        # 파일명 생성 (텍스트의 처음 20자를 사용)
        output_path = OUTPUT_DIR / f"{voice_id}_{datetime.now().strftime('%Y%m%d-%H%M%S')}_{text[:10]}.wav"

        # 파일로 저장
        output_path.write_bytes(response.content)

        return str(output_path)


@mcp.tool("play_audio", "Play the generated audio file")
async def play_audio(file_path: str) -> str:
    """Play the audio file at the specified path

    Args:
        file_path: Path to the audio file to play

    Returns:
        Status message
    """
    try:
        # 오디오 파일 읽기
        data, samplerate = sf.read(file_path)

        # 오디오 재생
        sd.play(data, samplerate)
        sd.wait()  # 재생이 끝날 때까지 대기

        return f"Successfully played audio file: {file_path}"
    except Exception as e:
        return f"Failed to play audio file: {str(e)}"


def main():
    mcp.run()


if __name__ == "__main__":
    main()
