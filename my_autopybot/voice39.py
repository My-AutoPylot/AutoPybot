from my_autopybot.CrashHandler import report_error

from my_autopybot.helpers import _is_speaker_available
is_speaker_connected = _is_speaker_available()


def _canonicalizePath(path):
    """
    Description:
        Support passing in a pathlib / Path-like object by converting to str.
    Args:
        path: A pathlib / Path-like object.
    Returns:
        [status]
        status (bool): True if success, False otherwise.
    """
    return str(path)


def playsound(sound, block=True):
    """
    Description:
        Play a sound file.
    Args:
        sound: A string containing the path to the sound file.
        block: A boolean indicating whether to block the program while the sound is playing.
    Returns:
        [status]
        status (bool): True if success, False otherwise.
    """

    sound = '"' + _canonicalizePath(sound) + '"'

    from ctypes import create_unicode_buffer, windll, wintypes
    from time import sleep
    windll.winmm.mciSendStringW.argtypes = [
        wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.UINT, wintypes.HANDLE]
    windll.winmm.mciGetErrorStringW.argtypes = [
        wintypes.DWORD, wintypes.LPWSTR, wintypes.UINT]

    def winCommand(*command):
        bufLen = 600
        buf = create_unicode_buffer(bufLen)
        command = ' '.join(command)
        # use widestring version of the function
        errorCode = int(windll.winmm.mciSendStringW(
            command, buf, bufLen - 1, 0))
        if errorCode:
            errorBuffer = create_unicode_buffer(bufLen)
            # use widestring version of the function
            windll.winmm.mciGetErrorStringW(errorCode, errorBuffer, bufLen - 1)
            exceptionMessage = ('\n    Error ' + str(errorCode) + ' for command:'
                                '\n        ' + command +
                                '\n    ' + errorBuffer.value)
            text_to_speech(exceptionMessage)
        return buf.value

    try:
        winCommand(u'open {}'.format(sound))
        winCommand(u'play {}{}'.format(sound, ' wait' if block else ''))
    finally:
        try:
            winCommand(u'close {}'.format(sound))
        except Exception:
            # If it fails, there's nothing more that can be done...
            pass


def speech_to_text():
    """
    Description:
        Speech to Text using speech_recognition
    Args:
        None
    Returns:
        [status]
        status (bool): True if success, False otherwise.
        data (str): The text spoken.
    """

    # import section
    try:
        import pyaudio
    except Exception as ex:
        report_error(ex)
    import speech_recognition as sr
    import sys

    """
    Speech to Text using Google's Generic API
    """

    recognizer = sr.Recognizer()
    energy_threshold = [3000]

    unknown = False
    status = False
    data = None

    try:
        while True:
            with sr.Microphone() as source:
                recognizer.dynamic_energy_threshold = True
                if recognizer.energy_threshold in energy_threshold or recognizer.energy_threshold <= \
                        sorted(energy_threshold)[-1]:
                    recognizer.energy_threshold = sorted(
                        energy_threshold)[-1]
                else:
                    energy_threshold.append(
                        recognizer.energy_threshold)

                recognizer.pause_threshold = 0.8

                recognizer.adjust_for_ambient_noise(source)

                try:
                    if not unknown:
                        text_to_speech("Speak now")
                    audio = recognizer.listen(source)
                    data = recognizer.recognize_google(audio)
                    status = True
                    # return [status, query]
                except AttributeError:
                    text_to_speech(
                        "Could not find PyAudio or no Microphone input device found. It may be being used by "
                        "another "
                        "application.")
                    # sys.exit()
                except sr.UnknownValueError:
                    unknown = True
                except sr.RequestError as e:
                    print("Try Again")

                # Windows OS - Python 3.8
    except OSError:
        raise Exception(
            "No input device found or it may be being used by another application.")
    except Exception as ex:
        report_error(ex)

    finally:
        return [status, data]


def text_to_speech(audio, show=True):
    """
    Description:
        Text to Speech using Google's Generic API
    Args:
        audio: A string containing the text to be spoken.
        show: A boolean indicating whether to show the text to be spoken.
    Returns:
        [status]
        status (bool): True if success, False otherwise.
    """

    # import section
    import random
    # from gtts import gTTS  # Google Text to Speech
    # from gtts.tts import gTTSError
    import os

    status = False

    try:
        text_to_speech_offline(audio, show)

    except Exception as ex:
        report_error(ex)
        status = False

    else:
        status = True
    finally:
        return [status]


def text_to_speech_offline(audio, show=True, rate=170):
    """
    Description:
        Text to Speech using Google's Generic API. Rate is the speed of speech. Default is 150
        Actual default : 200
    Args:
        audio: A string containing the text to be spoken.
        show: A boolean indicating whether to show the text to be spoken.
        rate: A integer indicating the speed of speech.
    Returns:
        [status]
        status (bool): True if success, False otherwise.
    """
    import random
    import pyttsx3
    import sys

    try:
        if is_speaker_connected:
            engine = pyttsx3.init('sapi5')
            voices = engine.getProperty('voices')
            voice = random.choice(voices)  # Randomly decide male/female voice
            engine.setProperty('voice', voice.id)

            engine.setProperty('rate', rate)
            engine.say(audio)
            engine.runAndWait()

        if type(audio) is list:
            if show:
                print(' '.join(audio))
        else:
            if show:
                print(str(audio))
    except Exception as ex:
        print(ex)
        sys.exit()


# text_to_speech_offline("Hello")
# text_to_speech("Hello")
# raise Exception("Hello")
# try:
#     raise Exception("This is an Exception")
# except Exception as ex:
#     report_error(ex)
