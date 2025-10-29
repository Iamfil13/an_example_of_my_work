from contextlib import contextmanager
from timeit import default_timer as timer

import allure
import pytest
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from pages.metrics import Metrics, MonitoringApiClient


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox",
                     help="Browser to run tests (firefox, chrome)")
    parser.addoption("--headless", action="store", default="false",
                     help="Run browser in headless mode (true/false)")
    parser.addoption("--metrics", action="store", default="false", help="Enable metrics sending (true/false)")


@pytest.fixture()
def browser(request):
    browser_name = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless").lower() == "true"

    options = None
    driver = None

    if browser_name == "firefox":
        options = FirefoxOptions()
        options.set_capability("pageLoadStrategy", "none")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        options.accept_insecure_certs = True
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)

    elif browser_name == "chrome":
        options = ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--ignore-certificate-errors")
        if headless:
            options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    driver.set_page_load_timeout(45)
    print("\nБраузер открывается...")

    yield driver

    print("\nБраузер закрывается...")
    driver.quit()


@pytest.fixture(scope="module", autouse=True)
def metrics(request):
    start_time = timer()
    metrics = Metrics()
    yield metrics
    total_time = round(timer() - start_time)
    metrics.total_time.labels(metrics.job_desc, metrics.product).set(total_time)

    if request.config.getoption("metrics").lower() == "true":
        print("Отправка метрик")
        metrics.push()
    else:
        print("Метрики не отправлены")


@pytest.fixture(scope="module", autouse=True)
def api_client(request):
    client = MonitoringApiClient()
    yield client

    if request.config.getoption("metrics").lower() == "true":
        client.send_result()


@contextmanager
def step_wrapper(step_name, step_desc, critical_time, browser, metrics, client):
    print(step_desc)
    with allure.step(step_desc):
        start = timer()
        try:
            client.set_last_step(step_desc)
            yield
            step_time = round(timer() - start)
            if step_time > critical_time:
                client.set_failed_timeout(True)
                pytest.fail("Превышен критичный порог времени выполнения шага")
            metrics.set_metrics(step_name, step_desc, step_time, cluster='1')
            allure.attach(browser.get_screenshot_as_png(), name="screenshot", attachment_type=AttachmentType.PNG)
        except:
            step_time = round(timer() - start)
            if step_time > critical_time:
                client.set_failed_timeout(True)
            client.set_failed(True)
            metrics.set_fail_step_metric(step_name, step_desc, step_time, cluster='1')
            allure.attach(browser.get_screenshot_as_png(), name="error", attachment_type=AttachmentType.PNG)
            raise
