import io
import time
import base64
import argparse
from PIL import Image
from pathlib import Path
from typing import Literal
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from src.roller import Roller



class BirthdayEmail(Roller):
    
    def __init__(self, debug=True) -> None:
        super().__init__(debug)

        self.table_xpath = "//div[@class='roller-grid ng-scope dx-widget dx-visibility-change-handler']"
        self.tbody_xpath = "/html/body/div[1]/div[3]/div[1]/div/div[2]/div[1]/roller-grid2/div[2]/div/div[6]/div/div/div[1]/div/table/tbody"


    @staticmethod
    def is_table_present(driver, xpath):
        try:
            # Try to find the element using the provided XPath
            driver.find_element(By.XPATH, xpath)
            return True
        except NoSuchElementException:
            return False
        
    def birthday_config(self): 
        WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, "//a[@id='bookings']"))
        )
        
        homepage_document = self.wait_watch_grab("//a[@id='bookings']")
        homepage_document.click()

        # switch driver to iframe 
        iframe = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.ID, "vmFrame"))
        )
        self.driver.switch_to.frame(iframe)
        
        # click on the dropdown *products*
        products_dropdown = self.wait_watch_grab(xpath="//button[@qa-id='select-filter-BOOKINGS.COMPONENTS.FILTER.PRODUCT_LABEL']//p[@class='flush _flex--center']")
        products_dropdown.click()
        
        # click on membership > 
        arrow_mem = self.wait_watch_grab(xpath="//li[@qa-id='product-type-Party packages']//a[@class='_flex--between one-whole list-item']")
        arrow_mem.click()
        
        # apply the filters 
        apply = self.wait_watch_grab(xpath="//button[@class='btn btn--primary btn--small']")
        apply.click()
        
        self.wait_for_seconds(driver=self.driver,seconds=10)


    def click_row_by_xpath(self, row_xpath):
        try:
            # Wait for the row to be present in the DOM
            row = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, row_xpath))
            )

            # Scroll the row into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", row)

            # Wait a bit for any animations to complete
            time.sleep(1)

            # Wait for the row to be clickable
            clickable_row = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable((By.XPATH, row_xpath))
            )

            # Click the row
            clickable_row.click()
        except Exception as e:
            print(f"Error clicking row {row_xpath}: {str(e)}")

    def get_all_Data(self,row_xpath): 
        
        data = {}

        # before clicking grab other stuffs as well
        #############################################

        self.click_row_by_xpath(row_xpath=row_xpath)

        self.custom_click(
            "/html[1]/body[1]/div[1]/div[3]/div[1]/div[2]/div[1]/form[1]/div[1]/ul[1]/li[1]/a[1]"
        )

        data["name"] = self.grab_text(
            "/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/form/div[2]/ui-view/div/section[1]/div[2]/ng-transclude/div[1]/div[1]/p[2]"
        )
        data["phone"] = self.grab_text(
            "/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/form/div[2]/ui-view/div/section[1]/div[2]/ng-transclude/div[1]/div[2]/p[2]"
        )
        data["email"] = self.grab_text(
            "/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/form/div[2]/ui-view/div/section[1]/div[2]/ng-transclude/div[2]/div/p[2]"
        )
        data["address"] = self.grab_text(
            "/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/form/div[2]/ui-view/div/section[1]/div[2]/ng-transclude/div[3]/p[2]"
        )
        
        
        text_box = self.driver.find_element(By.XPATH, '//*[@id="booking-name"]')

        text_value = text_box.get_attribute('value')        
        
        data["event"] = text_value

        return data


    def get_infos(self):

        data = {}
        if self.is_table_present(self.driver,xpath=self.table_xpath):
            

            # Locate the table rows containing data
            data_row_elements = self.driver.find_elements(By.XPATH, "//div[@class='roller-grid ng-scope dx-widget dx-visibility-change-handler']//tr[contains(@class, 'dx-data-row')]")

            # Print XPaths of individual rows
            row_xpaths = []
            for i, row in enumerate(data_row_elements, start=1):
                # Generate XPath for each row
                row_xpath = f"//div[@class='roller-grid ng-scope dx-widget dx-visibility-change-handler']//tr[contains(@class, 'dx-data-row')][{i}]"
                row_xpaths.append(row_xpath)

            for i, row_xpath in enumerate(row_xpaths):
                # Wait for the row to be present
                row_obj = self.wait_watch_grab(xpath=row_xpath)
                
                # Scroll the row into view
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", row_obj)
                time.sleep(2)  # Allow time for scrolling animation if needed

                # 
                data[str(i)] =  self.get_all_Data(row_xpath=row_xpath)
                

                # Backspace logic after clicking each row
                self.driver.switch_to.default_content()
                
                WebDriverWait(self.driver, self.timeout).until(
                    EC.presence_of_element_located((By.XPATH, "//a[@id='bookings']"))
                )
                time.sleep(3)
                homepage_document = self.wait_watch_grab("//a[@id='bookings']")
                homepage_document.click()

                # Switch driver to iframe
                iframe = WebDriverWait(self.driver, self.timeout).until(
                    EC.presence_of_element_located((By.ID, "vmFrame"))
                )
                self.driver.switch_to.frame(iframe)
                
                time.sleep(1) 
                
            
        else:
            print(f"There's no party today.")
    
        print(data)      
if __name__ == "__main__":
    
    # open roller 
    bday = BirthdayEmail(debug=True)
    bday.login_to_roller()
    bday.handle_popup(driver=bday.driver)
    bday.birthday_config()
    bday.get_infos()