import os

import allure
import requests
from allure_commons.types import AttachmentType
from selene import browser


def attach_bstack_video(session_id):
    bstack_session = requests.get(
        f'https://api.browserstack.com/app-automate/sessions/{session_id}.json',
        auth=(os.getenv('BS_USERNAME'), os.getenv('BS_ACCESSKEY')),
    ).json()
    video_url = bstack_session['automation_session']['video_url']

    allure.attach(
        '<html><body>'
        '<video width="100%" height="100%" controls autoplay>'
        f'<source src="{video_url}" type="video/mp4">'
        '</video>'
        '</body></html>',
        name='video recording',
        attachment_type=allure.attachment_type.HTML,
    )

def add_screenshot():
    allure.attach(
        browser.driver.get_screenshot_as_png(),
        name='screenshot',
        attachment_type=allure.attachment_type.PNG,
    )
    # png = browser.driver.get_screenshot_as_png()
    # allure.attach(body=png, name="Screenshot", attachment_type=AttachmentType.PNG)

def add_xml():
    allure.attach(
        browser.driver.page_source,
        name='screen xml dump',
        attachment_type=allure.attachment_type.XML,
    )
    # xml_dump = browser.driver.page_source
    # allure.attach(body=xml_dump, name="XML Screen", attachment_type=AttachmentType.XML)




