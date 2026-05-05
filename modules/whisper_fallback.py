from faster_whisper import WhisperModel
import yt_dlp

model = WhisperModel("base")


def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)


def transcribe_audio(file_path):
    segments, _ = model.transcribe(file_path)

    text = ""
    result_segments = []

    for seg in segments:
        text += seg.text + " "
        result_segments.append({
            "text": seg.text,
            "start": seg.start
        })

    return {
        "text": text,
        "segments": result_segments
    }


def get_transcript_whisper(url):
    audio_path = download_audio(url)
    return transcribe_audio(audio_path)