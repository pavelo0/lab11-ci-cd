"""Фикстуры Selenium для UI-тестов статической страницы."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,720")
    chromium = os.environ.get("CHROME_BINARY") or os.environ.get("CHROMIUM_BIN")
    if chromium:
        opts.binary_location = chromium

    drv = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opts,
    )
    drv.implicitly_wait(3)
    try:
        yield drv
    finally:
        drv.quit()


@pytest.fixture
def page_url() -> str:
    """
    Полный URL страницы формы.

    - В CI задаётся BASE_URL=http://127.0.0.1:8765 (страница отдаётся через http.server).
    - Локально по умолчанию открывается file:///.../index.html (сервер не нужен).
    """
    base = os.environ.get("BASE_URL", "").strip().rstrip("/")
    if base:
        return f"{base}/index.html"
    html = Path(__file__).resolve().parent.parent / "index.html"
    return html.resolve().as_uri()
