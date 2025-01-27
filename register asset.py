import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

driver = None


def test_successful_login():
    """
    Test to log in to the application successfully.
    """
    global driver
    driver = webdriver.Chrome()
    try:
        driver.get("https://dev-myworkwise360.azurewebsites.net/")
        driver.maximize_window()

        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Login to the application
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#root > div > div.wrapper > section > div > div > div > div > div > div > div.col-lg-6.align-self-center > div > div > form > div > div:nth-child(1) > div > input")
            )
        )
        email_field.send_keys("team@gacdigital.in")

        password_field = driver.find_element(By.CSS_SELECTOR, "#root > div > div.wrapper > section > div > div > div > div > div > div > div.col-lg-6.align-self-center > div > div > form > div > div:nth-child(2) > div > input")
        password_field.send_keys("ACD7BBD6")

        login_button = driver.find_element(By.CSS_SELECTOR, "#root > div > div.wrapper > section > div > div > div > div > div > div > div.col-lg-6.align-self-center > div > div > button")
        login_button.click()

        # Wait for the welcome message
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "h3.title"))
            )
        except TimeoutException:
            print("Welcome message not found")
            return False

        welcome_message = driver.find_element(By.CSS_SELECTOR, "h3.title").text
        assert "Welcome to WorkWise 360!" in welcome_message, "Login failed!"
        print("Test Passed: Successfully logged in.")
        return True

    except Exception as e:
        print(f"Login Test Failed: {e}")
        return False


def select_react_option(driver, input_selector, option_text):
    """
    Select an option from a React-based dropdown.
    """
    try:
        input_element = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, input_selector))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", input_element)
        input_element.click()

        input_field = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"{input_selector} input.react-select__input"))
        )
        input_field.send_keys(option_text)
        input_field.send_keys(Keys.ENTER)
    except Exception as e:
        print(f"Failed to select option '{option_text}' in dropdown: {e}")


def upload_invoice(file_path):
    """
    Upload an invoice file using the file input field.
    """
    global driver
    try:
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "file"))
        )
        file_input.send_keys(file_path)
        print("Invoice file uploaded successfully!")

    except Exception as e:
        print(f"Error during file upload: {e}")
        raise


def navigate_to_asset_management():
    """
    Navigate to the Asset Management tab.
    """
    global driver
    if driver is None:
        print("Driver not initialized. Please run login test first.")
        return False

    try:
        asset_management_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.nav-link[data-toggle='pill'][href='#asset-management-pan']"))
        )
        asset_management_tab.click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#asset-management-pan > div.app-sidebar-top > div > h5"))
        )
        print("Test Passed: Asset Management tab opened.")
        return True

    except Exception as e:
        print(f"Failed to navigate to Asset Management tab: {e}")
        return False


def navigate_to_register_asset():
    """
    Navigate to the Register Asset page.
    """
    global driver
    if driver is None:
        print("Driver not initialized. Please run login test first.")
        return False

    try:
        register_asset_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#asset-management a[href='/RegisterAsset']"))
        )
        register_asset_link.click()

        print("Test Passed: Navigated to Register Asset page.")
        return True

    except Exception as e:
        print(f"Failed to navigate to Register Asset page: {e}")
        return False


def test_navigation_to_register_page():
    """
    Test to navigate to the Register Asset page and fill the form.
    """
    global driver
    if navigate_to_asset_management():
        if navigate_to_register_asset():
            print("Ready to fill the Register Asset form.")

        try:
            # Read data from CSV file
            with open("asset_data.csv", "r") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    driver.find_element(By.NAME, "AssetId").send_keys(row["AssetId"])
                    driver.find_element(By.NAME, "SerialNumber").send_keys(row["SerialNumber"])
                    select_react_option(driver, "div.react-select__control", row["Category"])
                    driver.find_element(By.NAME, "PurchaseDate").send_keys(row["PurchaseDate"])
                    driver.find_element(By.NAME, "PurchaseOrder").send_keys(row["PurchaseOrder"])
                    select_react_option(driver, '#assetDetails > div:nth-child(6) > div > div > div', row["Location"])
                    driver.find_element(By.NAME, "PurchaseCost").send_keys(row["PurchaseCost"])
                    driver.find_element(By.NAME, "Model").send_keys(row["Model"])
                    driver.find_element(By.NAME, "InvoiceDate").send_keys(row["InvoiceDate"])
                    driver.find_element(By.NAME, "InvoiceNumber").send_keys(row["InvoiceNumber"])
                    upload_invoice(row["InvoiceFilePath"])
                    driver.find_element(By.NAME, "SupplierDetails").send_keys(row["SupplierDetails"])
                    select_react_option(driver, '#additionalDetails > div:nth-child(2) > div > div > div > div', row["SupplierLocation"])
                    driver.find_element(By.NAME, "SupplierContact").send_keys(row["SupplierContact"])
                    driver.find_element(By.NAME, "WarrantyStartDate").send_keys(row["WarrantyStartDate"])
                    driver.find_element(By.NAME, "WarrantyEndDate").send_keys(row["WarrantyEndDate"])
                    select_react_option(driver, "#additionalDetails > div:nth-child(5) > div > div", row["Condition"])

                    # Submit the form
                    submit_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "#root > div > div.content > div > div.row.fixed-footer > div > button.btn.btn-primary"))
                    )
                    submit_button.click()

                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.col-12.text-success.text-center i.ri-checkbox-circle-fill"))
                    )
                    print("Asset registered successfully!")

        except Exception as e:
            print(f"Navigation Test Failed: {e}")
        finally:
            if driver is not None:
                driver.quit()


if __name__ == "__main__":
    if test_successful_login():
        test_navigation_to_register_page()
