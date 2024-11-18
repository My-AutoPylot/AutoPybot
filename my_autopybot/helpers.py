def get_media_type(file_path):
    import mimetypes
    mimetypes.init()
    mimestart = mimetypes.guess_type(file_path)[0]
    if mimestart != None:
        mimestart = mimestart.split('/')[0]
        if mimestart in ['audio', 'video', 'image']:
            return mimestart
    return None


# check if Python is being run from AWS instance
def _is_ec2_instance():
    from urllib.request import urlopen
    from urllib.error import URLError

    """Check if an instance is running on AWS."""
    result = False
    meta = 'http://169.254.169.254/latest/meta-data/public-ipv4'
    try:
        result = urlopen(meta).status == 200
    except ConnectionError:
        return result
    except URLError:
        return result
    return result

# print(_is_ec2_instance())

# Below function needs addtional Python library, so discouraged to use it.
# #check if speaker is connected
# def _is_speaker_available():
#     from pycaw.pycaw import AudioUtilities
#     try:
#         AudioUtilities.GetSpeakers()
#         return True
#     except:
#         return False

# # print(_is_speaker_available())


# check if speaker is connected using pyaudio
def _is_speaker_available():
    try:
        import pyaudio
    except:
        from my_autopybot.CrashHandler import install_pyaudio
        install_pyaudio()
        import pyaudio

    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info['maxInputChannels'] > 0:
            return True
    return False

# print(_is_speaker_available())
