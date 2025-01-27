from selenium import webdriver
from selenium.webdriver.common.by import By
from login_page import LoginPage
import time


def test_valid_login():
    driver = webdriver.Chrome()
    try:
        driver.get("https://dev-myworkwise360.azurewebsites.net/")
        driver.maximize_window()
        login_page = LoginPage(driver)

        # Enter valid credentials
        login_page.enter_email("team@gacdigital.in")
        login_page.enter_password("ACD7BBD6")
        login_page.click_sign_in()

        # Validate successful login
        time.sleep(5)  # Allow time for the page to load
        welcome_message = driver.find_element(By.CSS_SELECTOR, "h3.title").text
        assert "Welcome to WorkWise 360!" in welcome_message, "Login failed!"
        print("Test Passed: Valid login")
    except Exception as e:
        print(f"Test Failed: {e}")
    finally:
        driver.quit()


def test_invalid_login():
    driver = webdriver.Chrome()
    try:
        driver.get("https://dev-myworkwise360.azurewebsites.net/")
        driver.maximize_window()
        login_page = LoginPage(driver)

        # Enter invalid credentials
        login_page.enter_email("invalid_email@gacdigital.in")
        login_page.enter_password("wrongpassword")
        login_page.click_sign_in()

        # Validate error message for invalid credentials
        time.sleep(3)  # Allow time for the toast message
        error_message = login_page.get_error_message()
        assert "notification timer" in error_message, "Error message for invalid credentials not displayed!"
        print("Test Passed: Invalid login error displayed")
    except Exception as e:
        print(f"Test Failed: {e}")
    finally:
        driver.quit()


def test_empty_email():
    driver = webdriver.Chrome()
    try:
        driver.get("https://dev-myworkwise360.azurewebsites.net/")
        driver.maximize_window()
        login_page = LoginPage(driver)

        # Leave email empty, enter password
        login_page.enter_email("")
        login_page.enter_password("ACD7BBD6")
        login_page.click_sign_in()

        # Validate error message for empty email
        time.sleep(3)
        error_message = login_page.get_error_message()
        assert "notification timer" in error_message, "Error message for empty email not displayed!"
        print("Test Passed: Empty email error displayed")
    except Exception as e:
        print(f"Test Failed: {e}")
    finally:
        driver.quit()


def test_empty_password():
    driver = webdriver.Chrome()
    try:
        driver.get("https://dev-myworkwise360.azurewebsites.net/")
        driver.maximize_window()
        login_page = LoginPage(driver)

        # Enter email, leave password empty
        login_page.enter_email("team@gacdigital.in")
        login_page.enter_password("")
        login_page.click_sign_in()

        # Validate error message for empty password
        time.sleep(3)
        error_message = login_page.get_error_message()
        assert "notification timer" in error_message, "Error message for empty password not displayed!"
        print("Test Passed: Empty password error displayed")
    except Exception as e:
        print(f"Test Failed: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    test_valid_login()
    test_invalid_login()
    test_empty_email()
    test_empty_password()
