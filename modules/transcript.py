import re
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str) -> str:
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    if match:
        return match.group(1)
    raise ValueError("Invalid YouTube URL")


def get_transcript(url: str, language="en"):
    video_id = extract_video_id(url)

    try:
        # Try preferred language
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=[language]
        )

    except Exception:
        try:
            transcripts = YouTubeTranscriptApi.list_transcripts(video_id)

            # Try any generated transcript
            transcript_obj = None
            for t in transcripts:
                transcript_obj = t
                break

            if transcript_obj is None:
                raise Exception("No transcripts available")

            transcript = transcript_obj.fetch()

        except Exception as e:
            raise Exception(
                "❌ Could not retrieve transcript.\n"
                "Possible reasons:\n"
                "- Video has no captions\n"
                "- Captions are restricted\n"
                "- YouTube blocked the request temporarily\n"
                f"\nError: {str(e)}"
            )

    if not transcript:
        raise Exception("❌ Empty transcript received")

    text = " ".join([t.get("text", "") for t in transcript])

    return {
        "text": text,
        "segments": transcript
    }
