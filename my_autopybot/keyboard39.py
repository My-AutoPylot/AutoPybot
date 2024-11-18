from my_autopybot.CrashHandler import report_error


def key_press(key_1='', key_2='', key_3='', write_to_window=""):

    # Description:
    """
    Description:
        Presses the given key / Emulates the given keystrokes on desired window.

    Args:
        key_1 (str, optional): Enter the 1st key
        Eg: ctrl or shift. Defaults to ''.
        key_2 (str, optional): Enter the 2nd key in combination.
        Eg: alt or A. Defaults to ''.
        key_3 (str, optional): Enter the 3rd key in combination.
        Eg: del or tab. Defaults to ''.
        write_to_window (str, optional): (Only in Windows) Name of Window you want to activate. Defaults to "".

    Returns:
        [status]
        status (bool): Whether the function is successful or failed.
    """

    # import section
    import pywinauto as pwa
    from my_autopybot.Engine import window_activate_window

    # Response section
    error = None
    status = False

    # Logic section
    try:
        if key_1 == '':
            raise Exception("Key 1 is empty.")

        special_keys = ['{SCROLLLOCK}', '{VK_SPACE}', '{VK_LSHIFT}', '{VK_PAUSE}', '{VK_MODECHANGE}',
                        '{BACK}', '{VK_HOME}', '{F23}', '{F22}', '{F21}', '{F20}', '{VK_HANGEUL}', '{VK_KANJI}',
                        '{VK_RIGHT}', '{BS}', '{HOME}', '{VK_F4}', '{VK_ACCEPT}', '{VK_F18}', '{VK_SNAPSHOT}',
                        '{VK_PA1}', '{VK_NONAME}', '{VK_LCONTROL}', '{ZOOM}', '{VK_ATTN}', '{VK_F10}', '{VK_F22}',
                        '{VK_F23}', '{VK_F20}', '{VK_F21}', '{VK_SCROLL}', '{TAB}', '{VK_F11}', '{VK_END}',
                        '{LEFT}', '{VK_UP}', '{NUMLOCK}', '{VK_APPS}', '{PGUP}', '{VK_F8}', '{VK_CONTROL}',
                        '{VK_LEFT}', '{PRTSC}', '{VK_NUMPAD4}', '{CAPSLOCK}', '{VK_CONVERT}', '{VK_PROCESSKEY}',
                        '{ENTER}', '{VK_SEPARATOR}', '{VK_RWIN}', '{VK_LMENU}', '{VK_NEXT}', '{F1}', '{F2}',
                        '{F3}', '{F4}', '{F5}', '{F6}', '{F7}', '{F8}', '{F9}', '{VK_ADD}', '{VK_RCONTROL}',
                        '{VK_RETURN}', '{BREAK}', '{VK_NUMPAD9}', '{VK_NUMPAD8}', '{RWIN}', '{VK_KANA}',
                        '{PGDN}', '{VK_NUMPAD3}', '{DEL}', '{VK_NUMPAD1}', '{VK_NUMPAD0}', '{VK_NUMPAD7}',
                        '{VK_NUMPAD6}', '{VK_NUMPAD5}', '{DELETE}', '{VK_PRIOR}', '{VK_SUBTRACT}', '{HELP}',
                        '{VK_PRINT}', '{VK_BACK}', '{CAP}', '{VK_RBUTTON}', '{VK_RSHIFT}', '{VK_LWIN}', '{DOWN}',
                        '{VK_HELP}', '{VK_NONCONVERT}', '{BACKSPACE}', '{VK_SELECT}', '{VK_TAB}', '{VK_HANJA}',
                        '{VK_NUMPAD2}', '{INSERT}', '{VK_F9}', '{VK_DECIMAL}', '{VK_FINAL}', '{VK_EXSEL}',
                        '{RMENU}', '{VK_F3}', '{VK_F2}', '{VK_F1}', '{VK_F7}', '{VK_F6}', '{VK_F5}', '{VK_CRSEL}',
                        '{VK_SHIFT}', '{VK_EREOF}', '{VK_CANCEL}', '{VK_DELETE}', '{VK_HANGUL}', '{VK_MBUTTON}',
                        '{VK_NUMLOCK}', '{VK_CLEAR}', '{END}', '{VK_MENU}', '{SPACE}', '{BKSP}', '{VK_INSERT}',
                        '{F18}', '{F19}', '{ESC}', '{VK_MULTIPLY}', '{F12}', '{F13}', '{F10}', '{F11}', '{F16}',
                        '{F17}', '{F14}', '{F15}', '{F24}', '{RIGHT}', '{VK_F24}', '{VK_CAPITAL}', '{VK_LBUTTON}',
                        '{VK_OEM_CLEAR}', '{VK_ESCAPE}', '{UP}', '{VK_DIVIDE}', '{INS}', '{VK_JUNJA}',
                        '{VK_F19}', '{VK_EXECUTE}', '{VK_PLAY}', '{VK_RMENU}', '{VK_F13}', '{VK_F12}', '{LWIN}',
                        '{VK_DOWN}', '{VK_F17}', '{VK_F16}', '{VK_F15}', '{VK_F14}']

        def make_down(key):
            return key.replace('}', ' down}')

        def make_up(key):
            return key.replace('}', ' up}')

        case_0 = True if not key_2 and not key_3 else False
        case_1 = True if key_1 in special_keys and key_2 not in special_keys and key_3 not in special_keys else False  # Only 1 Special Key
        case_2 = True if key_1 in special_keys and key_2 in special_keys and key_3 not in special_keys else False  # 2 Special Keys

        if write_to_window:
            window_activate_window(write_to_window)

        if case_0:
            pwa.keyboard.send_keys(str(key_1))
        elif case_1:
            key_1_down = make_down(key_1)
            key_1_up = make_up(key_1)
            pwa.keyboard.send_keys(str(key_1_down + key_2 + key_3 + key_1_up))
        elif case_2:
            key_1_down = make_down(key_1)
            key_1_up = make_up(key_1)
            key_2_down = make_down(key_2)
            key_2_up = make_up(key_2)
            pwa.keyboard.send_keys(
                str(key_1_down + key_2_down + key_3 + key_2_up + key_1_up))
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


