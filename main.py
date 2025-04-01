from flask import Flask, request, send_file
import yt_dlp
import time

app = Flask(__name__)


@app.route('/', methods=['GET'])
def health_check():
    return "Server is running!"  # Giúp kiểm tra nếu server đang hoạt động


@app.route('/download', methods=['GET'])
def download():
    video_id = request.args.get('video_id')  # Lấy video_id
    if not video_id:
        return "video_id is required!", 400  # Kiểm tra video_id có tồn tại không

    url = f'https://www.youtube.com/watch?v={video_id}'  # Tạo video URL từ video_id
    output_file = f"{int(time.time())}.mp4"  # Đổi tên file mỗi lần tải

    # Thiết lập yt-dlp để tải video
    ydl_opts = {
        'outtmpl': output_file,
        'format': 'mp4/bestaudio/best',
        'nocache': True,
        'force_overwrites': True,
        'noplaylist': True
    }

    # Tải video
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Trả file video về cho người dùng
    return send_file(output_file, as_attachment=True)


if __name__ == '__main__':
    # Chạy server trên port 3000 để Replit có thể truy cập được
    app.run(host='0.0.0.0', port=3000)
