import numpy as np
import sounddevice as sd
import librosa
from preprocess_data import extract_features
from tensorflow.keras.models import Sequential, model_from_json
import pickle

with open('scaler2.pickle', 'rb') as f:
    scaler2 = pickle.load(f)
    
with open('encoder2.pickle', 'rb') as f:
    encoder2 = pickle.load(f)

json_file = open('voice_recog_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

loaded_model.load_weights("voice_recog_model.h5")
print("Loaded model from disk")

emotions1={1:'Neutral', 2:'Calm', 3:'Happy', 4:'Sad', 5:'Angry', 6:'Fear', 7:'Disgust',8:'Surprise'}

# Define a function to capture live audio
def capture_audio(duration=2.5, sr=22050):
    print("Recording...")
    audio = sd.rec(int(duration * sr), samplerate=sr, channels=1, dtype="float32")
    sd.wait()  # Wait for audio recording to complete
    return audio.squeeze(), sr


def predict_emotion(audio_data, sr):
    features = extract_features(audio_data, sr)

    result=np.array(features)

    #desired_shape = (1, 2376)
    #num_zeros = np.prod(desired_shape) - result.size
    
    # Pad the array with zeros to fill the remaining values
    #result = np.pad(result, (0, num_zeros), mode='constant', constant_values=0)

    i_result = scaler2.transform(result.reshape(1,-1))

    #result = np.reshape(1,-1)(i_result)
    
    #result=np.reshape(result,newshape=(1,2376))
    final_result=np.expand_dims(i_result, axis=2)
    print(final_result)
    # Reshape the features to match model input shape (if needed)
    #features = features.reshape(1, features.shape[0], 1)
    # Perform prediction using your model
    prediction = loaded_model.predict(final_result)

    #predicted_emotion = np.argmax(prediction)

    y_pred = encoder2.inverse_transform(prediction)

    return y_pred[0][0]

# Main function to capture live audio, preprocess, and predict emotion
def main():
    while True:
        # Capture live audio
        audio_data, sr = capture_audio()
        # Predict emotion
        emotion_label = predict_emotion(audio_data, sr)
        print("Predicted Emotion:", emotion_label)

# Call the main function to start capturing live audio and predicting emotion
if __name__ == "__main__":
    main()
