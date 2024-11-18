
def send_gmail_using_app_password(gmail_username="", gmail_app_password="", to_email_id="", subject="", message="", attachment_path=""):
    """
    Description:
        Send email using Gmail from Desktop email application

    Args:
        gmail_username (str): [description]. Defaults to "".
        gmail_app_password (str): [description]. Defaults to "".
        to_email_id (str): [description]. Defaults to "".
        subject (str): [description]. Defaults to "".
        message (str): [description]. Defaults to "".
        attachment_path (optional): [description]. Defaults to "".

    Returns:
        [status]
        Status (bool): Whether the function is successful or failed.
    """

    # Import Section
    import os
    from my_autopybot.CrashHandler import report_error
    from pathlib import Path
    import yagmail

    # Response Section
    error = None
    status = False

    # Logic Section
    try:
        if not gmail_username:
            raise Exception("Gmail username cannot be empty")

        if not gmail_app_password:
            raise Exception("Gmail app password cannot be empty")

        if not to_email_id:
            raise Exception("To email id cannot be empty")

        if not subject:
            raise Exception("Subject cannot be empty")

        if not message:
            raise Exception("Message cannot be empty")

        yag = yagmail.SMTP(gmail_username, gmail_app_password)

        if attachment_path:
            yag.send(to_email_id, subject, message,
                     attachments=attachment_path)
        else:
            yag.send(to=to_email_id, subject=subject, contents=message)

        # Alternatively, with a simple one-liner:
        # yagmail.SMTP(gmail_username).send(to_email_id, subject, message)

    except Exception as ex:
        report_error(ex)
        error = ex

    else:
        status = True

    finally:
        if error is not None:
            raise Exception(error)
        return [status]


def email_send_via_desktop_outlook(to_email_id="", subject="", message="", attachment_path=""):
    """
    Description:
        Send email using Outlook from Desktop email application

    Args:
        to_email_id (str): [description]. Defaults to "".
        subject (str): [description]. Defaults to "".
        message (str): [description]. Defaults to "".
        attachment_path (str, optional): [description]. Defaults to "".
    Returns:
        [status]
        Status (bool): Whether the function is successful or failed.
    """
    # Import Section
    from my_autopybot.CrashHandler import report_error
    from pathlib import Path
    import win32com.client

    # Response Section
    error = None
    status = False

    # Logic Section
    try:
        if not to_email_id:
            raise Exception("To address cannot be empty")

        if not subject:
            raise Exception("Subject cannot be empty")

        if not message:
            raise Exception("HTML Body cannot be empty")

        outlook = win32com.client.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)

        if type(to_email_id) is list:
            for m in to_email_id:
                mail.Recipients.Add(m)
        else:
            mail.To = to_email_id

        mail.Subject = subject

        mail.HTMLBody = f"<body><html> {message} <br> </body></html>"

        if attachment_path:
            if isinstance(attachment_path, list):
                for p in attachment_path:
                    mail.Attachments.Add(p)
            else:
                mail.Attachments.Add(attachment_path)

        mail.Send()

    except Exception as ex:
        report_error(ex)
        error = ex

    else:
        status = True

    finally:
        if error is not None:
            raise Exception(error)
        return [status]


# send_gmail_using_app_password(gmail_username="admin@pybots.ai", gmail_app_password="wlfyprdcupvvofnd", to_email_id="mmv@pybots.ai", subject="Test Attachments",
#                               message="Test Body Message", attachment_path=[r"C:\Users\PyBots\Desktop\dummy.xlsx", r"C:\Users\PyBots\Desktop\Function Template For My-autopybot.py"])
