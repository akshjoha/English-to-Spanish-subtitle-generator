# English-to-Spanish-Subtitle-Generator

This is a simple web application built using Flask, a Python web framework. The application allows users to download YouTube videos and get their subtitles translated to Spanish. Here's a brief explanation of how it works:

The application has two routes:

The root route ("/") displays an HTML page where users can input the YouTube URL they want to download and translate.
The "/download_video" route is triggered when the user submits the URL from the form on the root page.
When the user submits a YouTube URL, the application performs the following steps:

Downloads the highest-resolution version of the video using the pytube library.
Extracts the audio from the video and saves it as a WAV file using moviepy.editor.
Splits the audio into smaller 10-second segments using ffmpeg.
Processes each audio segment through a pre-trained Whisper ASR model to transcribe the speech to text. The detected language for each segment is also printed.
Combines the transcriptions and timing information into a text file and saves it as "output.txt".
After obtaining the transcriptions, the application proceeds to translate the subtitles to Spanish using the googletrans library.

The translated subtitles are then saved into a new SRT (SubRip Subtitle) file named "output_spanish.srt".

Finally, the translated SRT file is sent as a download attachment to the user's web browser.

When you run the application locally with app.run(debug=True), it will start a web server on your computer, allowing you to access the application through your web browser. The server is set to run in debug mode, so any errors will be displayed in the browser for easier debugging during development.

In summary, this Flask web app lets users download YouTube videos and obtain the video's speech as transcribed text, which is then translated to Spanish and provided as a downloadable SRT subtitle file.

# Screenshorts

![image](https://github.com/akshjoha/English-to-Spanish-subtitle-generator/assets/74461670/b105a9d8-0ecd-4b9d-bea0-31ca51d8effa)

![image](https://github.com/akshjoha/English-to-Spanish-subtitle-generator/assets/74461670/6647e7e5-6b2d-433e-8495-7cc641733957)

![image](https://github.com/akshjoha/English-to-Spanish-subtitle-generator/assets/74461670/56630824-70ac-4f71-b177-310d62140b35)


