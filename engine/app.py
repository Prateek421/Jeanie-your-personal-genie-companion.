from flask import Flask, render_template, request
import subprocess
from face import implementation
#from speechr import implementation_voice2

app = Flask(__name__)
@app.route('/start_facial_recognition', methods=['POST'])
def start_facial_recognition():
    print("Entered faceial recognition")
    implementation.face_recog()
    #subprocess.Popen(['python', 'D:\\Work\\engine\\face\\implementation.py'])
    return 'Facial recognition process started'

'''@app.route('/start_voice_recognition', methods=['POST'])
def start_voice_recognition():
    print("Entered voice recognition")
    implementation_voice2.start()
    #subprocess.Popen(['python', 'D:\\Work\\engine\\face\\implementation.py'])
    return 'Voice recognition process started' '''
if __name__ == '__main__':
    app.run(debug=True)