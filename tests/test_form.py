"""3–4 UI-теста формы (лаб. 11).

Локально страница по умолчанию открывается через file:///…/index.html (сервер не нужен).
В CI задаётся BASE_URL и используется python -m http.server (как в .github/workflows/ci.yml).
"""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_page_has_expected_heading(driver, page_url):
    driver.get(page_url)
    h1 = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "page-title")))
    assert "Форма обратной связи" in h1.text


def test_intro_paragraph_visible(driver, page_url):
    driver.get(page_url)
    intro = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "page-intro")))
    assert len(intro.text.strip()) > 10


def test_form_fields_accept_input(driver, page_url):
    driver.get(page_url)
    name = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "name")))
    email = driver.find_element(By.ID, "email")
    name.clear()
    name.send_keys("Иван Тестов")
    email.clear()
    email.send_keys("ivan@example.com")
    assert "Иван" in name.get_attribute("value")
    assert "ivan@example.com" == email.get_attribute("value")


def test_submit_button_label_and_demo_success_message(driver, page_url):
    driver.get(page_url)
    btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "submit-btn")))
    assert btn.text.strip() == "Отправить"

    driver.find_element(By.ID, "name").send_keys("Анна")
    driver.find_element(By.ID, "email").send_keys("anna@example.com")
    btn.click()

    msg = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "status-msg")))
    assert msg.is_displayed()
    assert "отправлено" in msg.text.lower()
