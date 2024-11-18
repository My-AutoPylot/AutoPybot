import datetime
import os
import pandas as pd
from pathlib import WindowsPath
from typing import Dict, List, Union

output_folder_path = os.path.join(
    os.path.abspath(r'C:\Users\Public\PyBots'), 'My-autopybot', 'PDF Folder')

# create output folder if not present
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)


def pdf_extract_all_tables(pdf_file_path: str = "", table_with_borders : bool = True, vertical_strategy : str = "text", horizontal_strategy : str = "text"):
    """
    Description:
        Extract all tables from a pdf file and save them to a text file.
    Args:
        pdf_file_path (str): [description]. Defaults to "".
        output_folder (str): [description]. Defaults to "".
        output_file_name (str): [description]. Defaults to "".
    Returns:
        [status]
        status (bool) : Whether the pdf file was extracted or not.
    """
    # Import Section
    import pdfplumber
    import pandas as pd
    from datetime import datetime
    
    pdf = pdfplumber.open(pdf_file_path)

    tables = []

    if table_with_borders:
        for each_page in pdf.pages:
            tables.append(each_page.extract_tables())
    else:
            # {
        #     "vertical_strategy": "text",
        #     "horizontal_strategy": "text"
        # }
        table_settings =             {
            "vertical_strategy": vertical_strategy,
            "horizontal_strategy": horizontal_strategy,
            "explicit_vertical_lines": [],
            "explicit_horizontal_lines": [],
            "snap_tolerance": 3,
            "snap_x_tolerance": 3,
            "snap_y_tolerance": 3,
            "join_tolerance": 3,
            "join_x_tolerance": 3,
            "join_y_tolerance": 3,
            "edge_min_length": 3,
            "min_words_vertical": 3,
            "min_words_horizontal": 1,
            "keep_blank_chars": False,
            "text_tolerance": 3,
            "text_x_tolerance": 3,
            "text_y_tolerance": 3,
            "intersection_tolerance": 3,
            "intersection_x_tolerance": 3,
            "intersection_y_tolerance": 3,
        }

        for each_page in pdf.pages:
            tables.append(each_page.extract_tables(table_settings))

    for table in tables:
        df_main = []
        # list of the rows to dataframe
        for i in range(len(table)):
            df = pd.DataFrame(table[i])
            df_main.append(df)

        df_main = pd.concat(df_main)

    return df_main

# print(pdf_extract_all_tables(r"C:\Users\mrmay\Downloads\background-checks.pdf", False))
# print(pdf_extract_all_tables(r"C:\Users\mrmay\Downloads\AbhinavGupta_31YrsMale_LabReport.pdf", False))
# print(pdf_extract_all_tables(r"C:\Users\mrmay\Downloads\invitationtobearesourceperson\Schedule.pdf", True))

def pdf_extract_table(pdf_file_path: str = "", table_number: int = 0, page_number: int = 0):
    """
    Description:
        Extract a table from a pdf file and save it to a text file.
    Args:
        pdf_file_path (str): [description]. Defaults to "".
        table_number (int): [description]. Defaults to 0.
        page_number (int): [description]. Defaults to 0.
        output_folder (str): [description]. Defaults to "".
        output_file_name (str): [description]. Defaults to "".
    Returns:
        [status]
        status (bool) : Whether the pdf file was extracted or not.
    """
    # Import Section
    import pdfplumber
    import pandas as pd
    import datetime
    from my_autopybot.CrashHandler import report_error

    # Response Section
    error = None
    status = False
    Data = None

    # Logic Section
    try:
        if not pdf_file_path:
            raise Exception("PDF file path cannot be empty")

        elif not table_number:
            raise Exception("Table number cannot be empty")

        elif not page_number:
            raise Exception("Page number cannot be empty")

        # check if pdf_file_path exists
        if not os.path.exists(pdf_file_path):
            raise Exception("PDF file path does not exist")

        else:
            pdf = pdfplumber.open(pdf_file_path)

            tables = []

            for each_page in pdf.pages:
                tables.append(each_page.extract_tables())

            # list of the rows to dataframe
            df = pd.DataFrame(tables[page_number - 1][table_number - 1],
                              columns=tables[page_number - 1][table_number - 1][0])
            df = df.drop(df.index[0])
            df = df.reset_index(drop=True)

            Data = df

    except Exception as ex:
        report_error(ex)
        error = ex

    else:
        status = True

    finally:
        if error is not None:
            raise Exception(error)
        return [status, Data]

