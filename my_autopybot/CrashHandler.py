def _canonicalizePath(path):
    """
    Description:
        Return the given path in a standard format.
        Support passing in a pathlib.Path-like object by converting to str.
    Args:
        path: A pathlib.Path-like object or a string.
    Returns:
        A string representing the canonicalized path.
    """
    return str(path)


def playsound(sound, block=True):
    """
    Description:
        Play a sound file.
    Args:
        sound: A string representing the path to the sound file.
        block: A boolean representing whether the sound should be played
            in a blocking manner.
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
            print(exceptionMessage)
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


def text_to_speech_offline(audio, show=True, rate=170):
    """
    Description:
        Text to Speech using Google's Generic API. Rate is the speed of speech. Default is 150. Actual default : 200
    Args:
        audio: A string representing the text to be spoken.
        show: A boolean representing whether the text should be printed.
        rate: A integer representing the speed of speech.
    Returns:
        A boolean representing whether the text was spoken successfully.        
    """
    import random
    import pyttsx3
    import sys
    from my_autopybot.helpers import _is_speaker_available
    is_speaker_available = _is_speaker_available()

    try:
        if not is_speaker_available:  # IF Running on AWS Machine OR Speaker not connected
            show = True
        else:
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


def text_to_speech(audio, show=True):
    """
    Description:
        Text to Speech using Google's Generic API.
    Args:
        audio: A string representing the text to be spoken.
        show: A boolean representing whether the text should be printed.
    Returns:
        A boolean representing whether the text was spoken successfully.        
    """

    # import section
    import random
    # from gtts import gTTS  # Google Text to Speech
    # import os
    # from gtts.tts import gTTSError

    status = False

    try:
        # r = random.randint(1, 20000000)
        # audio_file = 'auto_pylot_audio' + str(r) + '.mp3'
        # try:
        #     # text to speech(voice)
        #     tts = gTTS(text=audio, lang='en', tld='co.in')
        #     tts.save(audio_file)  # save as mp3
        #     playsound(sound=audio_file)  # play the audio file
        #     os.remove(audio_file)  # remove audio file
        #     if show:
        #         if type(audio) is list:
        #             print(' '.join(audio))
        #         else:
        #             print(str(audio))
        # except gTTSError:
        text_to_speech_offline(audio, show)
    except Exception as ex:
        print(str(ex))
    else:
        status = True
    finally:
        return status


def text_to_speech_error(audio, show=True):
    """
    Description:
        Text to Speech using Google's Generic API.
    Args:
        audio: A string representing the text to be spoken.
        show: A boolean representing whether the text should be printed.

    """

    try:

        text_to_speech_offline(audio, show)
        # raise Exception(audio)
        # sys.exit()
    except Exception as ex:
        print(str(ex))


def install_module(module_name):
    """
    Description:
        Install a module.
    Args:
        module_name: A string representing the name of the module to be installed.

    """
    try:
        import subprocess
        import sys
        subprocess.call([sys.executable, "-m", "pip",
                        "install", module_name])
    except:
        text_to_speech("Sorry, I could not install the module {}".format(
            module_name))


def uninstall_module(module_name):
    """
    Description:
        Uninstall a module.
    Args:
        module_name: A string representing the name of the module to be uninstalled.

    """
    try:
        if module_name != "my_autopybot":
            import subprocess
            import sys
            subprocess.call([sys.executable, "-m", "pip",
                            "uninstall", "-y", module_name])
        else:
            text_to_speech_error(
                "You cannot uninstall my_autopybot from here.")
    except:
        text_to_speech("Sorry, I could not uninstall the module {}".format(
            module_name))


def install_pyaudio():
    """
    Description:
        Installs pyaudio.
    Args:
        None.
    Returns:
        A boolean representing whether the pyaudio was installed successfully.        
    """
    try:
        import pyaudio
    except:
        # import section
        import sys
        import subprocess
        _version_1 = str(sys.version_info.major) + str(sys.version_info.minor)

        if _version_1 == "37":
            _version_2 = "37m"
        else:
            _version_2 = _version_1

        _module = f"https://raw.githubusercontent.com/py-bots/autopybot/main/support/whls/PyAudio-0.2.11-cp{_version_1}-cp{_version_2}-win_amd64.whl"
        subprocess.call([sys.executable, "-m", "pip", "install", _module],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        pass


def report_error(ex: Exception):
    """
    Description:
        Reports an error to the user.
    Args:
        ex: An exception object.
    Returns:
        A boolean representing whether the error was reported successfully.        
    """

    exception_name = type(ex).__name__
    exception_message = str(ex)
    exception_line = str(ex.__traceback__.tb_lineno)
    exception_function = str(ex.__traceback__.tb_frame.f_code.co_name)
    # import my_autopybot.BlackBox as BB
    # try:
    #     BB.Report_Developer(ex)
    # except:
    #     pass
    # slice the exception message to the first 100 characters
    if len(exception_message) > 100:
        exception_message = exception_message[:100]

    # text_to_speech("You got a {} in {}. It describes as {}.".format(
    #     exception_name, exception_function, exception_message))


def report_error_user(ex: Exception):

    exception_name = type(ex).__name__
    exception_message = str(ex)
    exception_line = str(ex.__traceback__.tb_lineno)

    if len(exception_message) > 100:
        exception_message = exception_message[:100]

    text_to_speech_error("You got a {}. Please check the line number {} .It describes as {}.".format(
        exception_name, exception_line, exception_message))
