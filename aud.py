from flask import Flask, render_template, request, send_file
from pytube import YouTube
import moviepy.editor as mp
import speech_recognition as sr
import logging
import sys
import subprocess
import os
import whisper
from datetime import timedelta
import urllib.request
import urllib.error
from googletrans import Translator


app = Flask(__name__, template_folder='templateFiles', static_folder='static')


@app.route('/')
def index():
    return render_template('index2.html')


@app.route("/download_video", methods=["GET", "POST"])
def download_video():

    url = request.form["url"]
    video = YouTube(url, use_oauth=True, allow_oauth_cache=True)
    download_path = video.streams.get_highest_resolution().download()
    video_path = download_path.split("/")[-1]
    audio_path = "hi.wav"
    clip = mp.VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)

    output_dir = "output_dir"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    command = f"ffmpeg -i {audio_path} -f segment -segment_time 10 -c copy {output_dir}/output_%03d.wav"
    subprocess.call(command, shell=True)

    model = whisper.load_model("base")
    output_files = []
    start_time = timedelta(seconds=0)
    for filename in os.listdir(output_dir):
        if filename.endswith(".wav"):
            # load audio and pad/trim it to fit 30 seconds
            audio = whisper.load_audio(os.path.join(output_dir, filename))
            audio = whisper.pad_or_trim(audio)

            # make log-Mel spectrogram and move to the same device as the model
            mel = whisper.log_mel_spectrogram(audio).to(model.device)

            # detect the spoken language
            _, probs = model.detect_language(mel)
            print(f"Detected language for {filename}: {max(probs, key=probs.get)}")

            # decode the audio
            options = whisper.DecodingOptions(fp16=False)
            result = whisper.decode(model, mel, options)

            # append the recognized text to a list
            end_time = start_time + timedelta(seconds=10)

            # add the transcribed text to the list along with the timing information
            output_files.append(f"{len(output_files) + 1}\n{start_time} --> {end_time}\n{result.text}\n")

            # increment the start time for the next subtitle
            start_time = end_time

    # join the list elements into a single string
    combined_text = "\n".join(output_files)

    # write the combined text to a text file
    with open("output.txt", "w") as f:
        f.write(combined_text)

    # Translate subtitles to Spanish
    translated_subtitles = translate_subtitles(combined_text)

    # write the translated subtitles to a new SRT file
    with open("output_spanish.srt", "w") as f:
        f.write(translated_subtitles)

    return send_file("output_spanish.srt", as_attachment=True)


def translate_subtitles(subtitles_text):
    translator = Translator(service_urls=["translate.google.com"])
    subtitles = subtitles_text.strip().split("\n\n")
    translated_subtitles = []

    for subtitle in subtitles:
        lines = subtitle.split("\n")
        subtitle_number = lines[0]
        subtitle_timing = lines[1]
        subtitle_text = "\n".join(lines[2:])

        translation = translator.translate(subtitle_text, src="en", dest="es")
        translated_text = translation.text
        translated_subtitle = f"{subtitle_number}\n{subtitle_timing}\n{translated_text}\n"
        translated_subtitles.append(translated_subtitle)
        
    translated_srt_text = "\n\n".join(translated_subtitles)
    return translated_srt_text

if __name__ == '__main__':
    app.run(debug=True)