def key_write_enter(text_to_write="", write_to_window="", key="e"):

    # Description:
    """
    Description:
        This function is used to write given text to a window and then press the enter/tab key.

    Args:
        text_to_write (str, optional): Text you wanted to type
        Eg: ClointFusion is awesone. Defaults to "".
        write_to_window (str, optional): (Only in Windows) Name of Window you want to activate
        Eg: Notepad. Defaults to "".
        key (str, optional): Press Enter key after typing.
        Eg: t for tab. Defaults to e

    Returns:
        [status]
        status (bool): True if successful, False if not.
    """

    # import section
    import time
    import pywinauto as pwa
    from my_autopybot.Engine import window_activate_window
    # Response section
    error = None
    status = False

    # Logic section
    try:
        if not text_to_write:
            raise Exception("Text to write is empty.")

        if write_to_window:
            window_activate_window(write_to_window)

        time.sleep(0.2)
        pwa.keyboard.send_keys(
            text_to_write, with_spaces=True, with_tabs=True, with_newlines=True)
        if key.lower() == "e":
            pwa.keyboard.send_keys('{ENTER}')
        if key.lower() == "t":
            pwa.keyboard.send_keys('{TAB}')

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


def key_hit_enter(write_to_window=""):

    # Description:
    """
    Description:
        This function is used to press the enter key on a desired window.

    Args:
        write_to_window (str, optional): (Only in Windows)Name of Window you want to activate.
        Eg: Notepad. Defaults to "".

    Returns:
        [status]
        status (bool): True if successful, False if not.
    """

    # import section
    import pywinauto as pwa
    from my_autopybot.Engine import window_activate_window

    # Response section
    error = None
    status = False

    # Logic section

    try:
        if write_to_window:
            window_activate_window(write_to_window)
        pwa.keyboard.send_keys('{ENTER}')
        status = True

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
