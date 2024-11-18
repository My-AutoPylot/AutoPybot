from playwright.sync_api import sync_playwright
import time

def launch(playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    
    return browser.new_context()

def navigate_to_url(page, url):
    page.goto(url)
    return browser

#mouse click
def mouse_click(page):
    page.mouse.click(100, 100)

#click specific link
def click_link(page, text = ""):
    page.click("text=" + text)

def new_page(browser):
    page = browser.new_page()
    return page

def close_browser(browser):
    browser.close()

def close_page(page):
    page.close()

#bring front tab
def bring_front(page):
    page.bring_to_front()

#hit enter
def hit_enter(page):
    page.keyboard.press("Enter")

#hit tab
def hit_tab(page):
    page.keyboard.press("Tab")

#hit combination keys
def hit_keys(page, keys):
    page.keyboard.press(keys)

#set_download_path
def set_download_path(page, path):
    page.context.set_downloads_path(path)

def screenshot(page, path):
    page.screenshot(path=path)

def get_text(page):
    return page.inner_text()

def get_title(page):
    return page.title()

def get_url(page):
    return page.url()

def get_html(page):
    return page.inner_html()

def get_content(page):
    return page.content()

def get_cookies(page):
    return page.context.cookies()

#save authenication
def save_auth(page, username, password):
    page.context.add_init_script(f"""
        const auth = {{username: '{username}', password: '{password}'}}
        window.localStorage.setItem('auth', JSON.stringify(auth))
    """)
    page.reload()

with sync_playwright() as playwright:
    browser = launch(playwright)

    page_1 = new_page(browser)
    navigate_to_url(page_1, "http://pybots.ai")

    time.sleep(3)

    page_2 = new_page(browser)
    navigate_to_url(page_2, "http://google.com")

    time.sleep(5)

    bring_front(page_1)

    time.sleep(3)

    click_link(page_1, "FAQ")

    mouse_click(page_1)