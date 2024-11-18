from my_autopybot.helpers import _is_ec2_instance
import logging
from my_autopybot.CrashHandler import report_error, text_to_speech_error
from selenium.common.exceptions import TimeoutException
import os

output_folder_path = os.path.join(
    os.path.abspath(r'C:\Users\Public\PyBots'), 'My-autopybot', 'Converters Folder')

if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)


is_aws = _is_ec2_instance()


class DisableLogger():

    def __enter__(self):
        logging.disable(logging.CRITICAL)

    def __exit__(self, exit_type, exit_value, exit_traceback):
        logging.disable(logging.NOTSET)


class ChromeBrowser:
    def __init__(self):
        self.browser_driver = None

    def open_browser(self, dummy_browser: bool = True, profile: str = "Default", incognito: bool = False, ):
        """
        Description:
            This function opens a browser.
        Args:
            dummy_browser (bool, optional): True to open dummy browser. 
            Defaults: True.
            profile (str, optional): Profile name to open. 
            Defaults: "Default".
            incognito (bool, optional): True to open incognito browser. 
            Defaults: False.
        Returns:
            [status, browser_driver]
            status (bool): Whether the function is successful or failed.
            browser_driver (object): The browser driver object.
        """

        import selenium.webdriver as webdriver
        from webdriver_manager.chrome import ChromeDriverManager
        import os
        from selenium.webdriver.chrome.options import Options
        import helium

        self.options = Options()

        self.options.add_argument("--start-maximized")
        self.options.add_experimental_option(
            'excludeSwitches', ['enable-logging', 'enable-automation'])

        status = False
        error = None

        try:
            with DisableLogger():
                if not dummy_browser:
                    self.options.add_argument(
                        "user-data-dir=C:\\Users\\{}\\AppData\\Local\\Google\\Chrome\\User Data".format(os.getlogin()))
                    self.options.add_argument(
                        f"profile-directory={profile}")

                if is_aws:
                    self.browser_driver = webdriver.Chrome(
                        executable_path=ChromeDriverManager().install(), options=self.options, port=8080)
                else:
                    if incognito:
                        self.options.add_argument("--incognito")
                    self.browser_driver = webdriver.Chrome(
                        ChromeDriverManager().install(), options=self.options)

                helium.set_driver(self.browser_driver)
                helium.Config.implicit_wait_secs = 60
                status = True
        except Exception as ex:
            status = False
            # print(f"Error while creating browser driver: {e}")
            error = ex
            report_error(ex)
        finally:
            if error is not None:
                raise Exception(error)
            return [status, self.browser_driver]

    def navigate(self, url: str = ''):
        """
        Description:
            Navigate through the url after the session is started.
        Args:
            url (str, optional): Url which you want to visit. 
            Defaults: "".
        Returns:
            [status]
            status (bool): Whether the function is successful or failed.
        """

        status = False
        error = None
        import helium
        helium.set_driver(self.browser_driver)
        try:
            if not url:
                helium.go_to("https://www.pybots.ai")
            else:
                helium.go_to(url)
        except Exception as ex:
            status = False
            error = ex
            report_error(ex)
            # print("Error while navigating to url")

        else:
            status = True
        finally:
            if error is not None:
                raise Exception(error)
            return [status]

    def write(self, text: str = '', user_visible_text_element: str = ""):
        """
        Description:
            Write a string in browser, if user_visible_text_element is given it writes on the given element.

        Args:
            text (str, optional): String which has be written. 
            Defaults: "".
            user_visible_text_element (str, optional): The element which is visible(Like : Sign in). 
            Defaults: "".

        Returns:
            [status]
            status (bool): Whether the function is successful or failed.
        """

        status = False
        error = None
        import helium
        import time
        from selenium.common.exceptions import WebDriverException
        # import sys
        helium.set_driver(self.browser_driver)
        try:

            if text and str(user_visible_text_element).strip():
                if self.check_if(user_visible_text_element, "t")[0]:
                    helium.write(text, into=user_visible_text_element)
                    status = True
                else:
                    status = False

            if text and not str(user_visible_text_element).strip():
                helium.write(text)
                status = True

        except TimeoutException:
            print(
                "Element not found. Please check the given input or change browser_set_waiting_time().")
            # sys.exit()
        except WebDriverException as e:
            message = str(e)
            if "loading status" in message:
                time.sleep(2)
                self.write(text, user_visible_text_element)
        except AttributeError:
            print("Invalid Input given for function browser write")
        except Exception as ex:
            status = False
            report_error(ex)
            error = ex
        finally:
            if error is not None:
                raise Exception(error)
            return [status]

    def set_download_path(self, path: str = ""):
        """Set the download path for the browser.
        Args:
            path (str, optional): The path to set. Defaults: "".
        Returns:
            bool: Whether the function is successful or failed.
        """
        status = False
        error = None
        try:
            self.browser_driver.command_executor._commands["send_command"] = (
                "POST", '/session/$sessionId/chromium/send_command')
            params = {'cmd': 'Page.setDownloadBehavior', 'params': {
                'behavior': 'allow', 'downloadPath': path}}
            self.browser_driver.execute("send_command", params)
            status = True
        except Exception as ex:
            # print("Error while setting download path")
            status = False
            error = ex
            report_error(ex)

        finally:
            if error is not None:
                raise Exception(error)
            return [status]

    def mouse(self, value: str = "", action_type: str = "single", value_type: str = "text"):
        """
        Description: 
            Performs a Mouse Click on the given value.

        Args:
            value (str, optional): The value which has to be clicked.
            Defaults: "".
            action_type (str, optional): The type of click.
            Defaults: "single".
            value_type (str, optional): The type of value.
            Defaults: "text".

        Returns:
            [status]
            status (bool): Whether the function is successful or failed.
        """
        import helium
        import sys
        from selenium.common.exceptions import WebDriverException
        import time
        status = False
        error = None
        helium.set_driver(self.browser_driver)

        try:
            if not action_type:
                text_to_speech_error("Please provide click type", show=False)
            if not value:
                text_to_speech_error("Please provide value", show=False)
            if not value_type:
                text_to_speech_error("Please provide type", show=False)

            possible_value_types = ["text", "button", "link", "checkbox",
                                    "radio", "image", "xpath"]
            possible_clicks = ["single", "double", "right", "hover"]

            if not value_type in possible_value_types:
                text_to_speech_error(
                    "Value type is invalid for function mouse.", show=False)
            if not action_type in possible_clicks:
                text_to_speech_error(
                    "Click type is invalid for function mouse.", show=False)
            if value_type == "xpath":
                if action_type == "single":
                    self.browser_driver.find_element_by_xpath(
                        value).click()
                    status = True
                elif action_type == "double":
                    _element = self.browser_driver.find_element_by_xpath(
                        value)
                    helium.doubleclick(_element)
                    status = True
                elif action_type == "right":
                    _element = self.browser_driver.find_element_by_xpath(
                        value)
                    helium.rightclick(_element)
                    status = True
                elif action_type == "hover":
                    _element = self.browser_driver.find_element_by_xpath(
                        value)
                    helium.hover(_element)
                    status = True
                else:
                    status = False

            if value_type == "text":
                if action_type == "single":
                    helium.click(value)
                    status = True
                elif action_type == "double":
                    helium.doubleclick(value)
                    status = True
                elif action_type == "right":
                    helium.rightclick(value)
                    status = True
                elif action_type == "hover":
                    helium.hover(value)
                    status = True
            elif value_type == "button":
                if action_type == "single":
                    helium.click(helium.Button(value))
                    status = True
                elif action_type == "double":
                    helium.doubleclick(helium.Button(value))
                    status = True
                elif action_type == "right":
                    helium.rightclick(helium.Button(value))
                    status = True
                elif action_type == "hover":
                    helium.hover(helium.Button(value))
                    status = True
            elif value_type == "link":
                if action_type == "single":
                    helium.click(helium.Link(value))
                    status = True
                elif action_type == "double":
                    helium.doubleclick(helium.Link(value))
                    status = True
                elif action_type == "right":
                    helium.rightclick(helium.Link(value))
                    status = True
                elif action_type == "hover":
                    helium.hover(helium.Link(value))
                    status = True
            elif value_type == "checkbox":
                if action_type == "single":
                    helium.click(helium.Checkbox(value))
                    status = True
                elif action_type == "double":
                    helium.doubleclick(helium.Checkbox(value))
                    status = True
                elif action_type == "right":
                    helium.rightclick(helium.Checkbox(value))
                    status = True
                elif action_type == "hover":
                    helium.hover(helium.Checkbox(value))
                    status = True
            elif value_type == "radio":
                if action_type == "single":
                    helium.click(helium.Radio(value))
                    status = True
                elif action_type == "double":
                    helium.doubleclick(helium.Radio(value))
                    status = True
                elif action_type == "right":
                    helium.rightclick(helium.Radio(value))
                    status = True
                elif action_type == "hover":
                    helium.hover(helium.RadioButton(value))
                    status = True
            elif value_type == "image":
                if action_type == "single":
                    helium.click(helium.Image(value))
                    status = True
                elif action_type == "double":
                    helium.doubleclick(helium.Image(value))
                    status = True
                elif action_type == "right":
                    helium.rightclick(helium.Image(value))
                    status = True
                elif action_type == "hover":
                    helium.hover(helium.Image(value))
                    status = True
            else:
                status = False

        except WebDriverException as e:
            message = str(e)
            if "loading status" in message:
                time.sleep(2)
                self.mouse(value, action_type, value_type)

        except AttributeError:
            text_to_speech_error(
                "Invalid Input for function mouse. Please check the value type and action type.", show=False)
            # sys.exit()
        except Exception as ex:
            status = False
            report_error(ex)
            error = ex

        finally:
            if error is not None:
                raise Exception(error)
            return [status]

    def mouse_v2(self, value: str = "", action_type: str = "single", value_type: str = "t"):
        """
        Description: 
            Performs a Mouse Click on the given value.

        Args:
            value (str, optional): The value which has to be clicked.
            Defaults: "".
            action_type (str, optional): The type of click.
            Defaults: "single".
            value_type (str, optional): The type of value.
            Defaults: "text".

        Returns:
            [status]
            status (bool): Whether the function is successful or failed.
        """
        import helium
        import sys
        from selenium.common.exceptions import WebDriverException
        import time
        status = False
        error = None
        helium.set_driver(self.browser_driver)

        try:
            if not action_type:
                text_to_speech_error("Please provide click type", show=False)
            if not value:
                text_to_speech_error("Please provide value", show=False)
            if not value_type:
                text_to_speech_error("Please provide type", show=False)

            possible_value_types = ["t", "b", "l", "cb",
                                    "rb", "i", "xp", "li"]
            possible_clicks = ["single", "double", "right", "hover"]

            if not value_type in possible_value_types:
                text_to_speech_error(
                    "Value type is invalid for function mouse.", show=False)
            if not action_type in possible_clicks:
                text_to_speech_error(
                    "Click type is invalid for function mouse", show=False)

            if value_type == "xp":
                if action_type == "single":
                    self.browser_driver.find_element_by_xpath(
                        value).click()
                    status = True
                elif action_type == "double":
                    _element = self.browser_driver.find_element_by_xpath(
                        value)
                    helium.doubleclick(_element)
                    status = True
                elif action_type == "right":
                    _element = self.browser_driver.find_element_by_xpath(
                        value)
                    helium.rightclick(_element)
                    status = True
                elif action_type == "hover":
                    _element = self.browser_driver.find_element_by_xpath(
                        value)
                    helium.hover(_element)
                    status = True
            else:
                if self.check_if(value, value_type)[0]:
                    if value_type == "t":
                        if action_type == "single":
                            helium.click(value)
                            status = True
                        elif action_type == "double":
                            helium.doubleclick(value)
                            status = True
                        elif action_type == "right":
                            helium.rightclick(value)
                            status = True
                        elif action_type == "hover":
                            helium.hover(value)
                            status = True
                    elif value_type == "l":
                        if action_type == "single":
                            helium.click(helium.Link(value))
                            status = True
                        elif action_type == "double":
                            helium.doubleclick(helium.Link(value))
                            status = True
                        elif action_type == "right":
                            helium.rightclick(helium.Link(value))
                            status = True
                        elif action_type == "hover":
                            helium.hover(helium.Link(value))
                            status = True
                    elif value_type == "li":
                        if action_type == "single":
                            helium.click(helium.ListItem(value))
                            status = True
                        elif action_type == "double":
                            helium.doubleclick(helium.ListItem(value))
                            status = True
                        elif action_type == "right":
                            helium.rightclick(helium.ListItem(value))
                            status = True
                        elif action_type == "hover":
                            helium.hover(helium.ListItem(value))
                            status = True
                    elif value_type == "b":
                        if action_type == "single":
                            helium.click(helium.Button(value))
                            status = True
                        elif action_type == "double":
                            helium.doubleclick(helium.Button(value))
                            status = True
                        elif action_type == "right":
                            helium.rightclick(helium.Button(value))
                            status = True
                        elif action_type == "hover":
                            helium.hover(helium.Button(value))
                            status = True
                    elif value_type == "i":
                        if action_type == "single":
                            helium.click(helium.Image(value))
                            status = True
                        elif action_type == "double":
                            helium.doubleclick(helium.Image(value))
                            status = True
                        elif action_type == "right":
                            helium.rightclick(helium.Image(value))
                            status = True
                        elif action_type == "hover":
                            helium.hover(helium.Image(value))
                            status = True
                    elif value_type == "tf":
                        if action_type == "single":
                            helium.click(helium.TextField(value))
                            status = True
                        elif action_type == "double":
                            helium.doubleclick(helium.TextField(value))
                            status = True
                        elif action_type == "right":
                            helium.rightclick(helium.TextField(value))
                            status = True
                        elif action_type == "hover":
                            helium.hover(helium.TextField(value))
                            status = True
                    elif value_type == "cob":
                        if action_type == "single":
                            helium.click(helium.ComboBox(value))
                            status = True
                        elif action_type == "double":
                            helium.doubleclick(helium.ComboBox(value))
                            status = True
                        elif action_type == "right":
                            helium.rightclick(helium.ComboBox(value))
                            status = True
                        elif action_type == "hover":
                            helium.hover(helium.ComboBox(value))
                            status = True
                    elif value_type == "chb":
                        if action_type == "single":
                            helium.click(helium.Checkbox(value))
                            status = True
                        elif action_type == "double":
                            helium.doubleclick(helium.Checkbox(value))
                            status = True
                        elif action_type == "right":
                            helium.rightclick(helium.Checkbox(value))
                            status = True
                        elif action_type == "hover":
                            helium.hover(helium.Checkbox(value))
                            status = True
                    elif value_type == "rb":
                        if action_type == "single":
                            helium.click(helium.RadioButton(value))
                            status = True
                        elif action_type == "double":
                            helium.doubleclick(helium.RadioButton(value))
                            status = True
                        elif action_type == "right":
                            helium.rightclick(helium.RadioButton(value))
                            status = True
                        elif action_type == "hover":
                            helium.hover(helium.RadioButton(value))
                            status = True
                    else:
                        status = False
                else:
                    status = False
        except WebDriverException as e:
            message = str(e)
            if "loading status" in message:
                time.sleep(2)
                self.mouse(value, action_type, value_type)

        except AttributeError:
            text_to_speech_error(
                "Invalid Input for function Mouse Click")
            # sys.exit()
        except Exception as ex:
            status = False
            report_error(ex)
            error = ex
        finally:
            if error is not None:
                raise Exception(error)
            return [status]

    def scroll(self, direction: str = "down", weight=3):
        """
        Description:
            Scrolls the browser window.

        Args:
            direction (str, optional): The direction to scroll. Defaults: "down".u,d,l,r
            weight  : The weight of the scroll. Defaults: 3. 3 corresponds to 300 pixs

        Returns:
            [status]
            status (bool): Whether the function is successful or failed.
        """
        status = False
        error = None
        import helium
        helium.set_driver(self.browser_driver)
        scroll_pixs = int(weight)
        try:
            if direction.lower() == "down":
                helium.scroll_down(scroll_pixs)
            elif direction.lower() == "up":
                helium.scroll_up(scroll_pixs)
            elif direction.lower() == "left":
                helium.scroll_left(scroll_pixs)
            elif direction.lower() == "right":
                helium.scroll_right(scroll_pixs)

            status = True
        except Exception as ex:
            status = False
            report_error(ex)
            error = ex
        finally:
            if error is not None:
                raise Exception(error)
            return [status]

    def key_press(self, key_1: str = "", key_2: str = ""):
        """
        Description:
            Type text using Browser Helium Functions and press hot keys.

        Args:
            key_1 (str): Keys you want to simulate or string you want to press 
            Eg: "tab" or "Murali". Defaults: ""
            key_2 (str, optional): Key you want to simulate with combination to key_1. 
            Eg: "shift" or "escape". Defaults: ""

        Returns:
            [status]
            status (bool): Whether the function is successful or failed.
        """
        status = False
        error = None

        import sys
        import helium
        helium.set_driver(self.browser_driver)

        try:

            if not key_1:
                text_to_speech_error("Please select the text to type")

            if key_1 and not key_2:
                helium.press(key_1)
            elif key_1 and key_2:
                helium.press(key_1 + key_2)

            status = True
        except TimeoutException:
            print(
                "Element not found. Please check the given input or change browser_set_waiting_time().")

        except AttributeError:
            print("Invalid Input for function Key Press")

            # sys.exit()
        except Exception as ex:
            status = False
            report_error(ex)
            error = ex
        finally:
            if error is not None:
                raise Exception(error)
            return [status]

    def hit_enter(self):
        """
        Description:
            Hits enter KEY in Browser

        Args:
            None

        Returns:
            [status]
            status (bool): Whether the function is successful or failed.
        """
        status = False
        error = None
        import helium
        helium.set_driver(self.browser_driver)
        try:
            helium.press(helium.ENTER)
            status = True
        except Exception as ex:
            status = False
            report_error(ex)
            error = ex
        finally:
            if error is not None:
                raise Exception(error)
            return [status]

    def wait_until(self, text: str = "", element: str = "t", delay=10):
        """
        Description:
            Wait until a specific element is found.

        Args:
            text (str, optional): To wait until the string appears on the screen. 
            Eg: Export Successful Completed. Defaults: ""
            element (str, optional): Type of Element Whether its a Text(t) or Button(b). 
            Defaults: "t - Text".

        Returns:
            [status]
            status (bool): Whether the function is successful or failed.
        """
        import helium
        import sys
        helium.set_driver(self.browser_driver)
        status = False
        error = None
        try:

            if element.lower() == "t":
                helium.wait_until(helium.Text(text).exists,
                                  timeout_secs=delay)  # text

            elif element.lower() == "b":
                helium.wait_until(helium.Button(text).exists,
                                  timeout_secs=delay)  # button

            elif element.lower() == "l":
                helium.wait_until(helium.Link(text).exists,
                                  timeout_secs=delay)  # Link

            elif element.lower() == "i":
                helium.wait_until(helium.Image(text).exists,
                                  timeout_secs=delay)  # Image

            elif element.lower() == "li":
                helium.wait_until(helium.ListItem(text).exists,
                                  timeout_secs=delay)  # ListItem

            status = True
        except TimeoutException:
            # print(
            #     "Element not found. Please check the given input or change browser_set_waiting_time().")

            sys.exit()
            status = False
        except Exception as ex:
            status = False
            report_error(ex)
            error = ex
        finally:
            if error is not None:
                raise Exception(error)
            return [status]

    def check_if(self, text: str = "", element: str = "t"):
        """
        Description:
            Check if a specific element is found.

        Args:
            text (str, optional): To wait until the string appears on the screen. 
            Eg: Export Successful Completed. Defaults: ""
            element (str, optional): Type of Element Whether its a Text(t) or Button(b). 
            Defaults: "t - Text".

        Returns:
            [status]
            status (bool): Whether the function is successful or failed.
        """
        import helium
        helium.set_driver(self.browser_driver)
        status = False
        error = None
        try:
            if element.lower() == "t":
                status = helium.Text(text).exists()
            elif element.lower() == "l":
                status = helium.Link(text).exists()
            elif element.lower() == "li":
                status = helium.ListItem(text).exists()
            elif element.lower() == "b":
                status = helium.Button(text).exists()
            elif element.lower() == "i":
                status = helium.Image(text).exists()
            elif element.lower() == "tf":
                status = helium.TextField(text).exists()
            elif element.lower() == "cob":
                status = helium.ComboBox(text).exists()
            elif element.lower() == "chb":
                status = helium.CheckBox(text).exists()
            elif element.lower() == "rb":
                status = helium.RadioButton(text).exists()
            else:
                text_to_speech_error(
                    "Invalid Input for function checking if element is present.")
        except TimeoutException:
            pass
            # print(
            #     "Element not found. Please check the given input or change browser_set_waiting_time().")
        except Exception as ex:
            status = False
            report_error(ex)
            error = ex
        finally:
            if error is not None:
                raise Exception(error)
            return [status]

    def refresh_page(self):
        """
        Description:
            Refresh the current active browser page.

        Args:
            None

        Returns:
            [status]
            status (bool): Whether the function is successful or failed.
        """
        status = False
        error = None
        try:
            self.browser_driver.refresh()
            status = True
        except Exception as ex:
            status = False
            report_error(ex)
            error = ex

        finally:
            if error is not None:
                raise Exception(error)
            return [status]

    def set_waiting_time(self, time: int = 10):
        """
        Description:
            Set the waiting time for the self.browser_driver. If element is not found in the given time, it will raise an exception.

        Args:
            time ([int]): The time in seconds to wait for the element to be found. Defaults: 10

        Returns:
            [status]
            status (bool): Whether the function is successful or failed.
        """
        status = False
        error = None
        try:
            import helium
            helium.set_driver(self.browser_driver)
            helium.Config.implicit_wait_secs = int(time)
            status = True
        except Exception as ex:
            status = False
            report_error(ex)
            error = ex
        finally:
            if error is not None:
                raise Exception(error)
            return [status]

    def get_text(self, element_xpath: str = ""):
        """
        Description:
            Get the text of the element.

        Args:
            element_xpath (str, optional): The xpath of the element. Defaults: ""

        Returns:
            [status, data]
            status (bool): Whether the function is successful or failed.
            data (str): The text of the element.
        """
        status = False
        data = None
        error = None
        try:
            element = self.browser_driver.find_element_by_xpath(element_xpath)
            status = True
            data = element.text
        except Exception as ex:
            status = False
            report_error(ex)
            error = ex
        finally:
            if error is not None:
                raise Exception(error)
            return [status, data]

    def get_element_image(self, element_xpath: str = "", base64_image: bool = True, image_name: str = ""):
        """Get the image of the element.
        Args:
            element_xpath (str, optional): The xpath of the element. Defaults: ""
        Returns:
            bool: Whether the function is successful or failed.
            str: The image of the element.
        """

        # Imports
        from os.path import abspath
        import os
        status = False
        data = None
        error = None
        try:
            element = self.browser_driver.find_element_by_xpath(element_xpath)
            if base64_image:
                data = element.screenshot_as_base64
            else:
                if image_name == "":
                    image_name = f"Element-{str(element.id)}.png"
                    image_path = os.path.join(output_folder_path, image_name)
                else:
                    # check if the image name is a path
                    if os.path.isdir(image_name):
                        image_path = os.path.join(
                            image_name, f"Element-{str(element.id)}.png")
                    elif os.path.isfile(image_name):
                        image_path = os.path.abspath(image_name)
                    elif os.path.isdir(os.path.dirname(image_name)):
                        # check whether is has a extension
                        img_extension = os.path.splitext(image_name)[1]
                        img_dir = os.path.dirname(image_name)
                        img_name = os.path.basename(image_name).split('.')[0]
                        if img_extension == "":
                            image_path = os.path.join(
                                img_dir, f"{str(img_name)}.png")
                        else:
                            img_extension = ".png"

                            image_path = os.path.join(
                                img_dir, f"{str(img_name)}{img_extension}")
                    else:
                        img_name = os.path.basename(image_name).split('.')[0]
                        image_path = os.path.join(
                            output_folder_path, f"{str(img_name)}.png")

                try:
                    element.screenshot(image_path)
                except UserWarning:
                    pass
                else:
                    status = True
                    data = abspath(image_path)
        except Exception as ex:
            status = False
            report_error(ex)
            error = ex
        finally:
            if error is not None:
                raise Exception(error)
            return [status, data]

    def close(self):
        """
        Description:
            Close the current active browser.

        Args:
            None

        Returns:
            [status]    
            status (bool): Whether the function is successful or failed.
        """
        status = False
        error = None
        try:
            self.browser_driver.close()
            self.browser_driver.quit()
            status = True
        except Exception as ex:
            status = False
            report_error(ex)
            error = ex
        finally:
            if error is not None:
                raise Exception(error)
            return [status]

    def __str__(self):
        return f"Chrome Browser with options: {self.options}"

    # Finding browser elements relative to others
    def get_value_relatively(self, element_type="Text", above="", below="", to_left_of="", to_right_of=""):
        #Link, Image, Button, TextField, CheckBox,
        """
        Description:
            Text Element : Get the value of the element
            Link Element : Get the text of the element
            Button Element : Performs single left click on the element

        Args:
            element_type (str, optional): The type of the element. Defaults: "Text".
            above (str, optional): The xpath of the element above. Defaults: "".
            below (str, optional): The xpath of the element below. Defaults: "".
            to_left_of (str, optional): The xpath of the element to the left of. Defaults: "".
            to_right_of (str, optional): The xpath of the element to the right of. Defaults: "".

        Returns:
            [status, data]
            status (bool): Whether the function is successful or failed.
            data (str): The value of the element.

        """

        status = False
        data = ""
        import helium

        status = False
        data = None

        try:
            if element_type == "Text":
                if above != "" and below != "" and to_left_of != "" and to_right_of != "":
                    data = helium.Text(
                        above=above, below=below, to_left_of=to_left_of, to_right_of=to_right_of).value

                elif above != "" and below != "" and to_left_of != "" and to_right_of == "":
                    data = helium.Text(
                        above=above, below=below, to_left_of=to_left_of).value

                elif above != "" and below != "" and to_left_of == "" and to_right_of != "":
                    data = helium.Text(
                        above=above, below=below, to_right_of=to_right_of).value

                elif above != "" and below != "" and to_left_of == "" and to_right_of == "":
                    data = helium.Text(above=above, below=below).value

                elif above != "" and below == "" and to_left_of != "" and to_right_of != "":
                    data = helium.Text(
                        above=above, to_left_of=to_left_of, to_right_of=to_right_of).value

                elif above != "" and below == "" and to_left_of != "" and to_right_of == "":
                    data = helium.Text(
                        above=above, to_left_of=to_left_of).value

                elif above != "" and below == "" and to_left_of == "" and to_right_of != "":
                    data = helium.Text(
                        above=above, to_right_of=to_right_of).value

                elif above != "" and below == "" and to_left_of == "" and to_right_of == "":
                    data = helium.Text(above=above).value

                elif above == "" and below != "" and to_left_of != "" and to_right_of != "":
                    data = helium.Text(
                        below=below, to_left_of=to_left_of, to_right_of=to_right_of).value

                elif above == "" and below != "" and to_left_of != "" and to_right_of == "":
                    data = helium.Text(
                        below=below, to_left_of=to_left_of).value

                elif above == "" and below != "" and to_left_of == "" and to_right_of != "":
                    data = helium.Text(
                        below=below, to_right_of=to_right_of).value

                elif above == "" and below != "" and to_left_of == "" and to_right_of == "":
                    data = helium.Text(below=below).value

                elif above == "" and below == "" and to_left_of != "" and to_right_of != "":
                    data = helium.Text(to_left_of=to_left_of,
                                       to_right_of=to_right_of).value

                elif above == "" and below == "" and to_left_of != "" and to_right_of == "":
                    data = helium.Text(to_left_of=to_left_of).value

                elif above == "" and below == "" and to_left_of == "" and to_right_of != "":
                    data = helium.Text(to_right_of=to_right_of).value

            elif element_type == "Button":
                if above != "" and below != "" and to_left_of != "" and to_right_of != "":
                    data = helium.click(helium.Button(
                        above=above, below=below, to_left_of=to_left_of, to_right_of=to_right_of))

                elif above != "" and below != "" and to_left_of != "" and to_right_of == "":
                    data = helium.click(helium.Button(
                        above=above, below=below, to_left_of=to_left_of))

                elif above != "" and below != "" and to_left_of == "" and to_right_of != "":
                    data = helium.click(helium.Button(
                        above=above, below=below, to_right_of=to_right_of))

                elif above != "" and below != "" and to_left_of == "" and to_right_of == "":
                    data = helium.click(
                        helium.Button(above=above, below=below))

                elif above != "" and below == "" and to_left_of != "" and to_right_of != "":
                    data = helium.click(helium.Button(
                        above=above, to_left_of=to_left_of, to_right_of=to_right_of))

                elif above != "" and below == "" and to_left_of != "" and to_right_of == "":
                    data = helium.click(helium.Button(
                        above=above, to_left_of=to_left_of))

                elif above != "" and below == "" and to_left_of == "" and to_right_of != "":
                    data = helium.click(helium.Button(
                        above=above, to_right_of=to_right_of))

                elif above != "" and below == "" and to_left_of == "" and to_right_of == "":
                    data = helium.click(helium.Button(above=above))

                elif above == "" and below != "" and to_left_of != "" and to_right_of != "":
                    data = helium.click(helium.Button(
                        below=below, to_left_of=to_left_of, to_right_of=to_right_of))

                elif above == "" and below != "" and to_left_of != "" and to_right_of == "":
                    data = helium.click(helium.Button(
                        below=below, to_left_of=to_left_of))

                elif above == "" and below != "" and to_left_of == "" and to_right_of != "":
                    data = helium.click(helium.Button(
                        below=below, to_right_of=to_right_of))

                elif above == "" and below != "" and to_left_of == "" and to_right_of == "":
                    data = helium.click(helium.Button(below=below))

                elif above == "" and below == "" and to_left_of != "" and to_right_of != "":
                    data = helium.click(helium.Button(
                        to_left_of=to_left_of, to_right_of=to_right_of))

                elif above == "" and below == "" and to_left_of != "" and to_right_of == "":
                    data = helium.click(helium.Button(to_left_of=to_left_of))

                elif above == "" and below == "" and to_left_of == "" and to_right_of != "":
                    data = helium.click(helium.Button(to_right_of=to_right_of))

            # print(data)

            status = True
        except Exception as e:
            report_error(e)
        finally:
            return [status, data]

# def main():
#     browser = ChromeBrowser()
#     browser.open_browser()
#     browser.navigate("https://www.google.com")

    # print(browser.get_value_relatively(element_type="Button", to_right_of="Google Search"))
    # print(browser.get_value_relatively(element_type="Text", to_left_of="Images"))
    # print(browser.get_value_relatively(element_type="Text", above="About"))
    # print(browser.get_value_relatively(element_type="Text", below="India"))

    # browser.close()

# main()
