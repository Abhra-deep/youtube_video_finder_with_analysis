# ========================== REQUIRED MODULES ========================== #
# Install these using pip before running the program.
# Each module has a specific purpose in this automation project.

# Used to load secret API keys from a .env file (for security).
# pip install python-dotenv
import os
from dotenv import load_dotenv

# Allows capturing voice input and converting it to text.
# pip install SpeechRecognition
import speech_recognition as sr

# Required by SpeechRecognition to access the microphone.
# pip install pyaudio
# Note: On Windows, you may need to install PyAudio manually from:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# Example: pip install PyAudio‑0.2.11‑cp311‑cp311‑win_amd64.whl

# Allows access to YouTube Data API for searching and retrieving videos.
# pip install google-api-python-client
from googleapiclient.discovery import build

# Helps parse YouTube video duration from ISO 8601 format to seconds/minutes.
# pip install isodate
import isodate

# Official Python client for Google's Gemini models (e.g., Gemini 1.5 Flash).
# pip install google-generativeai
import google.generativeai as genai

# Built-in module for handling dates and times.
import datetime


# Load API keys from .env file
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini 2.0 Flash Model
genai.configure(api_key=GEMINI_API_KEY)
gemini_flash = genai.GenerativeModel("gemini-1.5-flash")

# Function to capture voice input from microphone
def get_voice_query():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="en-IN")
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
    return None

# Function to get text input from user
def get_text_query():
    return input("Enter your search query: ")

# Function to search YouTube using API
def fetch_video_ids(search_term):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    # Calculate date 14 days ago in required format
    recent_date = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=14)).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Perform YouTube search
    response = youtube.search().list(
        q=search_term,
        part="id,snippet",
        maxResults=50,
        type="video",
        publishedAfter=recent_date
    ).execute()

    # Extract video IDs
    ids = [item["id"]["videoId"] for item in response["items"]]
    return ids[:20]  # Return only top 20 results

# Function to get video title and duration
def fetch_video_metadata(video_ids):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    details = youtube.videos().list(
        part="snippet,contentDetails",
        id=",".join(video_ids)
    ).execute()

    video_data = []
    for item in details["items"]:
        title = item["snippet"]["title"]
        video_id = item["id"]
        duration_iso = item["contentDetails"]["duration"]

        # Convert ISO duration (e.g., PT10M5S) to minutes
        total_seconds = isodate.parse_duration(duration_iso).total_seconds()
        minutes = total_seconds / 60

        video_data.append({
            "title": title,
            "video_id": video_id,
            "duration": minutes
        })

    return video_data

# Function to filter out videos not within 4–20 minutes
def filter_shortlist_videos(videos):
    return [video for video in videos if 4 <= video["duration"] <= 20]

# Function to find best video using Gemini model
def choose_best_video_title(video_list):
    prompt = (
        "You are an assistant that helps pick the best YouTube video for a topic.\n"
        "From the following list of titles and video IDs, pick the most informative and relevant one:\n\n"
    )
    for video in video_list:
        prompt += f"- {video['title']} (ID: {video['video_id']})\n"

    # Send prompt to Gemini and get result
    result = gemini_flash.generate_content(prompt)
    return result.text.strip()

# Main function to run the app
def main():
    # Ask user for input mode
    mode = input("Choose input mode - (1) Voice (2) Text: ")

    # Get query based on selected input mode
    if mode == "1":
        query = get_voice_query()
    else:
        query = get_text_query()

    if not query:
        print("No input provided. Exiting.")
        return

    print("Searching YouTube...")
    video_ids = fetch_video_ids(query)
    video_metadata = fetch_video_metadata(video_ids)
    shortlisted = filter_shortlist_videos(video_metadata)

    if not shortlisted:
        print("No videos found with required criteria.")
        return

    print("Analyzing titles...")
    recommendation = choose_best_video_title(shortlisted)
    print("\nBest Video Recommendation:\n", recommendation)

# Run the main function
if __name__ == "__main__":
    main()
