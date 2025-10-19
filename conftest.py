import os
import allure
import allure_commons
from dotenv import load_dotenv
import pytest
from selene import browser,support
from appium import webdriver
from resources.utils.attach import attach_bstack_video, add_screenshot, add_xml
import config as app_config


def pytest_addoption(parser):
    parser.addoption(
        "--context",
        default="bstack",
        help="Выбор окружения для запуска теста: local device (локальный девайс), local emulator (локальный эмулятор) или bstack (BrowserStack)"
    )


def pytest_configure(config):
    context = config.getoption("--context")
    os.environ["CONTEXT"] = context
    load_dotenv(f".env.{context}")
    load_dotenv('.env.credentials')

@pytest.fixture
def context(request):
    return request.config.getoption("--context")


@pytest.fixture(scope='function', autouse=True)
def mobile_management(context):
    os.environ.pop("UDID", None)
    context_name = app_config.context_manager()
    options = app_config.to_driver_options(context_name)

    browser.config.driver = webdriver.Remote(options.get_capability('remote_url'), options=options)
    browser.config.timeout = float(os.getenv('timeout', '10.0'))

    browser.config._wait_decorator = support._logging.wait_with(
                context=allure_commons._allure.StepContext
            )

    yield

    session_id = browser.driver.session_id

    add_screenshot()
    add_xml()

    with allure.step('tear down app session'):
        browser.quit()

    if context == 'bstack':
        attach_bstack_video(session_id)


