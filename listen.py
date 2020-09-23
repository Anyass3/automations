
import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    print("Say something!")
    audio = r.listen(source)
    print('heard you')
    voice_data = r.recognize_google(audio)
    print(voice_data, 'yt')