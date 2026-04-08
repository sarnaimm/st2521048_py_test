import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://st2521048-py-test.vercel.app/"

@pytest.fixture(scope="session")
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    yield driver
    time.sleep(3)
    driver.quit()

def test_1_login(driver):
    print("\nTest start: Login")
    driver.get(BASE_URL)
    time.sleep(2)

    driver.find_element(By.ID, "username").send_keys("munkhsarnai")
    time.sleep(1)

    driver.find_element(By.ID, "password").send_keys("@Dm1n")
    time.sleep(1)

    driver.find_element(By.CSS_SELECTOR, ".login-card button").click()
    time.sleep(2)

    app = driver.find_element(By.ID, "app")
    assert app.is_displayed(), "App should be visible after successful login"
    print("Login successful!")

def test_2_invalid_login(driver):
    print("\nTest start: Invalid Login")
    driver.get(BASE_URL)
    time.sleep(2)

    driver.find_element(By.ID, "username").send_keys("wronguser")
    time.sleep(1)
    driver.find_element(By.ID, "password").send_keys("wrongpass")
    time.sleep(1)

    driver.find_element(By.CSS_SELECTOR, ".login-card button").click()
    time.sleep(1)

    error = driver.find_element(By.ID, "loginError").text
    assert error != "", "Error message should appear for invalid credentials"
    print(f"Error message shown: {error}")

def test_3_navigate_cameras(driver):
    print("\nTest start: Navigate to Cameras tab")
    # Login first
    driver.get(BASE_URL)
    time.sleep(2)
    driver.find_element(By.ID, "username").send_keys("munkhsarnai")
    driver.find_element(By.ID, "password").send_keys("@Dm1n")
    driver.find_element(By.CSS_SELECTOR, ".login-card button").click()
    time.sleep(2)

    driver.find_element(By.XPATH, "//nav//button[contains(text(), 'Cameras')]").click()
    time.sleep(1)

    cameras_section = driver.find_element(By.ID, "cameras")
    assert cameras_section.is_displayed(), "Cameras section should be visible"
    print("Cameras tab works!")

def test_4_navigate_lenses(driver):
    print("\nTest start: Navigate to Lenses tab")

    driver.find_element(By.XPATH, "//nav//button[contains(text(), 'Lenses')]").click()
    time.sleep(1)

    lenses_section = driver.find_element(By.ID, "lenses")
    assert lenses_section.is_displayed(), "Lenses section should be visible"

    cameras_section = driver.find_element(By.ID, "cameras")
    assert not cameras_section.is_displayed(), "Cameras section should be hidden"
    print("Lenses tab works!")

def test_5_navigate_contact(driver):
    print("\nTest start: Navigate to Contact tab")

    driver.find_element(By.XPATH, "//nav//button[contains(text(), 'Contact')]").click()
    time.sleep(1)

    contact_section = driver.find_element(By.ID, "contact")
    assert contact_section.is_displayed(), "Contact section should be visible"

    lenses_section = driver.find_element(By.ID, "lenses")
    assert not lenses_section.is_displayed(), "Lenses section should be hidden"
    print("Contact tab works!")

def test_6_contact_form_empty_submit(driver):
    print("\nTest start: Contact form empty submit")

    # Make sure we are on the Contact tab
    driver.find_element(By.XPATH, "//nav//button[contains(text(), 'Contact')]").click()
    time.sleep(1)

    driver.find_element(By.CSS_SELECTOR, ".form-container button[type='submit']").click()
    time.sleep(1)

    name_error = driver.find_element(By.ID, "nameError").text
    assert name_error != "", "Name error should appear when name is empty"
    print(f"Name error shown: {name_error}")

def test_7_contact_form_invalid_email(driver):
    print("\nTest start: Contact form invalid email")

    driver.find_element(By.XPATH, "//nav//button[contains(text(), 'Contact')]").click()
    time.sleep(1)

    email_field = driver.find_element(By.ID, "email")
    email_field.clear()
    email_field.send_keys("not-an-email")
    time.sleep(1)

    driver.execute_script("document.getElementById('email').dispatchEvent(new Event('input'));")
    time.sleep(1)

    email_error = driver.find_element(By.ID, "emailError").text
    assert email_error != "", "Email error should appear for invalid format"
    print(f"Email error shown: {email_error}")

def test_8_contact_form_invalid_phone(driver):
    print("\nTest start: Contact form invalid phone")

    driver.find_element(By.XPATH, "//nav//button[contains(text(), 'Contact')]").click()
    time.sleep(1)

    phone_field = driver.find_element(By.ID, "phone")
    phone_field.clear()
    phone_field.send_keys("123")
    time.sleep(1)

    driver.execute_script("document.getElementById('phone').dispatchEvent(new Event('input'));")
    time.sleep(1)

    phone_error = driver.find_element(By.ID, "phoneError").text
    assert phone_error != "", "Phone error should appear for invalid number"
    print(f"Phone error shown: {phone_error}")

def test_9_contact_form_valid_submit(driver):
    print("\nTest start: Contact form valid submit")

    driver.find_element(By.XPATH, "//nav//button[contains(text(), 'Contact')]").click()
    time.sleep(1)

    name_field = driver.find_element(By.ID, "name")
    name_field.clear()
    name_field.send_keys("Munkhsarnai Munkhochir")
    time.sleep(1)

    email_field = driver.find_element(By.ID, "email")
    email_field.clear()
    email_field.send_keys("sarnai@gmail.com")
    driver.execute_script("document.getElementById('email').dispatchEvent(new Event('input'));")
    time.sleep(1)

    phone_field = driver.find_element(By.ID, "phone")
    phone_field.clear()
    phone_field.send_keys("+35988123456")
    driver.execute_script("document.getElementById('phone').dispatchEvent(new Event('input'));")
    time.sleep(1)

    driver.find_element(By.ID, "message").send_keys("Hello from Selenium test!")
    time.sleep(1)

    driver.find_element(By.CSS_SELECTOR, ".form-container button[type='submit']").click()
    time.sleep(2)

    success_msg = driver.find_element(By.ID, "formSuccess").text
    assert "successfully" in success_msg.lower(), "Success message should appear after valid submission"
    print(f"Success message shown: {success_msg}")

def test_10_logout(driver):
    print("\nTest start: Logout")

    driver.find_element(By.CSS_SELECTOR, ".logout").click()
    time.sleep(2)
    login_page = driver.find_element(By.ID, "loginPage")
    assert login_page.is_displayed(), "Login page should be visible after logout"
    print("Logout successful!")