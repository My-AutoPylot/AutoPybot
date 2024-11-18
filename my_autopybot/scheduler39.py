import my_autopybot as ap
import os
import shutil
import random
output_folder_path = os.path.join(
    os.path.abspath(r'C:\Users\Public\PyBots'), 'My-autopybot', 'Scheduler Folder')


if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)


class Encryptor:
    def __init__(self, file_path, bot_name: str, bot_id):
        if not os.path.exists(file_path):
            raise Exception('{} does not exists!'.format(file_path))

        bot_folder = os.path.join(output_folder_path, bot_name)
        if not os.path.exists(bot_folder):
            os.makedirs(bot_folder)

        self.bot_id = bot_id

        self.bot_name = bot_name.replace('-', '_').replace(' ', '_')
        self.bot_name_new_path = os.path.join(bot_folder, self.bot_name+'.py')

        self.bot_folder = bot_folder

        # if not self.file_extension == '.py':
        #     raise Exception(
        #         '{} is not .py format!'.format(self.file_extension))
        # Creating .pvx file
        self.new_setup_path = os.path.join(bot_folder, 'setup.py')

        shutil.copy(file_path, self.bot_name_new_path)
        self.setup_file()
        self.encrypt()

    def setup_file(self):
        with open(self.new_setup_path, '+w') as file:
            file.write("from distutils.core import setup\n"
                       "from Cython.Build import cythonize\n\n"
                       ""
                       "setup(ext_modules=cythonize(r'{}', language_level=3))".format(self.bot_name_new_path))

    def encrypt(self):
        import sys
        import subprocess

        os.chdir(self.bot_folder)
        subprocess.run([sys.executable, self.new_setup_path,
                       'build_ext', '--inplace'])

        self.batch_file_path = self.bot_name_new_path.replace(".py", ".bat")

        cmd_str = f'"{sys.executable}" -c "import {self.bot_name}" --email {ap.user_email} --name {self.bot_name} --id {self.bot_id}\n'

        f = open(self.batch_file_path, 'w', encoding="utf-8")
        f.write("@echo off\n")
        f.write("cd {}\n".format(self.bot_folder))
        f.write(cmd_str)
        f.write("exit")
        f.close()

        os.remove(self.bot_name_new_path)
        os.remove(self.new_setup_path)
        test_name = self.bot_name_new_path.replace(".py", ".c")
        os.remove(test_name)
        shutil.rmtree(os.path.join(self.bot_folder, 'build'))


def create_batch_file(py_file_path="", bot_name=""):
    """
    Description:
        Creates .bat file for the given application / exe or even .pyw BOT developed by you. This is required in Task Scheduler.

    Args:
        py_file_path (str): [description]. Defaults to "".

    Returns:
        [status]
        status (bool): Whether the batch file is created or not.
    """
    # Import Section
    import os
    from my_autopybot.CrashHandler import report_error
    from pathlib import Path
    import sys
    import shutil
    import random

    # Response Section
    error = None
    status = False
    data = ""

    # Logic Section
    try:
        if not py_file_path:
            raise Exception("Python file path cannot be empty")

        if not os.path.exists(py_file_path):
            raise Exception("Python file path does not exist")

        if not os.path.isfile(py_file_path):
            raise Exception("Python file path is not a file")
        if not bot_name:
            bot_name = "autopybot_bot_" + str(random.randint(1, 100))

        bot_folder = os.path.join(output_folder_path, bot_name)
        if not os.path.exists(bot_folder):
            os.makedirs(bot_folder)

        pyw_file_path = os.path.join(
            bot_folder, os.path.basename(py_file_path).replace(".py", ".pyw"))
        shutil.copy(py_file_path, pyw_file_path)
        print("Python file converted to .bat file at " + str(pyw_file_path))

        cmd = ""

        batch_file_path = str(pyw_file_path).replace("pyw", "bat")
        cmd = "start \"\" " + '"' + \
            str(sys.executable).replace(".exe", "w.exe") + \
            '" ' + '"' + pyw_file_path + '" /popup\n'

        f = open(batch_file_path, 'w', encoding="utf-8")
        f.write("@echo off\n")
        f.write("cd /d " + str(Path(pyw_file_path).parent) + "\n")
        f.write(cmd)
        f.write("exit")
        f.close()

        print("Batch file created at " + str(batch_file_path))
    except Exception as ex:
        report_error(ex)
        error = ex

    else:
        status = True
        data = batch_file_path

    finally:
        if error is not None:
            raise Exception(error)
        return [status, data]


