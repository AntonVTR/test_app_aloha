import pytest
import time
import requests
import logging
import os
import datetime
import subprocess
from pytest_html import extras
from playwright.sync_api import sync_playwright

ALOHA_PATH = r'C:\Users\Administrator\AppData\Local\Aloha Mobile\Aloha\Application\aloha.exe'
ALOHA_USER_DATA = r'C:\Users\Administrator\AppData\Local\AlohaUserData'
DEBUG_PORT = 9222
LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def start_aloha():
    proc = subprocess.Popen([
        ALOHA_PATH,
        f'--remote-debugging-port={DEBUG_PORT}',
        f'--user-data-dir={ALOHA_USER_DATA}'
    ])

    # Wait for CDP
    for _ in range(15):
        try:
            r = requests.get(f"http://localhost:{DEBUG_PORT}/json/version")
            if r.status_code == 200:
                break
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    else:
        proc.terminate()
        raise RuntimeError("Aloha Browser did not expose CDP on port 9222")

    yield

    proc.terminate()


@pytest.fixture(scope="function")
def browser_context(start_aloha):
    with sync_playwright() as p:
        response = requests.get(f"http://localhost:{DEBUG_PORT}/json/version")
        ws_endpoint = response.json()["webSocketDebuggerUrl"]
        browser = p.chromium.connect_over_cdp(ws_endpoint)
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        yield context

        for page in context.pages:
            if not page.is_closed():
                page.close()


@pytest.fixture(autouse=True)
def log_test_start_end(request):
    log = logging.getLogger(request.node.name)
    log.setLevel(logging.INFO)
    handler = logging.FileHandler(f"logs/{request.node.name}.log", mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    log.addHandler(handler)

    request.node._logger = log
    log.info(f"START TEST: {request.node.name}")
    yield
    log.info(f"END TEST: {request.node.name}")
    log.removeHandler(handler)
    handler.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        context = item.funcargs.get("browser_context", None)
        if context and context.pages:
            page = context.pages[0]
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshots_dir = os.path.join("report", "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshots_dir, f"sh_{ts}_{item.name}.png")
            try:
                page.screenshot(path=screenshot_path)
                if hasattr(report, "extra"):
                    report.extra.append(extras.image(screenshot_path))
                else:
                    report.extra = [extras.image(screenshot_path)]
            except Exception as e:
                logger.error(f"Failed to take screenshot: {e}")