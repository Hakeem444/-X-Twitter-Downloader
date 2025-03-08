import os 
import re
import yt_dlp
from flask import Flask, request, render_template, jsonify 

app = Flask (__name__)

def is_valid_twitter_url(url):
    pattern = r"(https?://)?(www\.)?(twitter|x)\.com/.+"
    return bool(re.match(pattern, url))

def download_twitter_url(url):
    try: 
        ydl_opts = {
            outtmpl": "static/download_video.mp4","
            "format": "best",
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return "/static/download_video.mp4"
    except Exception as e:
        return None
    
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    video_url = data.get("url")

    if not is_valid_twitter_url(video_url):
        return jsonify({"error": "Invalid Twitter Video URL"}), 400
    
    download_link = download_twitter_url(video_url)

    if not download_link:
        return jsonify({"error": "Failed to download vide. Try another link."}), 500
    return jsonify({"download_link": download_link})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)