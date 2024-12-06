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
from src.membership.renderer import get_pdf
from src.membership.logs import LogManager 
from src.gdrive import GoogleDriveUploader

logger = LogManager()

class MembershipBot(Roller): 
    
    def __init__(self, gdrive_folder_id : str = None ,debug=True) -> None:
        super().__init__(debug)
        self.table_xpath = "//div[@class='roller-grid ng-scope dx-widget dx-visibility-change-handler']"
        self.tbody_xpath = "/html/body/div[1]/div[3]/div[1]/div/div[2]/div[1]/roller-grid2/div[2]/div/div[6]/div/div/div[1]/div/table/tbody"

        self.gdrive_folder_id = gdrive_folder_id
        
    def booking_config(self): 
        
        
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
        arrow_mem = self.wait_watch_grab(xpath="//li[@qa-id='product-type-Memberships']//span[@class='icon__arrow material-icons md-16'][normalize-space()='play_arrow']")
        arrow_mem.click()
        
        gold_membership_yearly_select_xpath = "//li[@qa-id='product-type-Gold Membership Annually']//div[@class='_flex--center one-whole hover multi-select__group']"
        gold_membership_monthly_select_xpath= "//li[@qa-id='product-type-Gold Membership Monthly']//div[@class='_flex--center one-whole hover multi-select__group']"
        platinum_mem_ann_xpth = "//li[@qa-id='product-type-Platinum Membership Annually']//div[@class='_flex--center one-whole hover multi-select__group']"
        platinum_mem_monthly_xpth = "//li[@qa-id='product-type-Platinum Membership Monthly']//div[@class='_flex--center one-whole hover multi-select__group']"
        
        meme_type = self.wait_watch_grab(xpath=gold_membership_yearly_select_xpath)
        meme_type.click()
        meme_type = self.wait_watch_grab(xpath=gold_membership_monthly_select_xpath)
        meme_type.click()
        meme_type = self.wait_watch_grab(xpath=platinum_mem_ann_xpth)
        meme_type.click()
        meme_type = self.wait_watch_grab(xpath=platinum_mem_monthly_xpth)
        meme_type.click()
        
        # apply the filters 
        apply = self.wait_watch_grab(xpath="//button[@class='btn btn--primary btn--small']")
        apply.click()
        

    @staticmethod
    def is_table_present(driver, xpath):
        try:
            # Try to find the element using the provided XPath
            driver.find_element(By.XPATH, xpath)
            return True
        except NoSuchElementException:
            return False


    def get_user_data(self, row_xpath):

        data = {}

        # before clicking grab other stuffs as well
        #############################################

        self.click_row_by_xpath(row_xpath=row_xpath)

        ################################################### The documents page ######################################
        data["booking_id"] = self.grab_text(
            "/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]/p[2]/span"
        )

        data["booking_date"] = self.grab_text(
            "/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/p[2]/span/p"
        )

        data["booking_total"] = self.grab_text(
            "/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[3]/p[2]/span"
        )

        data["status"] = self.grab_text(
            "/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[4]/p[2]/p/span[1]"
        )

        data["fees"] = self.grab_text(
            "/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[5]/p[2]/span"
        )

        data["inventory"] = self.grab_text(
            "/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[6]/p[2]/p"
        )

        data["discount"] = self.grab_text(
            "/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[7]/p[2]/span"
        )

        ####################### GO to DETAILS ###################################
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

        ######################### Go to orders ####################################
        self.custom_click(
            xpath="/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/form/div[1]/ul/li[2]/a"
        )
        data["membership"] = self.grab_text(
            "/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/form/div[2]/ui-view/div/div/div[1]/div[2]/div[2]/div/div[1]/strong"
        )

        ######################## Go to Payments ####################################
        self.custom_click(
            xpath="/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/form/div[1]/ul/li[4]"
        )

        data["paid_up_to"] = self.grab_text(
            xpath="/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/form/div[2]/ui-view/div/div[1]/div/div/div[2]/p"
        )
        data["payment_type"] = self.grab_text(
            "/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/form/div[2]/ui-view/div/roller-grid2/div[2]/div/div[6]/div/div/div[1]/div/table/tbody/tr[1]/td[3]"
        )

        data["transction_id"] = self.grab_text(
            "/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/form/div[2]/ui-view/div/roller-grid2/div[2]/div/div[6]/div/div/div[1]/div/table/tbody/tr[1]/td[4]"
        )

        ######################### Got to Documents ##################################

        self.custom_click(
            "/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/form/div[1]/ul/li[5]"
        )

        # enter the detailed mode
        self.custom_click(
            "/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/form/div[2]/ui-view/section[1]/div[2]/roller-grid2/div[2]/div/div[6]/div/div/div[1]/div/table/tbody/tr[1]"
        )

        data["form_status"] = self.grab_text(
            "/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/form/div[2]/ui-view/section[1]/div[2]/div/div/div[1]/div[2]/div[3]/div/button/span[2]"
        )

        signature_div = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.rf-question-signature")
            )
        )

        # Give some time for the signature to be fully rendered
        time.sleep(2)

        # Find all canvas elements within the signature div
        canvases = signature_div.find_elements(By.TAG_NAME, "canvas")

        for i, canvas in enumerate(canvases):
            try:
                # Get the canvas as a base64 encoded PNG
                canvas_base64 = self.driver.execute_script(
                    """
                    var canvas = arguments[0];
                    var ctx = canvas.getContext('2d');
                    var imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                    var blank = true;
                    for (var i = 0; i < imageData.data.length; i += 4) {
                        if (imageData.data[i+3] !== 0) {
                            blank = false;
                            break;
                        }
                    }
                    if (blank) {
                        return null;
                    }
                    return canvas.toDataURL('image/png').substring(22);
                """,
                    canvas,
                )

                if canvas_base64:
                    # Decode the base64 string
                    canvas_png = base64.b64decode(canvas_base64)

                    image = Image.open(io.BytesIO(canvas_png))

                    data["signature"] = image

                    break

            except Exception as e:
                print(f"Error processing canvas {i}: {str(e)}")
        else:
            print("Error: Could not find a non-empty canvas element.")
            
        return data



    def main_process(self, date_text : str):
        
        # apply filter 
        apply = self.wait_watch_grab(xpath="//button[@class='btn btn--primary btn--small']")
        apply.click()
        time.sleep(2)
        
        pdf_file_pths = []
        
        if self.is_table_present(self.driver,xpath=self.table_xpath):
            

            # Locate the table rows containing data
            data_row_elements = self.driver.find_elements(By.XPATH, "//div[@class='roller-grid ng-scope dx-widget dx-visibility-change-handler']//tr[contains(@class, 'dx-data-row')]")

            # Print XPaths of individual rows
            row_xpaths = []
            for i, row in enumerate(data_row_elements, start=1):
                # Generate XPath for each row
                row_xpath = f"//div[@class='roller-grid ng-scope dx-widget dx-visibility-change-handler']//tr[contains(@class, 'dx-data-row')][{i}]"
                row_xpaths.append(row_xpath)
                
            # Now iterate through each of the xpaths 
            # Iterate through each of the xpaths
            for row_xpath in row_xpaths:
                # Wait for the row to be present
                row_obj = self.wait_watch_grab(xpath=row_xpath)
                
                # Scroll the row into view
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", row_obj)
                time.sleep(2)  # Allow time for scrolling animation if needed

                
                try:

                    user_data = self.get_user_data(row_xpath=row_xpath)
                    
                    pdf = get_pdf(data=user_data)
                    pdf.page_mode = "FULL_SCREEN"

                    # get the pdf name
                    b_id = user_data["booking_id"]
                    pdf_name = "_".join([x.lower().capitalize() for x in user_data["name"].split()]) + f"_{b_id}" + ".pdf"

                    # check if 
                    Path("src/membership/PDFs").mkdir(parents=True,exist_ok=True)


                    # set the file path
                    pdf_path = Path("src/membership/PDFs").joinpath(pdf_name)

                    # check if the file exists, and delete if it does
                    if pdf_path.exists():
                        pdf_path.unlink()  # delete the existing file

                    pdf.output(str(Path("src/membership/PDFs").joinpath(pdf_name)))
                    
                    pdf_file_pths.append(pdf_name)
                    
                except Exception as e: 
                    
                    print(f"Something happened : {e}")
                            
                            
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
                
            return pdf_file_pths

        else: 
            return False

    def iterate_through_dates(self): 

        
        date = ""
        while date != "27 Sep 2024": 
              
            
            date_text_elem = self.wait_watch_grab(xpath="//input[@placeholder='Select date(s)']")
            date_text = date_text_elem.get_attribute("value")
            
            if date_text in  ["Today", "Yesterday"]: 
                if date_text == "Today":
                    today = datetime.now()
                    date_text = str(today.strftime('%d %b %Y'))
                    
                else: 
                    today = datetime.now()
                    yesterday = today - timedelta(days=1)
                    date_text = str(yesterday.strftime('%d %b %Y'))
                    
            
            if not logger.is_date_in_df(date=date_text):
                # this will work for all of PDFS in page
                status = self.main_process(date_text=date_text)
                
                if status:
                    logger.push_row(date=date_text,processed=True, is_empty=False)
                    
                    ######################## Push to Drive ######################
                    if self.gdrive_folder_id:
                        
                        uploader = GoogleDriveUploader(parent_folder_id=self.gdrive_folder_id)
                        for file in status: 
                            full_pth = Path("src/membership/PDFs").joinpath(file)
                            uploader.upload_pdf(file_path=str(full_pth))
                             
                        logger.mark_pushed_to_drive(date=date_text)
                        print(f"Sucess: All PDFs pushed to drive for :{date_text}" )
                                       
                        
                else: 
                    logger.push_row(date=date_text,processed=False, is_empty=True)

            else:
                row_status = logger.get_row_stats(date=date_text) 
                if row_status[1] == False:
                    print(f"There is no any data for {date_text}. Skipping the date.")
                
                else:
                    print(f"The data has been already saved for {date_text}. Skipping the date" )

             
            date = str(date_text)
            prev_page = self.wait_watch_grab(xpath="//span[normalize-space()='keyboard_arrow_left']")
            prev_page.click()
            
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
   
   



def main(debug, gdrive_folder_id, venue: Literal["london", "oakville"]):
    bot = MembershipBot(debug=debug, gdrive_folder_id=gdrive_folder_id)
    bot.login_to_roller()
    bot.handle_popup(driver=bot.driver)
    if venue == "london":
        bot.switch_venue(venue=venue)
    bot.booking_config()
    bot.iterate_through_dates()

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Run the MembershipBot with specified configurations.")
    
    parser.add_argument('--debug', action='store_true', help="Enable debug mode")  # Flag for debug
    parser.add_argument('--gdrive_folder_id', type=str, required=True, help="Google Drive folder ID")  # Google Drive folder ID
    parser.add_argument('--venue', type=str, choices=["london", "oakville"], default="oakville", help="Venue location")  # Venue

    # Parse the arguments
    args = parser.parse_args()

    # Call main function with parsed arguments
    main(debug=args.debug, gdrive_folder_id=args.gdrive_folder_id, venue=args.venue)
