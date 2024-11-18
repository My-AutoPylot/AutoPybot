from my_autopybot.CrashHandler import report_error


def folder_read_text_file(txt_file_path=""):

    # Description:
    """
    Description:
        Reads from a given text file and returns entire contents as a single list
    Args:
        txt_file_path (str) : path to the text file.
    Returns:
        [status, data] 
        status (bool) - True if the file is read successfully.
        data (List) - list of all the contents of the text file.

    """

    # import section
    # Response section
    error = None
    status = False
    data = None

    try:
        if not txt_file_path:
            raise Exception("Text file path is empty")

        with open(txt_file_path) as f:
            file_contents = f.readlines()
        data = file_contents

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


def folder_write_text_file(txt_file_path="", contents=""):
    # Description:
    """
    Description:
        Writes to a given text file and returns entire contents as a single list
    Args:
        txt_file_path (str) : path to the text file.
        contents (str) : contents to be written to the text file.
    Returns:
        [status, data]
        status (bool) - True if the file is read successfully.
        data (List) - list of all the contents of the text file.
    """

    # import section

    # Response section
    error = None
    status = False
    data = None

    try:

        if not txt_file_path:
            raise Exception("Text file path is empty")

        if not contents:
            raise Exception("Contents is empty")

        f = open(txt_file_path, 'w', encoding="utf-8")
        f.writelines(str(contents))
        f.close()

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


def folder_create(strFolderPath=""):
    # Description:
    """
    Description:
        while making leaf directory if any intermediate-level directory is missing,
        folder_create() method will create them all.
    Args:
        folderPath (str) : path to the folder where the folder is to be created.

    Returns:
        [status]
        status (bool) - True if the folder is created successfully.
    """

    # import section
    import os
    # Response section
    error = None
    status = False
    data = None

    try:
        if not strFolderPath:
            raise Exception("Folder path is empty")

        if not os.path.exists(strFolderPath):
            os.makedirs(strFolderPath, exist_ok=True)

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


def folder_create_text_file(textFolderPath="", txtFileName="", custom=False):
    # Description:
    """
    Description:
        Creates Text file in the given path.
        Internally this uses folder_create() method to create folders if the folder/s does not exist.
        automatically adds txt extension if not given in textFilePath.

    Args:
        textFolderPath (str) : path to the folder where the text file is to be created.
        txtFileName (str) : name of the text file.
        custom (bool) : True if the text file name is to be customised.

    Returns:
        [status]
        status (bool) - True if the file is created successfully.
    """

    # import section
    import os
    from pathlib import Path
    # Response section
    error = None
    status = False
    data = None

    try:
        if not textFolderPath:
            raise Exception("Text file path is empty")

        if not txtFileName:
            raise Exception("Text file name is empty")

        if not custom:
            if ".txt" not in txtFileName:
                txtFileName = txtFileName + ".txt"

        if not os.path.exists(textFolderPath):
            folder_create(textFolderPath)

        file_path = os.path.join(textFolderPath, txtFileName)
        file_path = Path(file_path)

        f = open(file_path, 'w', encoding="utf-8")
        f.close()
        data = file_path

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


def folder_get_all_filenames_as_list(strFolderPath="", extension='all'):
    # Description:
    """
    Description:
        Get all the files of the given folder in a list.

    Args:
        strFolderPath  (str) : Location of the folder.
        extension      (str) : extention of the file. by default all the files will be listed regarless of the extension.

    Returns:
        [status, data]
        status (bool) - True if the file is read successfully.
        data (List) - list of all the files in the folder.
    """

    # import section
    import os
    # Response section
    error = None
    status = False
    data = None

    try:
        if not strFolderPath:
            raise Exception("Folder path is empty")

        if extension == "all":
            allFilesOfaFolderAsLst = [
                f for f in os.listdir(strFolderPath)]

        else:
            # check if the extension is given or not
            if not extension.startswith("."):
                extension = "." + str(extension)

            allFilesOfaFolderAsLst = [
                f for f in os.listdir(strFolderPath) if f.endswith(extension)]

        data = allFilesOfaFolderAsLst

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


