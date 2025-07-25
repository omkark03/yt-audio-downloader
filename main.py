from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def download_audio():
    data = request.get_json()
    yt_url = data.get("url")

    if not yt_url:
        return jsonify({"error": "Missing 'url'"}), 400

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '/tmp/audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_url])

        file_path = "/tmp/audio.mp3"
        if not os.path.exists(file_path):
            return jsonify({"error": "Audio not found"}), 500

        return (
            open(file_path, "rb").read(),
            200,
            {
                "Content-Type": "audio/mpeg",
                "Content-Disposition": "attachment; filename=audio.mp3"
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
