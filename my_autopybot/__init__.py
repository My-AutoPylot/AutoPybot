# exclude these modules from pdoc auto documentation
from my_autopybot.Engine import *
import sourcedefender
import getopt
import sys
__pdoc__ = {}

__pdoc__['CrashHandler'] = False
__pdoc__['Engine'] = False
__pdoc__['resources'] = False
__pdoc__['chrome39.DisableLogger'] = False
__pdoc__['datascience39'] = False
__pdoc__['database39'] = False
__pdoc__['helpers'] = False
__pdoc__['citrix39.GetClipboardFormats'] = False
__pdoc__['clipboard39.GetClipboardFormats'] = False
__pdoc__['excel39.valid_data'] = False
__pdoc__['images39'] = False
__pdoc__['scheduler39'] = False
__pdoc__['screen_scraping39.GetClipboardFormats'] = False
__pdoc__['screen_scraping39.get_data_from_clipboard'] = False
# __pdoc__['voice39._canonicalizePath'] = False
__pdoc__['voice39.text_to_speech_offline'] = False

__version__ = '1.6'
__release_id__ = 7
__author__ = 'PyBots LLC'
__email__ = 'support@pybots.ai'

argument_list = sys.argv[1:]
compatible_system = False
debug_process = False
user_email = None
bot_id = None
bot_name = None

short_options = "d:e:i:n:v"
long_options = ["debug=", "email=", "id=", "name=", "version"]

arguments, values = getopt.getopt(
    argument_list, short_options, long_options)
for current_argument, current_value in arguments:
    if current_argument in ("-v", "--version"):
        print(f"{__version__},{__release_id__}")
        sys.exit(0)
    if current_argument in ("-d", "--debug"):
        debug_process = True if current_value == 'True' else False
    if current_argument in ("-e", "--email"):
        user_email = current_value
    if current_argument in ("-i", "--id"):
        bot_id = current_value
    if current_argument in ("-n", "--name"):
        bot_name = current_value


def check_email(user_email):
    import subprocess
    import requests
    import sys
    import json
    user_uuid = str(subprocess.check_output('wmic csproduct get uuid'),
                    'utf-8').split('\n')[1].strip()
    try:
        user_mac_add = subprocess.check_output(
            'wmic nic where PhysicalAdapter=True get MACAddress,Name | findstr "Realtek"', shell=True).decode('utf-8').split('\n')[
            0].strip().split(' ')[0]
    except:
        user_mac_add = 'M3:69:43:M5:96:3V'

    status = requests.post('https://api.pybots.ai/auth/verify-device-python/',
                           data={'user_email': user_email, 'device_uuid': user_uuid, 'device_mac': user_mac_add})

    if not status.status_code == 200:
        from my_autopybot.message39 import msg_count_down
        error_msg = json.loads(status.text)['error']
        msg_count_down(
            f'Initialization failed : {error_msg}')
        sys.exit(0)


if user_email is None and debug_process is False:
    print('Initialization failed. Run file with argument --email email@xyz.com to use My-autopybot python library.')
    sys.exit(0)
else:
    if debug_process is False:
        check_email(user_email)
