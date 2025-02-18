import time
import pytest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(
    filename="test_log.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger()


@pytest.fixture(scope="module")
def driver():
    logger.info("Starting Webdriver...")
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()


# @pytest.mark.skip
def test_invalid_login(driver):
    username = driver.find_element(By.ID, "user-name")
    password = driver.find_element(By.ID, "password")
    login_btn = driver.find_element(By.ID, "login-button")

    username.send_keys("standard_user1")
    password.send_keys("secret-sauce")
    login_btn.click()

    error_message = driver.find_element(By.XPATH, '//*[@id="login_button_container"]/div/form/div[3]/h3')

    assert error_message.text == "Epic sadface: Username and password do not match any user in this service"


# @pytest.mark.skip
def test_valid_login(driver):
    logger.info("Executing test: test_valid_login")
    driver.refresh()
    username = driver.find_element(By.ID, "user-name")
    password = driver.find_element(By.ID, "password")
    login_btn = driver.find_element(By.ID, "login-button")

    username.send_keys("standard_user")
    password.send_keys("secret_sauce")
    login_btn.click()

    check = driver.find_element(By.XPATH, '//*[@id="header_container"]/div[2]/span')
    logger.info(f"Logged in check text: {check.text}")
    assert check.text == "Products"


def test_sort(driver):
    sort_dropdown = driver.find_element(By.CLASS_NAME, "product_sort_container")
    select = Select(sort_dropdown)

    select.select_by_value("az")


def test_add_to_cart(driver):
    first_item = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
    first_item.click()

    cart_value = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    assert "1" in cart_value.text


def test_shopping_cart(driver):
    your_cart = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    your_cart.click()

    time.sleep(5)


def test_continue_shopping(driver):
    continue_button = driver.find_element(By.ID, "continue-shopping")
    continue_button.click()

    verify = driver.find_element(By.CLASS_NAME, "title")

    assert verify.text == "Products"


def test_next_add_to_cart(driver):
    next_item = driver.find_element(By.ID, "add-to-cart-sauce-labs-onesie")
    next_item.click()

    cart_value = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    assert "2" in cart_value.text


def test_shopping_cart_again(driver):
    your_cart = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    your_cart.click()


# @pytest.mark.skip
def test_checkout(driver):
    checkout_button = driver.find_element(By.ID, "checkout")
    checkout_button.click()


# @pytest.mark.skip
def test_checkout_information(driver):
    first_name = driver.find_element(By.ID, "first-name")
    last_name = driver.find_element(By.ID, "last-name")
    zip = driver.find_element(By.ID, "postal-code")

    first_name.send_keys("Rosie")
    last_name.send_keys("Brown")
    zip.send_keys("HA8 7ST")

    continue_btn = driver.find_element(By.ID, "continue").click()

    chkout = driver.find_element(By.CLASS_NAME, "summary_info_label")

    assert chkout.text == "Payment Information:"


# @pytest.mark.skip
def test_finish_button(driver):
    finish_button = driver.find_element(By.ID, "finish")

    driver.execute_script("arguments[0].scrollIntoView();", finish_button)

    finish_button.click()

    confirmation_msg = driver.find_element(By.CLASS_NAME, "complete-header")

    assert confirmation_msg.text == "Thank you for your order!"


# @pytest.mark.skip
def test_burger_menu_button(driver):
    burger_menu = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "react-burger-menu-btn")))
    burger_menu.click()


# @pytest.mark.skip
def test_reset_app_state(driver):
    reset = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "reset_sidebar_link")))
    reset.click()


# @pytest.mark.skip
def test_logout(driver):
    logout_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "logout_sidebar_link")))
    logout_button.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-button")))
