import json
from vosk import Model, KaldiRecognizer, SetLogLevel
import srt
from datetime import timedelta
import wave
import argparse
import os.path
import array
import moviepy.editor as mp

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert video to subtitle file using Vosk ASR.",
        usage="python %(prog)s <input-video-path> [options]"
    )
    parser.add_argument("input_video_path", metavar="input-video-path", help="Path to the input video file.")
    parser.add_argument("-l", "--language_model", dest="input_language_model_path",
                        default="vosk-model-en-us-0.22", metavar="",
                        help="Path to the Vosk language model. Default: vosk-model-en-us-0.22")
    parser.add_argument("-o", "--output_srt_path", dest="output_subtitle_path",
                        default=None, action="store", 
                        help="Path to save the output subtitle file. Default: directory of input file")
    args = parser.parse_args()

    inputVideoPath = args.input_video_path
    inputLanguageModelPath = args.input_language_model_path
    outputSubtitlePath = args.output_subtitle_path

#converts video to .wav tested with mp4 and mkv
#TODO: test with mov
print("Step 1: \nConverting video to wav...")
clip = mp.VideoFileClip(inputVideoPath) #this needs to be turned into a sys arg
clip.audio.write_audiofile("audioFileToConvert.wav", verbose=False, logger=None)

subtitleList = []
SetLogLevel(-1) #without this alot of console stuff will happen when the lm is loaded

def convert_to_mono_pcm(input_file, output_file):
    # Open the input WAV file
    print("Step 2: \nInvalid wav detected! Converting to valid format...")
    with wave.open(input_file, "rb") as wf:
        num_channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        frame_rate = wf.getframerate()

        # Check if the input file is already in mono format, if not, convert it to mono
        if num_channels != 1:
            print("Converting to mono...")
            data = array.array('h', wf.readframes(wf.getnframes()))
            data_mono = array.array('h', [data[i] for i in range(0, len(data), num_channels)])
            num_channels = 1
        else:
            data_mono = wf.readframes(wf.getnframes())

        # Check if the sample width is already 2 bytes, if not, convert it to 2 bytes
        if sample_width != 2:
            print("Converting to 2-byte sample width...")
            data_mono = array.array('h', data_mono)
            sample_width = 2

    # Ensure there is no compression (set the compType to "NONE")
    comp_type = "NONE"

    # Write the converted data to the output WAV file
    with wave.open(output_file, "wb") as wf_out:
        wf_out.setnchannels(num_channels)
        wf_out.setsampwidth(sample_width)
        wf_out.setframerate(frame_rate)
        wf_out.setcomptype(comp_type, "not compressed")
        wf_out.writeframes(data_mono.tobytes())

convert_to_mono_pcm("audioFileToConvert.wav", "output.wav")

audioFile = "output.wav"
print("Successfully converted!")

# Read the audio file and get the sampling rate
with wave.open(audioFile, "rb") as audio_file:
    samplingRate = audio_file.getframerate()

print("Step 3: \nLoading Language model... This may take awhile!")
# Load the language model
model_path = inputLanguageModelPath
model = Model(model_path)

# Check if the model is loaded
if not model:
    print("Error: Failed to load the Vosk model. rip lol")
else:
    print("Vosk model loaded successfully. YIPPEE!!")

# Create a recognizer object
recognizer = KaldiRecognizer(model, samplingRate)
recognizer.SetWords(True)

# Read the audio file
with open(audioFile, "rb") as audio_file:
    print("Step 4: \nReading audio file... this may take awhile!")
    audio_data = audio_file.read()

# Perform speech recognition
recognizer.AcceptWaveform(audio_data)
print("recognizing speech...")
result = json.loads(recognizer.Result())
print("Audio file successfully read!")
# Get recognized text
if "text" in result:
    recognized_text = result["text"]
    #print("Recognized Text: ", recognized_text)

    if "result" in result:
        print("Step 5: \nConverting result to srt file...")
        words = result["result"]
        silenceDetectedWords = []
        i = 0
        pastEndTime = words[0]["end"]
        iteration = 0
        finalWordText = ""  
        startTime = words[0]["start"]
        endTime = 0
        startStartTime = 0 #this is for those extremely rare edgecases where there is only ONE subtitle. doubt thisll ever be used tbh.
        for word in words:
            i += 1
            silenceStartTime = word["start"]
            endTime = word["end"]
            silenceDetectedWords.append(word)

            #silence detection
            silenceDuration = silenceStartTime - pastEndTime
            #print(f"{pastEndTime} - {silenceStartTime} = {silenceDuration}")
            pastEndTime = endTime
            
            if(silenceDuration > 0.1):
                silenceDetectedWords.insert(i - 1, "/silence")
                i += 1

        i = 0
        #print(silenceDetectedWords)
        for word in silenceDetectedWords:
            if(word == "/silence"):
                #print("silence detected")
                subtitleList.append(srt.Subtitle(index=i, start=timedelta(seconds=startTime), end=timedelta(seconds=endTime), content=finalWordText))
                finalWordText = ""
                iteration = 0
                continue
            
            if(iteration == 12):
                #print("iteration detected")
                subtitleList.append(srt.Subtitle(index=i, start=timedelta(seconds=startTime), end=timedelta(seconds=endTime), content=finalWordText))
                finalWordText = ""
                iteration = 0
            
            if(iteration == 0):
                startTime = word["start"]

            i += 1
            iteration += 1
            wordText = word["word"]
            finalWordText += wordText + " "
            endTime = word["end"]

        #if theres any text left thisll add it 
        if i == 0:
            startTime = startStartTime
        i += 1
        endTime = word["end"]
        subtitleList.append(srt.Subtitle(index=i, start=timedelta(seconds=startTime), end=timedelta(seconds=endTime), content=finalWordText))


newSubtitle = srt.compose(subtitleList)

videoPathComp = inputVideoPath.split('\\')
videoWithExtension = videoPathComp[-1].rsplit('.', 1)
videoName = videoWithExtension[0]

if not args.output_subtitle_path:
    parentDir = os.path.dirname(inputVideoPath)

    finalPath = os.path.join(parentDir, f"{videoName}-subtitle.srt")

else:
    finalPath = os.path.join(outputSubtitlePath, f"{videoName}-subtitle.srt")





with open (finalPath, 'w') as file:
    file.write(newSubtitle)

print("COMPLETE:\nProcess Completed!")
