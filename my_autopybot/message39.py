
def msg_box_info(msg_for_user=""):
    """
    Description:
        Display a message box with information.

    Args:
        msg_for_user (str): [description]

    Returns:
        [status]
        Status (bool) : Whether the message box was displayed or not.
    """
    try:
        if msg_for_user:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.attributes('-topmost', True)
            root.withdraw()
            tk.messagebox.showinfo('PyBOTs', msg_for_user, parent=root)
            root.destroy()
        else:
            from my_autopybot.CrashHandler import text_to_speech_error
            text_to_speech_error("Message cannot be empty")

    except Exception as ex:
        from my_autopybot.CrashHandler import report_error
        report_error(ex)
        return [False]
    else:
        return [True]


def msg_box_ask_yes_no(msg_for_user=""):
    """
    Description:
        Display a message box with information.
    Args:
        msg_for_user (str): [description]
    Returns:
        [status]
        Status (bool) : Whether the message box was displayed or not.
    """
    # Response section
    status = False

    try:
        if msg_for_user:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.attributes('-topmost', True)
            root.withdraw()
            yes_no = tk.messagebox.askyesno('PyBOTs', msg_for_user)
            root.destroy()

            if yes_no:
                status = True

        else:
            from my_autopybot.CrashHandler import text_to_speech_error
            text_to_speech_error("Message cannot be empty")

    except Exception as ex:
        from my_autopybot.CrashHandler import report_error
        report_error(ex)
    finally:
        return [status]


def msg_count_down(msg_for_user="", default_time=5):
    """
    Description:
        Display a message box with information.
    Args:
        msg_for_user (str): [description]
        default_time (int, optional): [description]. Defaults to 5.
    Returns:
        [status]
        Status (bool) : Whether the message box was displayed or not.
    """
    # Import section
    import tkinter
    from pathlib import Path
    import os
    import my_autopybot.resources as data

    # Response section
    status = False

    try:
        data_folder = data.__path__[0]
        logo_file_path = Path(os.path.join(data_folder, "pybots_logo.png"))

        def button_countdown(i, label):
            if i > 1:
                i -= 1
                label.set(i)
                root.after(1000, lambda: button_countdown(i, label))
            else:
                root.destroy()

        root = tkinter.Tk()

        # root window postion center
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        ww = root.winfo_reqwidth()
        wh = root.winfo_reqheight()
        x = (sw - ww)/2
        y = (sh - wh)/2
        root.geometry("+%d+%d" % (x, y))

        # window remove window controls
        root.overrideredirect(True)

        # add image to root
        img = tkinter.PhotoImage(file=logo_file_path)

        # reduce image size
        img = img.subsample(5, 5)

        tkinter.Label(root, image=img).pack()

        default_time = int(default_time + 1)

        button_label = tkinter.StringVar()
        button_label.set(default_time)

        # add label to root with message hello
        msg_label = tkinter.StringVar()

        if msg_for_user:
            msg_label.set(msg_for_user)
        else:
            msg_label.set("Countdown")

        tkinter.Label(root, textvariable=msg_label,
                      font=("Helvetica", 15)).pack()

        tkinter.Button(root, textvariable=button_label,
                       font=("Helvetica", 20)).pack()

        button_countdown(default_time, button_label)

        # stay on top
        root.attributes('-topmost', True)

        root.mainloop()
    except Exception as ex:
        from my_autopybot.CrashHandler import report_error
        report_error(ex)
    else:
        status = True
    finally:
        return [status]
