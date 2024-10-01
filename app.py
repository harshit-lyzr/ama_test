from youtube_transcript_api import YouTubeTranscriptApi
import streamlit as st

def get_transcript(video_id):
    try:
        # Fetch the transcript using the video ID
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        paragraphs = []
        paragraph = ""
        paragraph_start = 0
        paragraph_duration = 0

        for i, entry in enumerate(transcript):
            start_time = entry['start']
            duration = entry['duration']
            text = entry['text']

            # If paragraph is empty, mark start time of this paragraph
            if not paragraph:
                paragraph_start = start_time

            # Add text and update duration
            if len(paragraph) + len(text) + 1 <= 200:
                paragraph += " " + text
                paragraph_duration = (start_time + duration) - paragraph_start
            else:
                # Append the paragraph to result with the start and duration fields
                paragraphs.append({
                    'text': paragraph.strip(),
                    'start': paragraph_start,
                    'duration': paragraph_duration
                })
                # Start a new paragraph
                paragraph = text
                paragraph_start = start_time
                paragraph_duration = duration

        # Add the last paragraph
        if paragraph:
            paragraphs.append({
                'text': paragraph.strip(),
                'start': paragraph_start,
                'duration': paragraph_duration
            })
        print(paragraphs)
        return paragraphs

    except Exception as e:
        return str(e)

video_id = st.text_input("entr")

if video_id:
    transcript = get_transcript(video_id)
    st.markdown(transcript)