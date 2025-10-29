import time

import pytest
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait as Wait


class BasePage:
    def __init__(self, browser, url):
        self.browser = browser
        self.url = url
        self.actions = ActionChains(browser)

    def open(self):
        print(f"Переход на {self.url}")
        self.browser.get(self.url)

    def find_element(self, locator):
        return self.browser.find_element(*locator)

    def find_elements(self, locator):
        return self.browser.find_elements(*locator)

    def is_element_present(self, locator):
        try:
            self.browser.find_element(*locator)
        except NoSuchElementException:
            return False
        return True

    def is_not_element_present(self, locator, timeout=4):
        try:
            WebDriverWait(self.browser, timeout).until(ec.presence_of_element_located(locator))
        except TimeoutException:
            return True
        return False

    def is_element_enabled(self, locator):
        return self.browser.find_element(*locator).is_enabled()

    def is_element_selected(self, locator):
        return self.browser.find_element(*locator).is_selected()

    def wait_until_element_displayed(self, locator, timeout=20):
        return WebDriverWait(self.browser, timeout).until(
            ec.visibility_of_element_located(locator)
        )

    def wait_until_element_present(self, locator, timeout=4):
        return WebDriverWait(self.browser, timeout).until(
            ec.presence_of_element_located(locator)
        )

    def wait_until_element_is_clickable(self, locator, timeout=45):
        return WebDriverWait(self.browser, timeout).until(
            ec.element_to_be_clickable(locator)
        )

    # ждать когда исчезнет из DOM
    def wait_until_element_disappear(self, locator, timeout=4):
        try:
            WebDriverWait(self.browser, 4).until(ec.presence_of_element_located(locator))
            WebDriverWait(self.browser, timeout).until_not(ec.presence_of_element_located(locator))
        except TimeoutException:
            pass

    # ждать когда перестанет отображаться (в DOM остается)
    def wait_until_element_not_displayed(self, locator, timeout=3):
        try:
            WebDriverWait(self.browser, timeout).until(ec.visibility_of_element_located(locator))
            WebDriverWait(self.browser, 45).until_not(ec.visibility_of_element_located(locator))
        except TimeoutException:
            pass

    def switch_to_next_tab(self):
        time_count = 0
        while len(self.browser.window_handles) == 1:
            time.sleep(0.5)
            time_count += 1
            if time_count > 1000:
                raise Exception("Не дождался открытия следующей вкладки браузера")
        window_after = self.browser.window_handles[1]
        self.browser.switch_to.window(window_after)

    def switch_to_previous_tab(self):
        window_before = self.browser.window_handles[0]
        self.browser.close()
        self.browser.switch_to.window(window_before)

    def move_by_offset(self, locator):
        self.reset_actions()
        element_location = self.find_element(locator).location
        self.actions.move_by_offset(element_location['x'], element_location['y']).perform()

    def move_to_element(self, locator):
        self.reset_actions()
        self.actions.move_to_element(self.find_element(locator)).perform()

    def reset_actions(self):
        self.actions.reset_actions()

    def switch_to_frame(self, n):
        self.browser.switch_to.frame(n)

    def switch_to_default_content(self):
        self.browser.switch_to.default_content()

    def clear_textarea(self, locator):
        while not self.find_element(locator).text == "":
            self.find_element(locator).send_keys(Keys.BACKSPACE)

    def wait_or_report(self, locator, fail_message=None):
        try:
            self.wait_until_element_displayed(locator)
        except TimeoutException:
            pytest.fail(fail_message) or f'Елемент с локатором {locator} не отображается'

    def is_element_present_and_wait(self, locator, timeout=2):
        try:
            Wait(self.browser, timeout).until(ec.visibility_of_element_located(locator))
        except TimeoutException:
            return False
        return True

    def refresh(self):
        self.browser.refresh()
