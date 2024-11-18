import os
from pathlib import WindowsPath
from typing import Dict, List, Union

from my_autopybot.CrashHandler import report_error

output_folder_path = os.path.join(
    os.path.abspath(r'C:\Users\Public\PyBots'), 'My-autopybot', 'Converters Folder')

if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)


def convert_csv_to_excel(input_file="", sep=",", output_folder="", output_filename="",contains_headers=True):
    """
    Args:
        input_file (str): [description]. Defaults to "".
        sep (str): [description]. Defaults to "".
        output_folder (str, optional): [description]. Defaults to "".
        output_filename (str, optional): [description]. Defaults to "".
        contains_header (bool,optional):[description]. Defaults to True
    Returns:
        [bool]: [status]
    """
    # Import section
    from my_autopybot.CrashHandler import report_error
    import os
    from pathlib import Path
    import pandas as pd
    import datetime
    # Response section
    error = None
    status = False

    # Logic section
    try:
        if not input_file:
            raise Exception("CSV File name cannot be empty")

        if not output_folder:
            output_folder = output_folder_path

        if not output_filename:
            output_filename = "excel_" + \
                str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + ".xlsx"
        else:
            output_filename = output_filename.split(".")[0] + ".xlsx"
        if not sep:
            raise Exception("Separator cannot be empty")

        excel_file_path = os.path.join(
            output_folder, output_filename)
        excel_file_path = Path(excel_file_path)
        writer = pd.ExcelWriter(excel_file_path)
        headers='infer'
        if contains_headers==False:
            headers=None
        df = pd.read_csv(input_file, sep=sep,header=headers)
        df.to_excel(writer, sheet_name='Sheet1', index=False,header=contains_headers)
        writer.save()

    except Exception as ex:
        report_error(ex)
        error = ex

    else:
        status = True

    finally:
        if error is not None:
            raise Exception(error)
        return [status]
        

def get_image_from_base64(input_text="", output_folder="", output_filename=""):
    """
    Description:
        Convert base64 string to image.
    Args:
        imgFileName (str, optional): [description]. Defaults to "".
        input_file (str, optional): [description]. Defaults to "".
        output_folder (str, optional): [description]. Defaults to "".
    Returns:
        [bool]: [status]
    """
    # Import Section
    import base64
    import os
    import datetime
    from my_autopybot.CrashHandler import report_error

    # Response Section
    error = None
    status = False

    # Logic Section
    try:
        if not input_text:
            raise Exception("Image base64 string cannot be empty")

        if not output_folder:
            output_folder = output_folder_path

        if not output_filename:
            output_filename = "image_" + \
                str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + ".png"
        else:
            if not str(output_filename).endswith(".*"):
                output_filename = output_filename + ".png"
            else:
                output_filename = output_filename

        input_text = bytes(input_text, 'utf-8')
        if os.path.exists(output_folder):
            try:
                img_binary = base64.decodebytes(input_text)
                with open(os.path.join(output_folder, output_filename), "wb") as f:
                    f.write(img_binary)
            except Exception as ex:
                report_error(ex)
                error = ex
        else:
            raise Exception("Image folder path does not exist")
    except Exception as ex:
        report_error(ex)
        error = ex
    else:
        status = True
    finally:
        if error is not None:
            raise Exception(error)
        return [status]


def convert_image_to_base64(input_file=""):
    """
    Description:
        Convert image to base64 string.
    Args:
        input_file (str, optional): [description]. Defaults to "".
    Returns:
        [bool]: [status]
    """
    # Import section
    import base64
    import os
    from my_autopybot.CrashHandler import report_error

    # Response section
    error = None
    status = False
    data = None

    # Logic section
    try:
        if not input_file:
            raise Exception("Image file name cannot be empty")

        if os.path.exists(input_file):
            with open(input_file, "rb") as f:
                data = base64.b64encode(f.read())
        else:
            raise Exception("Image file does not exist")
    except Exception as ex:
        report_error(ex)
        error = ex
    else:
        status = True
    finally:
        if error is not None:
            raise Exception(error)
        return [status, data]
