import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

# Server temporary storage folder
DOWNLOAD_FOLDER = '/tmp/downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return jsonify({"status": "success", "message": "ToolSea API with FFmpeg is Live!"})

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"status": "error", "message": "Link daalo!"})

    try:
        out_template = os.path.join(DOWNLOAD_FOLDER, '%(id)s.%(ext)s')

        # Download best video + best audio and merge using FFmpeg
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': out_template,
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True,
            'overwrites': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'Instagram Media')
            thumbnail = info.get('thumbnail', '')
            video_id = info.get('id')

            filename = f"{video_id}.mp4"
            file_path = os.path.join(DOWNLOAD_FOLDER, filename)

            if os.path.exists(file_path):
                # Serve file direct from Render server
                download_url = request.host_url + f"get-file/{filename}"
                return jsonify({
                    "status": "success",
                    "data": {
                        "title": title,
                        "thumbnail": thumbnail,
                        "download_url": download_url
                    }
                })
            else:
                return jsonify({"status": "error", "message": "File processing fail ho gayi!"})

    except Exception as e:
        return jsonify({"status": "error", "message": "Error: " + str(e)})

@app.route('/get-file/<filename>')
def get_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
