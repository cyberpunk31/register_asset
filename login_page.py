from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def enter_email(self, email):
        try:
            email_field = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
            )
            email_field.clear()
            email_field.send_keys(email)
        except TimeoutException:
            print("Error: Email field not found.")
            raise

    def enter_password(self, password):
        try:
            password_field = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
            )
            password_field.clear()
            password_field.send_keys(password)
        except TimeoutException:
            print("Error: Password field not found.")
            raise

    def click_sign_in(self):
        try:
            sign_in_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
            )
            sign_in_button.click()
        except TimeoutException:
            print("Error: Sign-in button not found.")
            raise

    def get_error_message(self):
        try:
            error_message_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.Toastify__progress-bar--error"))
            )
            return error_message_element.get_attribute("aria-label") or "Error notification displayed"
        except TimeoutException:
            print("Warning: Error message element not found.")
            return ""
