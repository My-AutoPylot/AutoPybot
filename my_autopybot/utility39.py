import win32clipboard
from my_autopybot.CrashHandler import report_error


def pause_program(seconds="5"):

    # Description:
    """
    Description:
        Stops the program for given seconds
    Args:
        seconds (str): seconds to be paused
    Returns:
        Status (bool) - True if success, False if failure
    """

    # import section
    import time

    # Response section
    error = None
    status = False

    try:
        seconds = int(seconds)
        time.sleep(seconds)

        # If the function returns a value, it should be assigned to the data variable.
        # data = value
    except Exception as ex:
        report_error(ex)
        error = ex

    else:
        status = True
    finally:
        if error is not None:
            raise Exception(error)
        return [status]


def api_request(url: str, method='GET', body: dict = None, headers: dict = None):
    """
    Description:
        Function used to send generic api request

    Args : url (str): url of the api
        method (str): method of the api request
        data (dict): data to be sent in the request
        headers (dict): headers to be sent in the request

    Returns :
        Status (bool) - True if success, False if failure

    """
    import requests
    import json

    # Response section
    error = None
    status = False
    data = None

    try:
        if headers is None:
            headers = {"charset": "utf-8", "Content-Type": "application/json"}

        if method == 'GET':
            response = requests.get(
                url, headers=headers, params=body)
        elif method == 'POST':
            response = requests.post(
                url, data=json.dumps(body), headers=json.dumps(headers))
        elif method == 'PUT':
            response = requests.put(
                url, data=json.dumps(body), headers=json.dumps(headers))
        elif method == 'DELETE':
            response = requests.delete(
                url, data=json.dumps(body), headers=json.dumps(headers))
        else:
            raise Exception("Invalid method")
        if response.status_code in [200, 201, 202, 203, 204]:
            data = response.json()
        else:
            raise Exception(response.text)
    except Exception as ex:
        report_error(ex)
        error = ex

    else:
        status = True
    finally:
        if error is not None:
            raise Exception(error)
        return [status, data]


# api request todos free api
# print(api_request("https://todos.free.beeceptor.com/todos", body='', headers={}))
# print(api_request(url='https://todos.free.beeceptor.com/todos'))


def clipboard_set_data(data, format_id=win32clipboard.CF_UNICODETEXT):
    """
    Description:
        Set data to clipboard
    Args:
        data: data to be set to clipboard
        format_id: format of data
    Returns:
        Status (bool) - True if success, False if failure
    """

    # Import Section
    from my_autopybot.CrashHandler import report_error
    import win32clipboard

    # Response section
    error = None
    status = False

    # Logic Section
    try:
        win32clipboard.OpenClipboard()
        try:
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(format_id, data)
        finally:
            if error is not None:
                raise Exception(error)
            win32clipboard.CloseClipboard()

    except Exception as ex:
        report_error(ex)
        error = ex

    else:
        status = True

    finally:
        if error is not None:
            raise Exception(error)
        return [status]


def GetClipboardFormats():
    import win32clipboard

    win32clipboard.OpenClipboard()
    available_formats = []
    current_format = 0
    while True:
        current_format = win32clipboard.EnumClipboardFormats(current_format)
        if not current_format:
            break
        available_formats.append(current_format)
    win32clipboard.CloseClipboard()
    return available_formats


def clipboard_get_data(format_id=win32clipboard.CF_UNICODETEXT):
    """
    Description:
        Get data from clipboard
    Returns:
        Status (bool) - True if success, False if failure
    """

    # Import Section
    from my_autopybot.CrashHandler import report_error
    import win32clipboard

    # Response section
    error = None
    status = False
    data = None

    # Logic Section
    try:
        if format_id not in GetClipboardFormats():
            raise RuntimeError("That format is not available")
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData(format_id)
        win32clipboard.CloseClipboard()

    except Exception as ex:
        report_error(ex)
        error = ex

    else:
        status = True

    finally:
        if error is not None:
            raise Exception(error)
        return [status, data]


def clear_output():
    """
    Description:
        Clears Python Interpreter Terminal Window Screen
    Returns:
        Status (bool) - True if success, False if failure
    """
    # Import Section
    import os

    # Response section
    error = None
    status = False

    # Logic Section
    try:
        command = 'clear'
        if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
            command = 'cls'
        os.system(command)
    except Exception as ex:
        report_error(ex)
        error = ex
    else:
        status = True
    finally:
        if error is not None:
            raise Exception(error)
        return [status]


def install_module(module_name):
    try:
        if module_name != "my_autopybot":
            import subprocess
            import sys
            subprocess.call([sys.executable, "-m", "pip",
                            "install", module_name])
    except:
        raise Exception("Sorry, I could not install the module {}".format(
            module_name))


def uninstall_module(module_name):
    try:
        if module_name != "my_autopybot":
            import subprocess
            import sys
            subprocess.call([sys.executable, "-m", "pip",
                            "uninstall", "-y", module_name])
        else:
            raise Exception(
                "You cannot uninstall my_autopybot from here.")
    except:
        raise Exception("Sorry, I could not uninstall the module {}".format(
            module_name))


# def image_to_text(image_path):
#     """
#     Description:
#         Convert image to text
#     Args:
#         image_path: path of the image
#     Returns:
#         Status (bool) - True if success, False if failure
#     """
#     # Import Section
#     # import pytesseract
#     import cv2
#     import numpy as np

#     status = False
#     data = None

#     try:
#         import my_autopybot.BlackBox as BB
#         status = True
#         data = BB.Image_2_Text(image_path)
#     except Exception as ex:
#         report_error(ex)
#         error = ex
#     finally:
#         if error is not None:
#             raise Exception(error)
#         return [status, data]


def date_time_now():
    import datetime
    return datetime.datetime.now()


def add_datetime(input_date, time_type='days', value=0):
    import pendulum

    if not isinstance(input_date, str):
        input_date = str(input_date)

    if time_type == 'minutes':
        return pendulum.parse(input_date).add(minutes=value)
    elif time_type == 'hours':
        return pendulum.parse(input_date).add(hours=value)
    elif time_type == 'days':
        return pendulum.parse(input_date).add(days=value)
    elif time_type == 'weeks':
        return pendulum.parse(input_date).add(weeks=value)
    elif time_type == 'months':
        return pendulum.parse(input_date).add(months=value)
# time_type = ['minutes', 'hours', 'days', 'weeks', 'months']


def subtract_datetime(input_date, time_type='days', value=0):
    import pendulum

    if not isinstance(input_date, str):
        input_date = str(input_date)

    if time_type == 'minutes':
        return pendulum.parse(input_date).subtract(minutes=value)
    elif time_type == 'hours':
        return pendulum.parse(input_date).subtract(hours=value)
    elif time_type == 'days':
        return pendulum.parse(input_date).subtract(days=value)
    elif time_type == 'weeks':
        return pendulum.parse(input_date).subtract(weeks=value)
    elif time_type == 'months':
        return pendulum.parse(input_date).subtract(months=value)
# # Funtion using pendulum to subtract days to given date


# print(subtract_datetime(datetime.datetime.now(), 'days', 1))
# print(add_datetime(datetime.datetime.now(), 'months', 1))

def image_to_text(image_path):
    """
    """
    # Imports
    from PIL import Image
    import pytesseract
    from my_autopybot.CrashHandler import report_error

    # Response section
    status = False
    data = None
    error = None

    try:
        # Logic section
        image = Image.open(image_path)
        data = pytesseract.image_to_string(image)
        status = True

    except Exception as ex:
        report_error(ex)
        error = ex

    finally:
        if error is not None:
            raise Exception(error)
        return [status, data]
