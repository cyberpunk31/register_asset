from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize WebDriver
driver = webdriver.Chrome()

# Function to reset the URL
def reset_url():
    driver.get("https://dev-myworkwise360.azurewebsites.net/")

# Function to verify toast error messages
def verify_toast_message(expected_message):
    try:
        toast_icon = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".Toastify__toast-icon"))
        )
        svg_icon = toast_icon.find_element(By.TAG_NAME, "svg")
        fill_color = svg_icon.get_attribute("fill")
        assert "var(--toastify-icon-color-error)" in fill_color, "Error icon color mismatch!"
        print(f"Test Passed: Toast message displayed correctly for: {expected_message}")
    except Exception as e:
        print(f"Test Failed: {e}")

# Function to verify successful login
def verify_successful_login():
    try:
        welcome_message = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h3.title"))
        )
        assert "Welcome to WorkWise 360!" in welcome_message.text, "Login failed!"
        print("Test Passed: Login successful!")
    except Exception as e:
        print(f"Test Failed: {e}")

# Test for successful login
def test_valid_credentials():
    reset_url()
    try:
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
        )
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        sign_in_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")

        email_field.clear()
        email_field.send_keys("team@gacdigital.in")
        password_field.clear()
        password_field.send_keys("ACD7BBD6")
        sign_in_button.click()

        verify_successful_login()
    except Exception as e:
        print(f"Test Failed: {e}")

# Test for invalid username/password
def test_invalid_credentials():
    reset_url()
    try:
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
        )
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        sign_in_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")

        email_field.clear()
        email_field.send_keys("wrongemail@gacdigital.in")
        password_field.clear()
        password_field.send_keys("wrongpassword")
        sign_in_button.click()

        verify_toast_message("Invalid Username or Password")
    except Exception as e:
        print(f"Test Failed: {e}")

# Test for empty email
def test_empty_email():
    reset_url()
    try:
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
        )
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        sign_in_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")

        email_field.clear()  # Leave email empty
        password_field.clear()
        password_field.send_keys("ACD7BBD6")
        sign_in_button.click()

        verify_toast_message("Email field is empty")
    except Exception as e:
        print(f"Test Failed: {e}")

# Test for empty password
def test_empty_password():
    reset_url()
    try:
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
        )
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        sign_in_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")

        email_field.clear()
        email_field.send_keys("team@gacdigital.in")
        password_field.clear()  # Leave password empty
        sign_in_button.click()

        verify_toast_message("Password field is empty")
    except Exception as e:
        print(f"Test Failed: {e}")

# Run the tests
if __name__ == "__main__":
    try:
        test_valid_credentials()
        test_invalid_credentials()
        test_empty_email()
        test_empty_password()
    finally:
        driver.quit()