# print(image_to_base64(r"C:\Users\PyBots\Desktop\images\image.jpg"))


def excel_change_corrupt_xls_to_xlsx(input_file='', input_sheetname='', output_folder='', output_filename=''):
    '''
        Repair corrupt file to regular file and then convert it to xlsx.
        status : Done.
    '''

    # Import section
    import os
    from my_autopybot.CrashHandler import report_error
    import io
    from xlwt import Workbook
    from xls2xlsx import XLS2XLSX
    import datetime
    from pathlib import Path

    # Response section
    error = None
    status = False
    data = None

    # Logic section
    try:
        if not input_file:
            raise Exception("XLS File name cannot be empty")

        if not input_sheetname:
            raise Exception("XLS Sheet name cannot be empty")

        if not output_folder:
            output_folder = output_folder_path

        if not output_filename:
            output_filename = os.path.join(output_folder, str(Path(input_file).stem), str(
                datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + ".xlsx")
        else:
            output_filename = output_filename.split(".")[0] + ".xlsx"
            output_filename = os.path.join(
                output_folder, str(output_filename))

        # Opening the file
        file1 = io.open(input_file, "r")
        data = file1.readlines()

        # Creating a workbook object
        xldoc = Workbook()
        # Adding a sheet to the workbook object
        sheet = xldoc.add_sheet(input_sheetname, cell_overwrite_ok=True)
        # Iterating and saving the data to sheet
        for i, row in enumerate(data):
            # Two things are done here
            # Removing the '\n' which comes while reading the file using io.open
            # Getting the values after splitting using '\t'
            for j, val in enumerate(row.replace('\n', '').split('\t')):
                sheet.write(i, j, val)

        # Saving the file as a normal xls excel file
        xldoc.save(input_file)

        # checking the downloaded file is present or not
        if os.path.exists(input_file):
            # converting xls to xlsx
            x2x = XLS2XLSX(input_file)
            x2x.to_xlsx(output_filename)

    except Exception as ex:
        report_error(ex)
        error = ex

    else:
        status = True
    finally:
        if error is not None:
            raise Exception(error)
        return [status]


def excel_convert_xls_to_xlsx(input_file='', output_folder='', output_filename=''):
    """
    Converts given XLS file to XLSX
    """
    # Import section
    from my_autopybot.CrashHandler import report_error
    import os
    from xls2xlsx import XLS2XLSX
    from pathlib import Path
    import datetime

    # Response section
    error = None
    status = False

    # Logic section
    try:
        if not input_file:
            raise Exception("XLS File name cannot be empty")

        if not output_folder:
            output_folder = output_folder_path

        if not output_filename:
            output_filename = os.path.join(output_folder, str(Path(input_file).stem), str(
                datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + ".xlsx")
        else:
            output_filename = os.path.join(
                output_folder, str(output_filename)+".xlsx")

        # Checking the path and then converting it to xlsx file
        if os.path.exists(input_file):
            # converting xls to xlsx
            x2x = XLS2XLSX(input_file)
            x2x.to_xlsx(output_filename)
    except Exception as ex:
        report_error(ex)
        error = ex

    else:
        status = True
        # # If the function returns a value, it should be assigned to the data variable.
    finally:
        if error is not None:
            raise Exception(error)
        return [status]


def convert_image_jpg_to_png(input_filepath="", output_folder="", output_filename=""):

    # Description:
    """
   Convert the image from jpg to png

    Args:
        input_image_path (str): The path of the input image
        output_folder_path (str): The path of the output folder

    Returns:
        [bool]: Whether the function is successful or failed.
    """

    # import section

    from pathlib import Path
    import os
    from PIL import Image
    import datetime

    # Response section
    error = None
    status = False
    # Logic section
    try:

        if not input_filepath:
            raise Exception("Enter the valid input image path")
        if not output_folder:
            output_folder = output_folder_path
        if not output_filename:
            output_filename = os.path.join(output_folder, str(Path(input_filepath).stem), str(
                datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + ".png")
        else:
            output_filename = os.path.join(
                output_folder, str(output_filename) + ".png")

        im = Image.open(input_filepath)
        rgb_im = im.convert('RGB')
        rgb_im.save(output_filename)

        status = True

    except Exception as ex:
        report_error(ex)
        error = ex

    else:
        status = True
    finally:
        if error is not None:
            raise Exception(error)
        return [status]


def convert__image_png_to_jpg(input_filepath="", output_folder="", output_filename=""):

    # Description:
    """
   Convert the image from png to jpg

    Args:
        input_image_path (str): The path of the input image
        output_folder_path (str): The path of the output folder

    Returns:
        [bool]: Whether the function is successful or failed.
    """

    # import section

    from pathlib import Path
    import os
    from PIL import Image
    import datetime

    # Response section
    error = None
    status = False
    # Logic section
    try:

        if not input_filepath:
            raise Exception("Enter the valid input image path")
        if not output_folder:
            output_folder = output_folder_path
        if not output_filename:
            output_filename = os.path.join(output_folder, str(Path(input_filepath).stem), str(
                datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + ".jpg")
        else:
            output_filename = os.path.join(
                output_folder, str(output_filename) + ".jpg")

        im = Image.open(input_filepath)
        rgb_im = im.convert('RGB')
        rgb_im.save(output_filename)

        status = True

    except Exception as ex:
        report_error(ex)
        error = ex

    else:
        status = True
    finally:
        if error is not None:
            raise Exception(error)
        return [status]


def excel_to_colored_html(input_filepath="", output_folder="", output_filename=""):

    # Description:
    """
    Converts given Excel to HTML preserving the Excel format and saves in same folder as .html
    """

    # import section
    from pathlib import Path
    from xlsx2html import xlsx2html
    import datetime

    # Response section
    error = None
    status = False

    try:

        if not input_filepath:
            raise Exception("Please provide the excel path")
        if not output_folder:
            output_folder = output_folder_path
        if not output_filename:
            output_filename = os.path.join(output_folder, str(Path(input_filepath).stem)+'_'+str(
                datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + ".html")
        else:
            output_filename = os.path.join(
                output_folder, output_filename+'.html')

        xlsx2html(input_filepath, output_filename)
        os.startfile(output_folder)

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


# excel_to_colored_html(input_filepath=r"C:\Users\PyBots\Desktop\dummy.xlsx",
#                       output_folder=r"C:\Users\PyBots\My autopybot", output_filename="output")



def excel_to_colored_html_1(input_excel_path : Union[str, WindowsPath], sheet_name : str, output_folder_path : Union[str, WindowsPath]) -> None:
    """
    Description: Converts given Excel to HTML preserving the Excel format and saves in same folder as .html

    Parameters:
    input_excel_path (Union[str, WindowsPath]): Input Excel path
    sheet_name (str): Sheet name
    output_folder_path (Union[str, WindowsPath]): Output folder path

    Returns:
    None

    Example:
    
    """
    # Import section
    from pathlib import Path
    from xlsx2html import xlsx2html
    import datetime

    # Code section
    output_filename = os.path.join(output_folder_path, str(Path(input_excel_path).stem)+'_'+str(
        datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + ".html")
    
    xlsx2html(input_excel_path, output_filename, sheet=sheet_name)

# excel_to_colored_html_1(input_excel_path=r"C:\Users\mrmay\OneDrive\Desktop\Excel Templates\Raw Data - Copy\PreviousMobileOrdersFlatReport.xlsx",
#                        sheet_name="PreviousMobileOrdersFlatReport", output_folder_path=r"C:\Users\mrmay\OneDrive\Desktop\Excel Templates\Raw Data - Copy")

