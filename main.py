# main.py

from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def download_audio():
    data = request.get_json()
    video_url = data.get("video_url")

    if not video_url:
        return {"error": "Missing video_url"}, 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloaded_audio.%(ext)s',
        'cookiefile': 'cookies.txt',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return send_file("downloaded_audio.mp3", as_attachment=True)
    except Exception as e:
        return {"error": str(e)}, 500

# THIS is the critical part for Cloud Run
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
