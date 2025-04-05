# YouTube Video Finder with Analysis

This Python project lets users search for YouTube videos using either text or voice input. It filters the results to show only relevant videos and uses Gemini 2.0 Flash to analyze and recommend the best video based on title quality and relevance.

## Features

- Accepts voice or text input (Hindi/English)
- Searches YouTube for videos related to the query
- Filters videos:
  - Duration between 4 to 20 minutes
  - Uploaded in the last 14 days
  - Returns top 20 videos
- Analyzes video titles using Gemini 2.0 Flash (Google LLM)
- Outputs the best video based on title

## Choice 2: YouTube Video Finder with Analysis

- Create an automation that:
  - Accepts voice or text input (Hindi/English)
  - Searches YouTube for relevant videos based on the query
  - Filters the results to:
    - 4-20 minutes in length
    - Posted within the last 14 days
    - Returns top 20 results
  - Analyzes the video titles using Gemini 2.0 Flash or ChatGPT 4o Mini
  - Outputs the best video based on title quality or relevance

- Tech Stack:
  - n8n / Make.com / Python
  - YouTube API
  - LLM for analysis

## Tech Stack Used

- Python
- YouTube Data API
- Google Generative AI (Gemini 2.0 Flash)
- SpeechRecognition (for voice input)
- Optional integration with n8n or Make.com

## Required Python Packages

Make sure to install these packages before running the project:

```bash
pip install google-api-python-client
pip install python-dotenv
pip install google-generativeai
pip install SpeechRecognition
pip install isodate
pip install pyaudio
