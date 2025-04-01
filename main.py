from flask import Flask, request, send_file
import yt_dlp
import time
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def health_check():
    return "Server is running!"

@app.route('/download', methods=['GET'])
def download():
    video_id = request.args.get('video_id')
    if not video_id:
        return "video_id is required!", 400

    url = f'https://www.youtube.com/watch?v={video_id}'
    output_file = f"/tmp/{int(time.time())}.mp4"  # Ghi vào thư mục /tmp (Render cho phép)

    ydl_opts = {
        'outtmpl': output_file,
        'format': 'mp4/bestaudio/best',
        'nocache': True,
        'force_overwrites': True,
        'noplaylist': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        return f"Download error: {str(e)}", 500

    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))  # Bắt buộc lấy PORT từ biến môi trường Render
    app.run(host='0.0.0.0', port=port)
