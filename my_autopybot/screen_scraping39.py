import win32clipboard
import os
from my_autopybot.CrashHandler import report_error

output_folder_path = os.path.join(
    os.path.abspath(r'C:\Users\Public\PyBots'), 'My-autopybot', 'Scraped Data Folder')


def scrape_save_contents_to_notepad(folderPathToSaveTheNotepad: str = "", switch_to_window: str = "", X: int = 0, Y: int = 0):

    # Description:
    """
    Description:
        Copy pastes all the available text on the screen to notepad and saves it.
    Args:
        folderPathToSaveTheNotepad: Folder path to save the notepad file
        switch_to_window: Window name to switch to
        X: X coordinate of the screen to click and get focus
        Y: Y coordinate of the screen to click and get focus
    Returns:
        [status, data]
        status: True if successful, False if not
        data: Text copied from the screen by scraping
    """

    # import section
    from my_autopybot.Engine import window_activate_and_maximize_windows
    import time
    import pywinauto as pwa
    import pathlib as Path
    # import clipboard

    # Response section
    error = None
    status = False
    data = None

    try:

        if not folderPathToSaveTheNotepad:
            folderPathToSaveTheNotepad = output_folder_path

        if switch_to_window:
            window_activate_and_maximize_windows(switch_to_window)

        time.sleep(1)

        if X == 0 and Y == 0:
            from win32api import GetSystemMetrics
            X = int(GetSystemMetrics(0))/2
            Y = int(GetSystemMetrics(1))/2
        # pg.click(X, Y)
        pwa.mouse.click(coords=(X, Y), button='left')
        time.sleep(0.5)

        # pg.hotkey("ctrl", "a")
        pwa.keyboard.send_keys("{VK_LCONTROL down} a {VK_LCONTROL up}")
        time.sleep(1)

        # pg.hotkey("ctrl", "c")
        pwa.keyboard.send_keys("{VK_LCONTROL down} c {VK_LCONTROL up}")
        time.sleep(1)

        clipboard_data = get_data_from_clipboard()
        time.sleep(2)

        screen_clear_search()

        notepad_file_path = Path(folderPathToSaveTheNotepad)
        notepad_file_path = notepad_file_path / 'notepad-contents.txt'

        f = open(notepad_file_path, "w", encoding="utf-8")
        f.write(clipboard_data)
        time.sleep(2)
        f.close()

        clipboard_data = ''
        data = str(notepad_file_path)

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
        return [status, data]


def screen_clear_search(delay=0.2):
    # Description:
    """
    Description:
        Clears previously found text (crtl+f highlight)
    Args:
        delay: Delay in seconds. Default is 0.2
    Returns:
        [status]
        status: True if successful, False if not
    """

    # import section
    # from clointfusion.clointfusion import text_to_speech
    import pywinauto as pwa
    import time
    # Response section
    error = None
    status = False

    try:
        # pg.hotkey("ctrl", "f")
        pwa.keyboard.send_keys("{VK_LCONTROL down} f {VK_LCONTROL up}")

        time.sleep(delay)
        # pg.typewrite("^%#")
        pwa.keyboard.send_keys("^%#")
        time.sleep(delay)
        # pg.hotkey("esc")
        pwa.keyboard.send_keys("{ESC}")
        time.sleep(delay)
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
    """
    Description:
        Get all formats of clipboard
    Args:
        None
    Returns:
        Status: True if successful, False if not
        Data : Clipboard formats
    """

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


def get_data_from_clipboard(format_id=win32clipboard.CF_UNICODETEXT):
    if format_id not in GetClipboardFormats():
        raise RuntimeError("That format is not available")
    win32clipboard.OpenClipboard()
    try:
        data = win32clipboard.GetClipboardData(format_id)
        data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
    finally:
        win32clipboard.CloseClipboard()
    return data


