from my_autopybot.CrashHandler import report_error


def _window_find_exact_name(windowName=""):
    """
    Description:
        Gives you the exact window name you are looking for.

    Args:
        windowName  (str) : Name of the window to find.

    Returns:
        [status, data]
        status (bool) : True if the window is found.
        data (str) : Name of the window.
    """
    import pygetwindow as gw
    win = ""
    window_found = False

    if not windowName:
        raise ValueError("Window name cannot be empty")

    lst = gw.getAllTitles()

    for item in lst:
        if str(item).strip():
            if str(windowName).lower() in str(item).lower():
                win = item
                window_found = True
                break
    return win, window_found


def window_show_desktop():

    # Description:
    """
    Description:
        Shows the desktop by minimizing all the windows.

    Args:
        None

    Returns:
        [staus]
        status (bool) : True if the window is found.
    """

    # import section
    import pywinauto as pwa

    # Response section
    error = None
    status = False
    # data = None

    try:
        pwa.keyboard.send_keys('{VK_RWIN down} d {VK_RWIN up}')

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


def window_get_active_window():

    # Description:
    """
    Description:
        Gives you the active window name.

    Args:
        None

    Returns:
        [status, data]
        status (bool) : True if the window is found.
        data (str) : Name/Title of the active window.
    """

    # import section
    import win32gui
    import pygetwindow as gw

    # Response section
    error = None
    status = False
    data = None

    try:
        _title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        data = _title

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


def window_activate_window(window_title=''):

    # Description:
    """
    Description:
        Activates the desired window.

    Args:
        window_title  (str) : Name of the window to activate.

    Returns:
        [status]
        status (bool) : True if the window is found.
    """

    # import section
    import pygetwindow as gw

    # Response section
    error = None
    status = False
    # data = None

    try:
        if not window_title:
            raise Exception('Window title name is empty.')

        item, window_found = _window_find_exact_name(window_title)
        if window_found:
            windw = gw.getWindowsWithTitle(item)[0]

            try:
                windw.activate()
            except:
                windw.minimize()
                windw.maximize()

        else:
            raise Exception(
                'Window title name {} not found'.format(window_title))

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


def window_get_all_opened_titles_windows():

    # Description:
    """
    Description:
        Gives the title of all the existing (open) windows.

    Args:
        None

    Returns:
        [status, data]
        status (bool) : True if the window is found.
        data (list) : List of all the opened windows.
    """

    # import section
    import pygetwindow as gw

    # Response section
    error = None
    status = False
    data = None

    try:
        allTitles_lst = []
        lst = gw.getAllTitles()
        for item in lst:
            if str(item).strip() != "" and str(item).strip() not in allTitles_lst:
                allTitles_lst.append(str(item).strip())
        data = allTitles_lst

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


def window_activate_and_maximize_windows(windowName=""):

    # Description:
    """
    Description:
        Activates and maximizes the desired window.

    Args:
        windowName  (str) : Name of the window to maximize.

    Returns:
        [status]
        status (bool) : True if the window is found.
    """

    # import section
    import time
    import pygetwindow as gw

    # Response section
    error = None
    status = False
    # data = None

    try:
        if not windowName:
            raise Exception('Window title name is empty.')

        item, window_found = _window_find_exact_name(windowName)
        if window_found:
            windw = gw.getWindowsWithTitle(item)[0]

            try:
                windw.activate()
                windw.maximize()
            except:
                windw.minimize()
                time.sleep(1)
                windw.maximize()
        else:
            Exception('Window title name {} not found'.format(windowName))

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


def window_minimize_windows(windowName=""):

    # Description:
    """
    Description:
        Activates and minimizes the desired window.

    Args:
        windowName  (str) : Name of the window to miniimize.

    Returns:
        [status]
        status (bool) : True if the window is found.
    """

    # import section
    import pygetwindow as gw

    # Response section
    error = None
    status = False
    # data = None

    try:
        if not windowName:
            raise Exception('Window title name is empty.')

        item, window_found = _window_find_exact_name(windowName)
        if window_found:
            windw = gw.getWindowsWithTitle(item)[0]
            windw.minimize()
        else:
            Exception('Window title name {} not found'.format(windowName))

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


def window_close_windows(windowName=""):

    # Description:
    """
    Description:
        Close the desired window.

    Args:
        windowName  (str) : Name of the window to close.

    Returns:
        [status]
        status (bool) : True if the window is found.
    """

    # import section
    import pygetwindow as gw

    # Response section
    error = None
    status = False
    # data = None

    try:
        if not windowName:
            raise Exception('Window title name is empty.')

        item, window_found = _window_find_exact_name(windowName)
        if window_found:
            windw = gw.getWindowsWithTitle(item)[0]
            windw.close()
        else:
            Exception('Window title name {} not found'.format(windowName))

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


def launch_any_exe_bat_application(pathOfExeFile=""):

    # Description:
    """
    Description:
        Launches any exe or batch file or excel file etc.

    Args:
        pathOfExeFile (str, optional): Location of the file with extension 
        Eg: Notepad, TextEdit. Defaults to "".

    Returns:
        [status]
        Status (bool) : True if the file is found.
    """

    # import section
    import win32gui
    import win32con
    import os
    import time

    # Response section
    error = None
    status = False
    # data = None

    try:
        if not pathOfExeFile:
            raise Exception('Path of the exe file is empty.')

        try:
            os.startfile(pathOfExeFile)
            time.sleep(2)
            hwnd = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            status = True
        except Exception:
            os.startfile(pathOfExeFile)

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


def window_restore_windows(windowName=""):

    # Description:
    """
    Description:
        Restores the desired window.
    Args:
        windowName  (str) : Name of the window to restore.

    Returns:
        [status]
        Status (bool) : True if the window is found.
    """

    # import section
    import pygetwindow as gw

    # Response section
    error = None
    status = False
    # data = None

    try:
        if not windowName:
            raise Exception('Window title name is empty.')

        item, window_found = _window_find_exact_name(windowName)
        if window_found:
            windw = gw.getWindowsWithTitle(item)[0]
            windw.restore()
        else:
            Exception('Window title name {} not found'.format(windowName))

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
