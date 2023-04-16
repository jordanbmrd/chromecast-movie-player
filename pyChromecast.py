import os
import sys
import time
from pathlib import Path
from flask import Flask, Response, request, render_template, send_file
import pychromecast
from pychromecast.controllers.media import MediaController
from multiprocessing import Process
import mimetypes
import subprocess

app = Flask(__name__)

def get_local_ip():
    import socket
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def cast_movie(movie_path, chromecast_name):
    chromecast = None
    chromecasts, _ = pychromecast.get_listed_chromecasts(friendly_names=[chromecast_name])
    
    if not chromecasts:
        print(f"Chromecast '{chromecast_name}' not found.")
        sys.exit(1)

    chromecast = chromecasts[0]
    chromecast.wait()
    media_controller = MediaController()
    chromecast.register_handler(media_controller)

    ip = get_local_ip()
    filename = os.path.basename(movie_path)
    movie_url = f"http://{ip}:8000/{filename}"
    
    media_type, _ = mimetypes.guess_type(movie_path)
    if not media_type.startswith('video/'):
        print(f"Unsupported media type '{media_type}' for file '{filename}'.")
        sys.exit(1)

    media_controller.play_media(movie_url, media_type)
    media_controller.block_until_active()
    print(f"Casting '{filename}' to '{chromecast_name}'")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping cast...")
        media_controller.stop()

@app.route('/<path:filename>')
def serve_movie(filename):
    movie_file = Path(movie_directory) / filename
    transcode_options = [
        "-c:v", "libx264",
        "-b:v", "2M",
        "-maxrate", "2M",
        "-bufsize", "4M",
        "-pix_fmt", "yuv420p",
        "-preset", "medium",
        "-movflags", "frag_keyframe+empty_moov",
        "-c:a", "aac",
        "-b:a", "192k",
        "-f", "mp4",
        "pipe:1"
    ]
    command = ["ffmpeg", "-i", str(movie_file)] + transcode_options
    proc = subprocess.Popen(command, stdout=subprocess.PIPE)
    return Response(proc.stdout, content_type="video/mp4")

from flask import request
from werkzeug.utils import secure_filename

import traceback

@app.route('/cast_movie', methods=['POST'])
def handle_cast_movie():
    try:
        movie_file = request.files.get('movie')
        if not movie_file:
            return 'No movie file provided', 400

        filename = secure_filename(movie_file.filename)
        movie_path = os.path.join(movie_directory, filename)
        movie_file.save(movie_path)

        cast_process = Process(target=cast_movie, args=(movie_path, request.args.get('chromecast_name')))
        cast_process.start()

        return 'Movie is being cast', 200
    except Exception as e:
        print(traceback.format_exc())
        return f"Error: {str(e)}", 500

@app.route('/')
def home():
    return render_template('./index.html')


if __name__ == '__main__':
    movie_directory = './uploaded_movies'
    os.makedirs(movie_directory, exist_ok=True)

    app.run(host="0.0.0.0", port=8000, debug=False)
