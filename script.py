from ast import arg
import csv
import os
import random
import threading
import time
import traceback
import zipfile
from inspect import Traceback

from bs4 import BeautifulSoup
from cv2 import add
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--no-sandbox")
# options.add_argument("--start-maximized")
# options.add_argument('--start-fullscreen')
# options.add_argument("--single-process")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--incognito")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("disable-infobars")


class Click_Bot:
    wd = None
    proxyExtensionPath=None

    def __init__(
        self,
        use_proxy=False,
        user_agent=None,
        PROXY_HOST="usa.rotating.proxyrack.net",
        PROXY_PORT=1000,
        PROXY_USER="ashtonrooney",
        PROXY_PASS="2187bd-6a425c-b217d2-643c2f-a391d0",
    ) -> None:
        def getProxyExtensionName():
            i = 0
            proxyExtensionPath = f"./extensions/proxyExtension{i}.zip"
            while os.path.exists(proxyExtensionPath):
                i += 1
                proxyExtensionPath = f"./extensions/proxyExtension{i}.zip"
            return proxyExtensionPath

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (
            PROXY_HOST,
            PROXY_PORT,
            PROXY_USER,
            PROXY_PASS,
        )

        path = os.path.dirname(os.path.abspath(__file__))

        if use_proxy:
            self.use_proxy=True

            pluginfile = getProxyExtensionName()
            self.proxyExtensionPath = pluginfile

            with zipfile.ZipFile(pluginfile, "w") as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)

            options.add_extension(pluginfile)
        if user_agent:
            options.add_argument("--user-agent=%s" % user_agent)

        self.wd = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    def get_driver(self) -> webdriver:
        return self.wd

    def __del__(self):
        if  self.proxyExtensionPath:
            try:
                os.remove(self.proxyExtensionPath)
            except:
                pass

    def open_website(self, site):
        self.wd.get(site)
        self.wd.implicitly_wait(100)
        print('Site Opened')

    def click(self, path_to_button):
        print(self.wd.find_elements_by_xpath(path_to_button))

        if len(self.wd.find_elements_by_xpath(path_to_button)):

            print('Clicking!')
            try:
                self.wd.find_elements_by_xpath(path_to_button)[0].click()
            except:
                self.wd.execute_script(
                    "arguments[0].click();",
                    self.wd.find_elements_by_xpath(path_to_button)[0],
                )



if __name__ == "__main__":
    try:
        bot = Click_Bot(use_proxy=False)
        bot.open_website('https://www.facebook.com/')
        bot.click('//*[@name="login"]')

    except Exception as e:
        print(e)
        pass
