import win32clipboard


def clipboard_set_data(data, format_id=win32clipboard.CF_UNICODETEXT):
    """
    Description:
        Set data to clipboard
    Args:
        data: data to be set to clipboard
        format_id: format of data
    Returns:
        [status]
        status (bool) - True if successful, False if not
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
            win32clipboard.CloseClipboard()

    except Exception as ex:
        error = ex
        report_error(ex)

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
    Args:
        format_id: format of data
    Returns:
        [status, data]
        status (bool) - True if successful, False if not
        data (str) - data from clipboard
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
        error = ex
        report_error(ex)

    else:
        status = True

    finally:
        if error is not None:
            raise Exception(error)
        return [status, data]


def citrix_scrape_contents_by_search_copy_paste(highlight_text=""):
    """
    Description:
        Gets the focus on the Citrix screen/window by searching desired text using crtl+f and performs copy/paste of all data. Useful in Citrix applications
        This is useful in Citrix systems
    Args:
        highlight_text: text to be searched and highlighted
    Returns:
        [status, data]
        status (bool) - True if successful, False if not
        data (str) - Scraped data

    """
    # Import Section
    from my_autopybot.CrashHandler import report_error
    from my_autopybot import key_press, key_write_enter
    import time

    # Response section
    error = None
    status = False
    data = None

    # Logic section

    output_lst_newline_removed = []
    try:
        if not highlight_text:
            highlight_text = "&###%#&&"  # seach for some string to get focus on the screen

        time.sleep(1)

        key_press("ctrl", "f")
        time.sleep(1)

        key_write_enter(highlight_text)
        time.sleep(1)

        key_press("esc")
        time.sleep(2)

        key_press("ctrl", "a")
        time.sleep(2)

        key_press("ctrl", "c")
        time.sleep(2)

        clipboard_data = clipboard_get_data()
        time.sleep(2)

        citrix_window_clear_search()

        entire_data_as_list = clipboard_data.splitlines()
        for line in entire_data_as_list:
            if line.strip():
                output_lst_newline_removed.append(line.strip())

        clipboard_data = ''

        data = output_lst_newline_removed
    except Exception as ex:
        error = ex
        report_error(ex)

    else:
        status = True

    finally:
        if error is not None:
            raise Exception(error)
        return [status, data]
# [status, data]


def citrix_window_clear_search():
    """
    Description:
        Clears previously found text (crtl+f highlight)
    Args:
        None
    Returns:
        [status]
        status (bool) - True if successful, False if not
    """
    # Import Section
    from my_autopybot.CrashHandler import report_error
    from my_autopybot import key_press, key_write_enter
    import time

    # Response section
    error = None
    status = False

    # Logic Section
    try:
        key_press("ctrl", "f")
        time.sleep(2)

        key_write_enter("^%#")
        time.sleep(2)

        key_press("esc")
        time.sleep(2)

    except Exception as ex:
        error = ex
        report_error(ex)

    else:
        status = True

    finally:
        if error is not None:
            raise Exception(error)
        return [status]
# [status]
