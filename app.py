from flask import Flask, request
import os

app = Flask(__name__)

# Directory where uploaded files will be saved
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_video():
    # Check if a video file was included in the request
    if 'video' not in request.files:
        return 'No video file provided', 400
    
    video_file = request.files['video']

    # Check if the file name is not empty
    if video_file.filename == '':
        return 'No selected file', 400

    if video_file:
        # Save the video file to the 'uploads' directory
        file_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
        video_file.save(file_path)

        # Write "True" to a text file
        with open('upload_status.txt', 'a') as f:
            f.write(file_path)

        return 'Upload successful', 200

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)