def create_py_file(code="", folder_path="", file_name="", bot_name=""):
    """
    Description:
        Creates .py file from the given code.

    Args:
        code (str): [description]. Defaults to "".
        folder_path (str): [description]. Defaults to "".


    Returns:
        [status]
        status (bool): Whether the .py file is created or not.
    """
    # Import Section
    import os
    from my_autopybot.CrashHandler import report_error
    import random

    # Response Section
    error = None
    status = False
    data = ""

    # Logic Section
    try:
        if not code:
            raise Exception("Code cannot be empty")
        if not folder_path:
            folder_path = output_folder_path
            os.makedirs(folder_path)
        if not bot_name:
            bot_name = "autopybot_bot_file_" + str(random.randint(1, 100))
        if not file_name:
            file_name = str(bot_name) + ".py"

        py_file_path = os.path.join(
            folder_path, file_name)
        f = open(py_file_path, 'w', encoding="utf-8")
        f.write(code)
        f.close()

        print("Python file created at " + str(py_file_path))
    except Exception as ex:
        report_error(ex)
        error = ex

    else:
        status = True
        data = py_file_path

    finally:
        if error is not None:
            raise Exception(error)
        return [status, data]


def schedule_create_task_windows(batch_file_path="", bot_name="", weekly_or_daily="D", week_day="Sun", start_time_hh_mm_24_hr_frmt="11:00"):
    """
    Description:
        Schedules (weekly & daily options as of now) the current BOT (.bat) using Windows Task Scheduler. Please call create_batch_file() function before using this function to convert .pyw file to .bat
    Args:
        batch_file_path (str): [description]. Defaults to "".
        bot_name (str): [description]. Defaults to "".
        weekly_or_daily (str): [description]. Defaults to "D".
        week_day (str): [description]. Defaults to "Sun".
        start_time_hh_mm_24_hr_frmt (str): [description]. Defaults to "11:00".
    Returns:
        Status (bool): Whether the task is scheduled or not.
    """

    # Import Section
    import os
    from my_autopybot.CrashHandler import report_error
    import subprocess

    # Response Section
    error = None
    status = False

    # Logic Section
    try:
        str_cmd = ""

        if not batch_file_path:
            raise Exception("Batch file path cannot be empty")

        if weekly_or_daily == "D":
            str_cmd = r"powershell.exe schtasks /create  /SC DAILY /tn PyBOTs\'{}' /tr '{}' /st {} /f ".format(
                str(bot_name), batch_file_path, start_time_hh_mm_24_hr_frmt)
        elif weekly_or_daily == "W":
            str_cmd = r"powershell.exe schtasks /create  /SC WEEKLY  /d {} /tn PyBOTs\'{}' /tr '{}' /st {} /f ".format(
                week_day, str(bot_name), batch_file_path, start_time_hh_mm_24_hr_frmt)

        subprocess.call(str_cmd)

    except Exception as ex:
        report_error(ex)
        error = ex

    else:
        status = True

    finally:
        if error is not None:
            raise Exception(error)
        return [status]

# schedule_create_task_windows(r"C:\Users\mrmay\OneDrive\Desktop\mmv1.bat",1,"D","Sun","12:00")


def schedule_delete_task(bot_name=""):
    """
    Description:
        Deletes already scheduled task. Asks user to supply task_name used during scheduling the task. You can also perform this action from Windows Task Scheduler.
    Args:
        bot_name (str): [description]. Defaults to "".
    Returns:
        Status (bool): Whether the task is deleted or not.
    """

    # Import Section
    import os
    from my_autopybot.CrashHandler import report_error
    import subprocess

    # Response Section
    error = None
    status = False

    # Logic Section
    try:
        if not bot_name:
            raise Exception("Bot name cannot be empty")

        str_cmd = r"powershell.exe schtasks /delete /tn PyBOTs\'{}' /f ".format(
            bot_name)

        subprocess.call(str_cmd)

        # delete the bot folder
        bot_folder_path = os.path.join(output_folder_path, str(bot_name))
        if os.path.exists(bot_folder_path):
            shutil.rmtree(bot_folder_path)

    except Exception as ex:
        report_error(ex)
        error = ex

    else:
        status = True

    finally:
        if error is not None:
            raise Exception(error)
        return [status]