#get filled data from pdf FORM using PyPDF2
def get_filled_data_from_pdf_form_pypdf(pdf_file_path: Union[str, WindowsPath]) -> dict:
    """
    Description:
        Get filled data from a pdf form.
    Args:
        pdf_file_path (str): [description]. Defaults to "".
    Returns:
        [status]
        status (bool) : Whether the pdf file was extracted or not.
    """
    # Import Section
    import PyPDF2
    import pandas as pd
    from my_autopybot.CrashHandler import report_error

    # Logic Section
    f = PyPDF2.PdfFileReader(pdf_file_path)
    form_fields = f.getFields()

    return form_fields

# get_filled_data_from_pdf_form_pypdf(r"C:\Users\mrmay\Downloads\OoPdfFormExample.pdf")

def get_filled_data_from_pdf_form_fillpdf(input_pdf_path: Union[str, WindowsPath]) -> dict:
    """
    Description:
        Get filled data from a pdf form.
    Args:
        input_pdf_path (str): [description]. Defaults to "".
    Returns:
        [status]
        status (bool) : Whether the pdf file was extracted or not.
    """
    # Import Section
    import fillpdf
    from fillpdf import fillpdfs
    
    # Logic Section
    return fillpdfs.get_form_fields(input_pdf_path, sort=False, page_number=None)
    
# print(get_filled_data_from_pdf_form_fillpdf(r"C:\Users\mrmay\Downloads\OoPdfFormExample.pdf"))    
# get_filled_data_from_pdf_form_pdfminer(r"C:\Users\mrmay\Downloads\OoPdfFormExample.pdf")
# 

#rotate pdf pages
def rotate_pdf_pages(pdf_file_path: str = "", output_folder: str = "", output_file_name: str = "", degree: int = 90):
    """
    Description:
        Rotate pdf pages.
    Args:
        pdf_file_path (str): [description]. Defaults to "".
        output_folder (str): [description]. Defaults to "".
        output_file_name (str): [description]. Defaults to "".
    Returns:
        [status]
        status (bool) : Whether the pdf file was extracted or not.
    """
    # Import Section
    import PyPDF2
    from PyPDF2 import PdfFileWriter, PdfFileReader
    from pathlib import Path
    import os
    from my_autopybot.CrashHandler import report_error

    input_pdf = PdfFileReader(open(pdf_file_path, "rb"))
    output_pdf = PdfFileWriter()

    for i in range(input_pdf.getNumPages()):
        page = input_pdf.getPage(i)
        page.rotateClockwise(degree)
        output_pdf.addPage(page)

    if not output_folder:
        output_folder = Path(pdf_file_path).parent

    if not output_file_name:
        output_file_name = Path(pdf_file_path).stem + "_rotated.pdf"

    with open(os.path.join(output_folder, output_file_name), "wb") as outputStream:
        output_pdf.write(outputStream)

# rotate_pdf_pages(r"C:\Users\mrmay\Downloads\OoPdfFormExample.pdf", r"C:\Users\mrmay\Downloads", "OoPdfFormExample_rotated.pdf")
# rotate_pdf_pages(r"C:\Users\mrmay\Downloads\3 Day FDP on Metaverse - Information Brochure .pdf", r"C:\Users\mrmay\Downloads", "3 Day FDP on Metaverse - Information Brochure_rotated.pdf")
# rotate_pdf_pages(r"C:\Users\mrmay\OneDrive\Documents\Priya Docs\SIRI\siri rate list.pdf", r"C:\Users\mrmay\OneDrive\Documents\Priya Docs\SIRI", "siri rate list_rotated.pdf", -90)


