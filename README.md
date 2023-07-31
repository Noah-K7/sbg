# sbg 
sbg.py is a (not so) simple python program that converts video into a usable .srt subtitle file. Subtitles are timed with crude silence detection and word timestamps provided by the Vost API, which is also responsible for the reading of the audio. The overall workflow of the program is as follows: Converts inputted video into a .wav, makes sure that .wav is in the correct format and converts if not, the .wav file will be read with the language model of your choosing, the result will then be thrown into a .srt file using the srt library. 

The code is very crude and I did no cleaning up because I don't care lol


## windows instructions for setup:

**1. Prerequisites:**

- Ensure you have python installed. This project requires Python 3.11 or later. You can download python from the [offical website.](https://www.python.org/downloads/)

- Make sure you have pip installed. It usually comes with python, but you can check by running `pip` in your terminal or command prompt. 

**2. Download the repository:**

- Download this repository. Extract it in whatever folder your heart desires.

**3. Navigate to program directory:**

- Open your terminal or command prompt and change your working directory to the location where you extracted the repository. You can use the `cd` command to navigate or you can just go in file explorer, open the folder the repository is in, and type `cmd` in the address bar.

**4. Install dependencies:**

- In the terminal, run the following command to install the required dependencies listed in the `requirements.txt` file:

```
pip install -r requirements.txt
```

Doing that will automatically download and install everything neccessary for sbg to run. 

IF THIS FAILS:

- Double check your python is the correct version (3.11 or later)

- Download VS Build Tools at [Microsoft's Offical Website.](https://visualstudio.microsoft.com/downloads/) For me this took alot of trial and eror, but what finally worked was downloading Desktop development with C++ aswell as the Windows 10 SDK and the most recent C++ build tools for x86 and x64 windows.

- the most recent .NET version may also be required, honestly do not remember sorry. 

**5. Install your desired language model**

- Language models (lms) are basically what is used to scan the audio. Lms differ in what they specialize in and language. A smaller lm will lead to a faster processing time, but less accurate result. You can download them at the [Vosk offical website.](https://alphacephei.com/vosk/models) For sbg I reccomend installing the general english lm; `vosk-model-en-us-0.22` and the smaller general english lm; `vosk-model-small-en-us-0.15`

- After you've downloaded your desired lm's, I reccomend unzipping them into a folder in the project directory, it will allow for easier access when inputting commands. Sbg will also try using the general english lm in it's directory as a default if you dont input anything. Though it does support typing in a full path name if you so desire. 

**6. Run the Program:**

- With all the stuff installed, you can now run sbg! Use the following command to check if it's working properly:

```python sbg.py```

If you get a message that looks like:

```
usage: python sbg.py <input-video-path> [options]
error: the following arguments are required: input-video-path
```

Then you did it!! The program works and you are ready to start using the program... speaking of using it..


## instructions for using sbg

The program takes one required argument and two optional ones, along with a help screen. 

Firstly, to get to the help screen, simply run:

```
python sbg.py -h
```

It'll output all the arguments, required and optional. But I'll also go over that here. 

**input-video-path**

- this is required, input the path to the video you want to convert to subtitles. It works with most video types, mp4, mkv, mov, and many others. 

**-l or --language_model**

- this is optional, input the path to the language model you want to use. A smaller language model will take much less time processing, but the results will also be less accurate. This repository comes with two language models already downloaded, a small US english model and a large US english model. If you need a more specifc model, or a model in a different language, you can download them at the [Vosk offical website.](https://alphacephei.com/vosk/models) By default the program uses the large general US english model, otherwise known as `vosk-model-en-us-0.22`.

**-o or --output_srt_path**

- this is optional, input the path to where you want the program to output the .srt file. By default it will output to the current working directory, i.e. the folder the program is in. 

**example:**

If I want to put in a video in my hdd, using the small lm, and output it to a different folder in my hdd i would do this:

```
python sbg.py "D:\videos\2023-07-28 02-49-03.mp4" -l "vosk-model-small-en-us-0.15" -o "D:\saved-subtitles"
```

The quotes are reccomended just incase there is a space or something in one of your files. Anyways thats a wrap! I hope this might be useful to you, I'm writing this at 4:00am so pardon if this is wack. 

# the future of sbg

- I am looking into a possible way to make vosk run faster, don't look forward to this, I don't know if my idea will lead to anything.

- Apparently vosk also comes with (limited) punctuation models. I'm going to look further into this as it could be a great addition, but from first look it seems like a whole nother can of worms so take this with a pinch of salt.  
