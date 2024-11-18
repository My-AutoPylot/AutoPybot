import os
from pathlib import WindowsPath
from typing import Dict, List, Union

output_folder_path = os.path.join(os.path.abspath(
    r'C:\Users\Public\PyBots'), 'My-autopybot', 'Excel Folder')

# create output folder if not present
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

#vba macro function
def run_custom_vba_macro_function(module_name : str, vba_macro_code : str) -> None:
    """
    Description: VBA macro function

    Parameters:
    module_name (str): Name of the module
    vba_macro_code (str): VBA macro code
    
    Returns:
    None

    Example:
    >>> run_custom_vba_macro_function("test", "Sub test() MsgBox \"Hello World\" End Sub")
    None
    
    """
    # Import section
    import win32com.client as win32

    # Code section
    xl = win32.gencache.EnsureDispatch('Excel.Application')
    xl.Visible = False
    ss = xl.Workbooks.Add()
    xlmodule = ss.VBProject.VBComponents.Add(1)
    xlmodule.Name = module_name
    xlmodule.CodeModule.AddFromString(vba_macro_code)

    #get macro name from vba macro code after sub and before ()
    macro_name = vba_macro_code.split(" ")[1]
    #remove ()
    macro_name = macro_name[:-2]
    
    ss.Application.Run(module_name + "." + macro_name)

code = """sub test_macro() 
msgbox "Hare Krishna" 
end sub """
# run_custom_vba_macro_function("my_module",code)

#vba macro function pass arguments and get return value

code = """sub add_numbers(a As Integer, b As Integer)
add_numbers = a + b
end sub"""
# print(run_custom_vba_macro_function_pass_arguments_and_get_return_value("my_module",code, (10, 20)))


def run_custom_vba_macro_function_pass_arguments_and_get_return_value(module_name : str, vba_macro_code : str, arguments : tuple) -> None:
    """
    Description: VBA macro function

    Parameters:
    module_name (str): Name of the module
    vba_macro_code (str): VBA macro code
    arguments (tuple): Arguments to be passed to the macro
    
    Returns:
    None

    Example:
    >>> run_custom_vba_macro_function_pass_arguments_and_get_return_value("test", "Sub test(a As Integer, b As Integer) MsgBox a + b End Sub", (10, 20))
    None
    
    """
    # Import section
    import win32com.client as win32

    # Code section
    xl = win32.gencache.EnsureDispatch('Excel.Application')
    xl.Visible = False
    ss = xl.Workbooks.Add()
    xlmodule = ss.VBProject.VBComponents.Add(1)
    xlmodule.Name = module_name
    xlmodule.CodeModule.AddFromString(vba_macro_code)

    #get macro name from vba macro code after sub and before ()
    macro_name = vba_macro_code.split(" ")[1]
    #remove ()
    macro_name = macro_name[:-2]
    print(macro_name)
    
    return ss.Application.Run(module_name + "." + macro_name, *arguments)

code = """Function add_numbers(a As Integer, b As Integer)
add_numbers=a + b
end Function"""


# print(run_custom_vba_macro_function_pass_arguments_and_get_return_value("my_module",code, (10, 20)))

from typing import Dict, List, Union
from pathlib import WindowsPath

# function to get the row and column count of an excel sheet using VBA
def excel_macro_get_all_sheets_as_list(user_excel_path : Union[str, WindowsPath], sheet_name : str = "") -> None:
    """
    Excel VBA Macros called from Myautopybot
    """
    try:
        print(1)
        import os
        import xlwings as xw
        import shutil
        from pathlib import Path
        import pygetwindow as gw
        excel_rountine_file_path = os.path.join(output_folder_path,"Excel_Routines.xlsm")
        print(2)
        print("excel_rountine_file_path=", excel_rountine_file_path)
        

        import win32com.client
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = True
        excel.DisplayAlerts = False
        
        user_excel_path_with_sr = str(user_excel_path).replace(".xlsx",".xlsm")
        
        #save excel file as xlsm
        wb = excel.Workbooks.Open(user_excel_path)
        wb.SaveAs(user_excel_path_with_sr, FileFormat = 52)
        wb.Close()
        excel.Quit()
        
        print("user_excel_path_with_sr=", user_excel_path_with_sr)
        
        #Delete if already present using shutil
        if os.path.exists(user_excel_path_with_sr):
            os.remove(user_excel_path_with_sr)
        
        shutil.copy2(excel_rountine_file_path,user_excel_path_with_sr)

        wb1 = xw.Book(user_excel_path)
        wb2 = xw.Book(user_excel_path_with_sr)

        ws1 = wb1.sheets(1)

        ws1.api.Copy(Before=wb2.sheets(1).api)
        try:
            wb2.save(user_excel_path_with_sr)
        except:
            pass

        wb1.close()
        wb2.close()

        try:
            wb1.app.quit()
            wb2.app.quit()
        except:
            pass

        excel.Workbooks.Open(Filename=user_excel_path_with_sr, ReadOnly=1)
        # file_name = str(Path(user_excel_path_with_sr).stem) + ".xlsx"
        
        # print("file_name=", file_name)

        #activate an excel sheet
        # excel.Worksheets(sheet_name).Activate()

        #Run the macro and get return value
        res= excel.Application.Run("'{}'!getAllSheetsAsList".format(user_excel_path_with_sr))
        print("res",res)

        excel.Workbooks.Close()
        excel.Application.Quit() 
        del excel

        # try:
        #     ew = gw.getWindowsWithTitle('Excel')[0]
        #     ew.close()
        # except:
        #     pass
        
    except Exception as ex:
        print("Error in excel_sub_routines="+str(ex))

# excel_macro_get_all_sheets_as_list(r"C:\Users\mrmay\OneDrive\Desktop\Excel Templates\Anil.xlsx")
    