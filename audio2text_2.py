import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks

myaudio = AudioSegment.from_file("chunk1.wav", "wav")  # archivo larga duracion
chunk_length_ms = 180000 # pydub calculates in millisec
chunks = make_chunks(myaudio, chunk_length_ms) # Make chunks of one sec

# Export all of the individual chunks as wav files

for i, chunk in enumerate(chunks):
    chunk_name = "chunk{0}.wav".format(i)
    print ("exporting", chunk_name)
    chunk.export(chunk_name, format="wav")

i=0
whole_text = ""
for chunk in chunks:
    print ("in chunks")
    chunk_silent = AudioSegment.silent(duration = 10)  # 10 y 500 mejores hasta ahora
    audio_chunk = chunk_silent + chunk + chunk_silent
    audio_chunk.export("./chunk{0}.wav".format(i), bitrate ='192k', format ="wav")
    filename = 'chunk'+str(i)+'.wav'
    print("Processing chunk "+str(i))
    file = filename
    r = sr.Recognizer()
    with sr.AudioFile(file) as source:

        r.adjust_for_ambient_noise(source)  # probando con duration=1 NO 0.5 regular
        audio_listened = r.record(source)
    try:
        text = r.recognize_google(audio_listened)
    except sr.UnknownValueError as e:
        print("Error:", str(e))
    else:
        text = f"{text.capitalize()}. "
        print(file, ":", text)
        whole_text += text

    i += 1