import sqlite3
import os
from my_autopybot.CrashHandler import report_error

output_folder_path = os.path.join(os.path.abspath(
    r'C:\Users\Public\PyBots'), 'My-autopybot', 'Database Files')
# print(output_folder_path)

cursr = ""
connct = ""

# create output folder if not present
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

try:
    db_file_path = r'{}\my_autopybot_db.db'.format(str(output_folder_path))

    connct = sqlite3.connect(db_file_path, check_same_thread=False)
    cursr = connct.cursor()
except Exception as ex:
    report_error(ex)

# Create Table LOG
try:
    cursr.execute('''CREATE TABLE IF NOT EXISTS My_autopybot_LOG
         (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
         BOT_ID UUID NOT NULL,
         BOT_NAME           TEXT    NOT NULL,
         BOT_TIMESTAMP            TIMESTAMP NOT NULL DEFAULT(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')),
         BOT_STATUS  TEXT NOT NULL,
         DESCRIPTION TEXT NULL);''')
    connct.commit()
except sqlite3.OperationalError:
    pass
except Exception as ex:
    print(f"Exception: {ex}")

# Create Table Current_Status
try:
    cursr.execute('''CREATE TABLE IF NOT EXISTS My_autopybot_Current_Status
         (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
         BOT_ID UUID NOT NULL,
         BOT_NAME           TEXT    NOT NULL,
         BOT_TIMESTAMP            TIMESTAMP NOT NULL DEFAULT(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')),
         BOT_STATUS  TEXT NOT NULL,
         DESCRIPTION TEXT NULL);''')
    connct.commit()
except sqlite3.OperationalError:
    pass
except Exception as ex:
    print(f"Exception: {ex}")


def delete_log_database():
    try:
        cursr.execute("DELETE FROM My_autopybot_LOG")
        connct.commit()

        cursr.execute("DELETE FROM My_autopybot_Current_Status")
        connct.commit()
    except Exception as ex:
        report_error(ex)


def update_log_database(bot_name="", bot_status="", description="OK", bot_id=""):
    try:
        sql_query = "INSERT INTO My_autopybot_LOG (BOT_NAME,BOT_STATUS,DESCRIPTION,BOT_ID) VALUES ('" + \
            bot_name + "','" + bot_status + "'" + ",'" + \
            description + "', '" + bot_id + "')"
        cursr.execute(sql_query)
        connct.commit()
        # print("Data Inserted to My_autopybot_LOG")

        cursr.execute(
            "SELECT * FROM  My_autopybot_Current_Status where bot_id = '" + bot_id + "'")
        row = cursr.fetchone()
        if row is None:
            sql_query = "INSERT INTO My_autopybot_Current_Status (BOT_NAME,BOT_STATUS,DESCRIPTION,BOT_ID) VALUES ('" + \
                bot_name + "','" + bot_status + "'" + ",'" + \
                description + "', '" + bot_id + "')"
        else:
            sql_query = "UPDATE My_autopybot_Current_Status SET BOT_STATUS ='" + bot_status + \
                "', DESCRIPTION = '" + description + "', BOT_NAME = '" + \
                bot_name + "' WHERE BOT_ID = '" + bot_id + "'"

        cursr.execute(sql_query)
        # print(sql_query, "sql_query")
        connct.commit()
        # print("Data Updated to My_autopybot_Current_Status")
    except Exception as ex:
        report_error(ex)


def get_all_rows(table_name):
    try:
        cursr.execute("SELECT * FROM " + table_name)
        rows = cursr.fetchall()
        # loop through all the rows
        # print(rows)
        # for row in rows:
        #     print(row)
        return rows
    except Exception as ex:
        report_error(ex)


def drop_table(table_name):
    try:
        cursr.execute("DROP TABLE IF EXISTS " + table_name)
        connct.commit()
        # print("Table Dropped ", table_name)
    except Exception as ex:
        report_error(ex)


def status_report_started():
    # Import section
    import my_autopybot as ap

    # Logic section
    bot_id = ap.bot_id if ap.bot_id else "Unknown_ID"
    bot_name = ap.bot_name if ap.bot_name else "Unknown_Name"
    bot_status = "Started"
    description = f"Execution Started"
    update_log_database(bot_name, bot_status, description, bot_id)


def status_report_completed():
    # Import section
    import my_autopybot as ap

    # Logic section
    bot_id = ap.bot_id if ap.bot_id else "Unknown_ID"
    bot_name = ap.bot_name if ap.bot_name else "Unknown_Name"
    bot_status = "Completed"
    description = f"Execution Completed"
    update_log_database(bot_name, bot_status, description, bot_id)


def status_report_failed(ex: Exception):
    # Import section
    import my_autopybot as ap

    # Logic section
    bot_id = ap.bot_id if ap.bot_id else "Unknown_ID"
    bot_name = ap.bot_name if ap.bot_name else "Unknown_Name"
    bot_status = "Failed"
    exception_name = type(ex).__name__
    exception_message = str(ex)
    exception_line = str(ex.__traceback__.tb_lineno)
    description = f"Execution Failed\nError : {exception_name} - {exception_message}\nLine : {exception_line}"
    update_log_database(bot_name, bot_status, description, bot_id)