# schedule_delete_task_windows(2)


def schedule_py_file(filepath, bot_name, bot_id, weekly_or_daily, week_day, start_time_hh_mm_24_hr_frmt):
    """
    Description:
        Schedules the given .py file using Windows Task Scheduler.
    Args:
        filepath (str): [description].
        bot_name (str): [description].
        weekly_or_daily (str): [description].
        week_day (str): [description].
        start_time_hh_mm_24_hr_frmt (str): [description].
    Returns:
        Status (bool): Whether the task is scheduled or not.
    """

    # Import Section
    import os
    from my_autopybot.CrashHandler import report_error
    # from my_autopybot.encrypt import Encryptor

    # Response Section
    error = None
    status = False

    # Logic Section
    try:
        if not filepath:
            raise Exception("File path cannot be empty")

        if not os.path.exists(filepath):
            raise Exception("File path does not exist")

        if not os.path.isfile(filepath):
            raise Exception("File path is not a file")

        # status, batch_path = create_batch_file(filepath, bot_name)
        enc_class = Encryptor(filepath, bot_name, bot_id)
        batch_path = enc_class.batch_file_path
        status = schedule_create_task_windows(
            batch_path, bot_name, weekly_or_daily, week_day, start_time_hh_mm_24_hr_frmt)
        if not status:
            raise Exception("Error in scheduling task")

    except Exception as ex:
        report_error(ex)
        error = ex

    else:
        status = status

    finally:
        if error is not None:
            raise Exception(error)
        return [status]

# schedule_py_file(r"C:\Users\mrmay\OneDrive\Desktop\test1.py", "mmv1", "W", "Mon,Fri", "02:00")


def schedule_code(code, bot_name, weekly_or_daily, week_day, start_time_hh_mm_24_hr_frmt):
    """
    Description:
        Schedules the given python code using Windows Task Scheduler.
    Args:
        code (str): [description].
        bot_name (str): [description].
        weekly_or_daily (str): [description].
        week_day (str): [description].
        start_time_hh_mm_24_hr_frmt (str): [description].
    Returns:
        [bool]: [status].
    """

    # Import Section
    import os
    from my_autopybot.CrashHandler import report_error

    # Response Section
    error = None
    status = False

    # Logic Section
    try:
        if not code:
            raise Exception("Code cannot be empty")

        if not bot_name:
            raise Exception("Bot name cannot be empty")

        status, filepath = create_py_file(code, bot_name=bot_name)
        print(filepath)

        schedule_py_file(filepath, bot_name, weekly_or_daily,
                         week_day, start_time_hh_mm_24_hr_frmt)

    except Exception as ex:
        report_error(ex)
        error = ex

    else:
        status = status

    finally:
        if error is not None:
            raise Exception(error)
        return [status]


# schedule_py_file(r"C:\Users\PyBots\Desktop\test.py",
#                  'This is name 126', "D", "Sun", "12:00")

# schedule_code("""
# import subprocess


# def msg_box_info(msg_for_user=""):

#     import tkinter as tk
#     from tkinter import messagebox
#     root = tk.Tk()
#     root.withdraw()
#     tk.messagebox.showinfo('PyBOTs', msg_for_user, parent=root)
#     root.destroy()


# msg_box_info("Murali Code 456")

# # run command dir in powershell
# # subprocess.call(r"powershell.exe dir")

# # run command dir in cmd
# # subprocess.call(r"cmd.exe /c dir")
# """,
#               'Murali Code3', "W", "Mon", "02:00")

# schedule_delete_task("Murali Code3")

# if __name__ == "__main__":
#     # tr = Encryptor(r"C:\Users\PyBots\Desktop\heere\test1.py", 'BOTNAME')
#     # print(tr.batch_file_path, 'hj')
#     schedule_py_file(r"C:\Users\PyBots\Desktop\heere\test1.py",
#                      "Botname 1", "sdsd-sds-d54s5d4s-dsd4sdsd", "W", "Mon,Fri", "02:00")