#extrat text from pdf
def extract_text_from_pdf(pdf_file_path: str, page_num : int = 0) -> str:
    """
    Description:
        Extract text from a pdf file.
    Args:
        pdf_file_path (str): [description]. Defaults to "".
    Returns:
        [status]
        status (bool) : Whether the pdf file was extracted or not.
    """
    # Import Section
    import PyPDF2
    from PyPDF2 import PdfFileWriter, PdfFileReader
    from pathlib import Path
    import os
    from my_autopybot.CrashHandler import report_error

    # Logic Section
    pdf_file = open(pdf_file_path, 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    
    #read text from all pages
    if page_num == 0:
        text = ""
        for i in range(number_of_pages):
            page = read_pdf.getPage(i)
            text += page.extractText()
    else:
        page = read_pdf.getPage(page_num)
        text = page.extractText()

    return text

# print(extract_text_from_pdf(r"C:\Users\mrmay\Downloads\OoPdfFormExample.pdf"))
# print(extract_text_from_pdf(r"C:\Users\mrmay\Downloads\3 Day FDP on Metaverse - Information Brochure .pdf", 2))

#merge pdf files
def merge_pdf_files(pdf_file_paths: list, output_folder: str = "", output_file_name: str = ""):
    """
    Description:
        Merge pdf files.
    Args:
        pdf_file_paths (list): [description]. Defaults to [].
        output_folder (str): [description]. Defaults to "".
        output_file_name (str): [description]. Defaults to "".
    Returns:
        [status]
        status (bool) : Whether the pdf file was extracted or not.
    """
    # Import Section
    import PyPDF2
    from PyPDF2 import PdfFileWriter, PdfFileReader
    from pathlib import Path
    import os
    
    # Logic Section
    pdf_writer = PdfFileWriter()

    for path in pdf_file_paths:
        pdf_reader = PyPDF2.PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))

    if not output_folder:
        output_folder = Path(pdf_file_paths[0]).parent

    if not output_file_name:
        output_file_name = "merged_pdf.pdf"

    with open(os.path.join(output_folder, output_file_name), "wb") as out:
        pdf_writer.write(out)

# merge_pdf_files([r"C:\Users\mrmay\Downloads\OoPdfFormExample.pdf", r"C:\Users\mrmay\Downloads\3 Day FDP on Metaverse - Information Brochure .pdf"], r"C:\Users\mrmay\Downloads", "merged_pdf.pdf")

#split pdf files
def split_pdf_files(pdf_file_path: str, output_folder: str = "", output_file_name: str = ""):
    """
    Description:
        Split pdf files.
    Args:
        pdf_file_path (str): [description]. Defaults to "".
        output_folder (str): [description]. Defaults to "".
        output_file_name (str): [description]. Defaults to "".
    """
    # Import Section
    import PyPDF2
    from PyPDF2 import PdfFileWriter, PdfFileReader
    from pathlib import Path
    import os
    
    # Logic Section
    if not output_folder:
        output_folder = Path(pdf_file_path).parent

    pdf_reader = PdfFileReader(pdf_file_path)
    for page in range(pdf_reader.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf_reader.getPage(page))

        new_output_file_name = Path(output_file_name).stem + "_page_" + str(page) + ".pdf"

        with open(os.path.join(output_folder, new_output_file_name), "wb") as out:
            pdf_writer.write(out)

#create PDF from image files of a folder
def create_pdf_from_images(image_folder_path: str, output_folder: str = "", output_file_name: str = ""):
    """
    Description:
        Create PDF from image files of a folder.
    Args:
        image_folder_path (str): [description]. Defaults to "".
        output_folder (str): [description]. Defaults to "".
        output_file_name (str): [description]. Defaults to "".
    """
    # Import Section
    from PIL import Image
    from pathlib import Path
    import os
    from fpdf import FPDF
    from my_autopybot.CrashHandler import report_error

    # Logic Section
    if not output_folder:
        output_folder = Path(image_folder_path).parent

    if not output_file_name:
        output_file_name = Path(image_folder_path).stem + ".pdf"

    image_list = os.listdir(image_folder_path)
    image_list.sort()

    pdf = FPDF()
    for image in image_list:
        pdf.add_page()
        pdf.image(os.path.join(image_folder_path, image), 0, 0, 210, 297)
    pdf.output(os.path.join(output_folder, output_file_name), "F")


create_pdf_from_images(r"C:\Users\mrmay\OneDrive\Documents\Mayur Docs\NEFT", r"C:\Users\mrmay\OneDrive\Documents\Mayur Docs\NEFT", "NEFT-FORM.pdf")

# split_pdf_files(r"C:\Users\mrmay\Downloads\merged_pdf.pdf", r"C:\Users\mrmay\Downloads", "Split.pdf")

# Compress PDF file