def folder_delete_all_files(fullPathOfTheFolder="", file_extension_without_dot="all", print_status=False):

    # Description:
    """
    Description:
        Deletes all the files of the given folder

    Args:
        fullPathOfTheFolder  (str) : Location of the folder.
        extension            (str) : extention of the file. by default all the files will be deleted inside the given folder 
                                    regarless of the extension.
    Returns:
        [status]
        status (bool) - True if the file is deleted successfully.
    """

    # import section
    import os
    from pathlib import Path
    # Response section
    error = None
    status = False
    # data = None

    try:
        if not fullPathOfTheFolder:
            raise Exception("Folder path is empty")

        count = 0
        # check if file_extension_without_dot begins

        if not file_extension_without_dot.startswith("."):
            file_extension_with_dot = "." + str(file_extension_without_dot)

        if file_extension_with_dot.lower() == ".all":
            filelist = [f for f in os.listdir(fullPathOfTheFolder)]
        else:
            filelist = [f for f in os.listdir(
                fullPathOfTheFolder) if f.endswith(file_extension_with_dot)]

        for f in filelist:
            file_path = os.path.join(fullPathOfTheFolder, f)
            file_path = Path(file_path)
            os.remove(file_path)
            count += 1

        if print_status:
            print(filelist)
        # data = count

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

# write a function to delete file or folder


def folder_delete_file_or_folder(file_or_folder_path: str = "", print_status=False):
    # Description:
    """
    Description:
        Deletes single file or entire folder with all its contents.

    Args:
        file_or_folder_path  (str) : Location of the file or folder.
    Returns:
        [status]
        status (bool) - True if the file is deleted successfully.
    """

    # import section
    import os
    from pathlib import Path
    # Response section
    error = None
    status = False
    # data = None

    try:
        if not file_or_folder_path:
            raise Exception("File or folder path is empty")

        file_or_folder_path = Path(file_or_folder_path)

        # check if the file or folder exists
        if file_or_folder_path.exists():

            # check if path is a file
            if file_or_folder_path.is_file():
                os.remove(file_or_folder_path)
            elif file_or_folder_path.is_dir():
                import os
                import shutil
                shutil.rmtree(file_or_folder_path)

            if print_status:
                print("File or folder deleted successfully")
        else:
            raise Exception("File or folder does not exist")
        # data = count

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

# if __name__ == "__main__":
#     folder_delete_file_or_folder(r"C:\Users\mrmay\OneDrive\Desktop\Del Me")


def file_rename(old_file_path='', new_file_name='', print_status=False):
    # Description:
    """
    Description:
        Renames the given file name to new file name with same extension

    Args:
        old_file_path (str) : Location of the file.
        new_file_name (str) : New file name.
        print_status (bool) : True if the status is to be printed.
    Returns:
        [status, data]
        status (bool) - True if the file is renamed successfully.
        data (List) - list of all the contents of the text file.
    """

    # import section
    import os
    from pathlib import Path
    # Response section
    error = None
    status = False
    data = None

    try:
        if not old_file_path:
            raise Exception("Old file path is empty")

        if not new_file_name:
            raise Exception("New file name is empty")

        if os.path.exists(old_file_path):
            if new_file_name:
                ext = old_file_path.split('\\')[-1].split('.')[-1]
                path_of_new_file = os.path.join('\\'.join(old_file_path.split('\\')[
                                                :-1]), '.'.join([new_file_name, ext]))

                os.rename(src=Path(old_file_path),
                          dst=Path(path_of_new_file))
                if print_status:
                    print("File renamed successfully")
                    print(path_of_new_file)
            else:
                raise Exception('new_file_name can\'t be empty.')
        else:
            raise Exception(
                'Old_file_path is invalid. Please pass a valid path.')

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


def file_get_json_details(path_of_json_file='', section=''):
    # Description:
    """
    Description:
        Returns all the details of the given section in a dictionary

    Args:
        path_of_json_file (str) : Location of the json file.
        section (str) : section of the json file.

    Returns:
        [status, data]
        status (bool) - True if the file is renamed successfully.
        data - The contents of the JSON file.

    """

    # import section
    import json
    # Response section
    error = None
    status = False
    data = None

    try:
        if not path_of_json_file:
            raise Exception("Path of json file is empty")

        if not section:
            raise Exception("Section is empty")

        # import json

        with open(path_of_json_file, 'r') as fp:
            data = json.load(fp)
        fp.close()

        if section in list(data.keys()):
            data = data.get(section)
        else:
            raise Exception(
                'Section can\'t be find in given json file.')

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
