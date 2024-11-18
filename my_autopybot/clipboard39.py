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
        report_error(ex)
        error = ex

    else:
        status = True

    finally:
        if error is not None:
            raise Exception(error)
        return [status, data]
