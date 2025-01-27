from selenium import webdriver 

# Initialize WebDriver 

driver = webdriver.Chrome()  # Replace with your WebDriver (e.g., Firefox(), Edge(), etc.) 

# Open a website 

driver.get("https://www.google.com") 

print("Title of the page:", driver.title) 

# Close the browser 

driver.quit() 