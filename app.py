from flask import Flask, render_template, Response, redirect, url_for
from flask_socketio import SocketIO, emit
import cv2
import numpy as np
from cvzone.FaceDetectionModule import FaceDetector
from flask_cors import CORS


app = Flask(__name__)
socketio = SocketIO(app)
CORS(app)

realWidth = 640
realHeight = 480
videoWidth = 160
videoHeight = 120
videoChannels = 3
videoFrameRate = 15

webcam = cv2.VideoCapture(0)
detector = FaceDetector()

webcam.set(3, realWidth)
webcam.set(4, realHeight)

camera_on = True  # Track the camera state
bpm_value = 0

@app.route('/')
def index():
    return render_template('index.html', bpm=bpm_value)

def generate_frames():
    global bpm_value
    while True:
        if camera_on:
            ret, frame = webcam.read()
            if not ret:
                break

            frame, bboxs = detector.findFaces(frame, draw=False)
            print(bboxs)

            # Update bpm_value based on the confidence score of detected faces
            bpm_value = calculate_bpm(bboxs)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            socketio.emit('bpm_update', {'bpm': bpm_value})
            print(f'BPM: {bpm_value}')

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            # If the camera is off, yield an empty frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + b'\r\n\r\n')




def calculate_bpm(bboxs):
    if bboxs:
        # Calculate BPM based on the average confidence score of detected faces
        avg_confidence = np.mean([face['score'][0] for face in bboxs])
        bpm = int(avg_confidence * 100)  # Adjust the multiplier based on your calibration
        return bpm
    else:
        return 0  # No faces detected


@socketio.on('toggle_camera')
def handle_toggle_camera():
    global camera_on
    camera_on = not camera_on

    # Emit the camera state to the 'camera_toggled' event
    socketio.emit('camera_toggled', {'camera_on': camera_on})

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/redirect_detect')
def redirect_detect():
    return redirect(url_for('detect_page'))

@app.route('/detect')
def detect_page():
    return render_template('detect.html')

if __name__ == "__main__":
    socketio.run(app, debug=True)
