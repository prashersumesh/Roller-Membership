from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


from src.credentials import Authentication

class Roller(Authentication):
    def __init__(self, debug = True) -> None:

        self.timeout = 10
        self.username, self.password = self.load_credentials()

        if debug:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            self.driver.maximize_window()
        else:
            # Set up Chrome options for headless mode
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Enable headless mode
            chrome_options.add_argument("--disable-gpu")  # Disable GPU (optional for stability)
            chrome_options.add_argument("--no-sandbox")  # Bypass OS-level sandbox (needed in some environments)
            chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome resource limitations in Docker
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            self.driver.maximize_window()
            

    def handle_popup(self, driver):
        """
        Checks for a popup menu on a webpage. If found, closes it. Otherwise, continues.

        Parameters:
            driver (selenium.webdriver): The WebDriver instance controlling the browser.
        """
        try:
            
            iframe = WebDriverWait(driver, self.timeout).until(
            EC.presence_of_element_located((By.ID, "vmFrame"))
            )
            driver.switch_to.frame(iframe)
            # Check for the popup using the provided XPath
            popup = driver.find_element(By.XPATH, "//section[contains(@class,'main hide-search-input')]")
            
            if popup.is_displayed():
                print("Popup detected. Attempting to close it...")
                # Find the close button using the second XPath and click it
                close_button = driver.find_element(By.XPATH, "//div[@class='close']//*[name()='svg']")
                close_button.click()
                print("Popup closed successfully.")
            else:
                print("Popup is not displayed.")

        except NoSuchElementException:
            print("No popup detected. Proceeding...")

        
        driver.switch_to.default_content()
        
    def wait_for_seconds(self,driver, seconds):
        try:
            WebDriverWait(driver, seconds).until(lambda driver: False)  # This will always time out after `seconds`
        except TimeoutException:
            pass

    def wait_watch_grab(self, xpath):
        element_present = EC.presence_of_element_located((By.XPATH, xpath))
        WebDriverWait(self.driver, self.timeout).until(element_present)
        return self.driver.find_element(By.XPATH, xpath)

    def custom_click(self, xpath):
        driver_obj = self.wait_watch_grab(xpath=xpath)
        driver_obj.click()

    def grab_text(self, xpath):
        driver_obj = self.wait_watch_grab(xpath=xpath)
        return driver_obj.text


    def login_to_roller(self):
        
        # Define xpaths
        self.username_xpath = "/html/body/div/div[2]/div/form/label[1]/input"
        self.password_xpath = "/html/body/div/div[2]/div/form/label[2]/input"
        self.roller_roll_in_xpath = "/html/body/div/div[2]/div/form/button"
        
        self.driver.get("https://manage.roller.app/")

        # Login
        username_field = self.wait_watch_grab(self.username_xpath)
        password_field = self.wait_watch_grab(self.password_xpath)
        roll_in_field = self.wait_watch_grab(self.roller_roll_in_xpath)
        username_field.send_keys(self.username)
        password_field.send_keys(self.password)
        roll_in_field.click()
        
        self.wait_for_seconds(self.driver,8)



    def switch_veneue(self, venue): 
        
        # click account 
        self.custom_click(xpath="//div[@class='sidebar__footer']//button[1]//span[4]")
        
        self.wait_for_seconds(self.driver,2)
        
        
        # click swith venue 
        self.custom_click("//button[@data-track-id='account-switch-venue']//span[@class='inner-wrapper']")
        
        self.wait_for_seconds(self.driver,2)
        
        if venue == "london": 
            self.custom_click("//span[@class='venue-switch--venue non-hq-venue'][normalize-space()='Aerosports London']")
        
        self.wait_for_seconds(self.driver,2)
        