def screen_scrape_extract_table(switch_to_window: str, after_this_word: str, before_this_word: str, include_after_this_word=False, include_before_this_word=False):
    """
    Description:
        Extracts the table from the screen and returns the data in a list.
    Args:
        switch_to_window (str, optional): [description]. Defaults to "".
        after_this_word (str, optional): [description]. Defaults to "".
        before_this_word (str, optional): [description]. Defaults to "".
        include_after_this_word (bool, optional): [description]. Defaults to False.
        include_before_this_word (bool, optional): [description]. Defaults to False.

    Returns:
        [status, data]
        status (bool): True if the function executed successfully.
        data (list): List of the data in the table.
    """
    # Import Section
    import pandas as pd
    from win32api import GetSystemMetrics
    import numpy as np
    from my_autopybot.Engine import window_activate_and_maximize_windows, key_press, pause_program, clipboard_get_data, mouse_click
    from my_autopybot.CrashHandler import report_error

    # Response Section
    error = None
    status = False
    data = None

    # Logic Section
    try:
        if not switch_to_window:
            raise Exception("Window name is not provided.")

        if not after_this_word or not before_this_word:
            raise Exception("After and Before words cannot be empty")

        if switch_to_window:
            window_activate_and_maximize_windows(switch_to_window)

        mouse_click(int(GetSystemMetrics(0)/2), int(GetSystemMetrics(1)/2))
        pause_program(1)

        key_press(key_1='{VK_CONTROL}', key_2='a')
        pause_program(1)

        key_press(key_1='{VK_CONTROL}', key_2='c')
        pause_program(1)

        clipboard_data = clipboard_get_data()
        pause_program(1)

        mouse_click(int(GetSystemMetrics(0)/2), int(GetSystemMetrics(1)/2))

        entire_data_as_list = []

        input_data_as_list = str(clipboard_data).splitlines()

        # print(input_data_as_list,"input_data_as_list")

        for line in input_data_as_list:
            if line.strip() != '':
                entire_data_as_list.append(str(line.strip()))

        if include_after_this_word == True and include_before_this_word == True:
            string_1 = after_this_word + \
                str(entire_data_as_list).split(after_this_word)[1]  # + "\\t"
            required_data = str(string_1).split(before_this_word)[
                0] + "\\t" + before_this_word

        elif include_after_this_word == True and include_before_this_word == False:
            string_1 = after_this_word + \
                str(entire_data_as_list).split(after_this_word)[1]  # + "\\t"
            required_data = str(string_1).split(before_this_word)[0]

        elif include_after_this_word == False and include_before_this_word == True:
            string_1 = str(entire_data_as_list).split(after_this_word)[1]
            required_data = before_this_word + \
                str(string_1).split(before_this_word)[0]  # + "\\t"

        elif include_after_this_word == False and include_before_this_word == False:
            string_1 = str(entire_data_as_list).split(after_this_word)[1]
            required_data = str(string_1).split(before_this_word)[0]

        data = ''

        try:
            data = pd.DataFrame([x.split('\\\\t') for x in required_data.split('\\\\r\\\\n')[
                                1:]], columns=[x for x in required_data.split('\\\\r\\\\n')[0].split('\\\\t')])
        except:
            data = pd.DataFrame([x.split('\\\\t')
                                for x in required_data.split('\\\\r\\\\n')[1:]])

        data = data.replace(to_replace='None', value=np.nan).dropna()

    except Exception as ex:
        report_error(ex)
        error = ex

    else:
        status = True

    finally:
        if error is not None:
            raise Exception(error)
        return [status, data]
# [status, data]
# print(screen_scrape_extract_table(switch_to_window="PROCURE BOX",after_this_word="VEHICLE NUMBER",before_this_word="Showing"))
# print(screen_scrape_extract_table("PROCURE BOX","VEHICLE NUMBER","Showing",include_after_this_word=True))

# https://en.wikipedia.org/wiki/Scoring_in_association_football
# print(screen_scrape_extract_table(switch_to_window="Scoring in association",after_this_word="Scoring rate in major competitions",before_this_word="An analysis of several years"))
# print(screen_scrape_extract_table("Scoring in association","Ball must go between posts below specified height","Ball must go between posts at any height"))
