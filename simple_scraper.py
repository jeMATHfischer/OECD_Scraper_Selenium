from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

file_path = '/home/jens/Documents_Ubuntu/'

options = Options()
options.add_argument('--headless')   #remove comment to let it run in the background
profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2) 
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', file_path)
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

driver = webdriver.Firefox(firefox_profile=profile, options=options)
driver.get("https://stats.oecd.org/")

begin = driver.find_element_by_id("browsethemes")
begin = begin.text.split('\n')

def tree_disolver(highest_level_names = begin): 
    '''
    -> This function runs through the whole tree starting from a highest given level.
    
    -> Highest given level has to be visible after driver loards page. 
    
    -> Highest_level_names has to contain elements in begin. Has to be given as a single list.
    '''
    if len(highest_level_names) != 0:
        for name in highest_level_names:
            # replace html formating to python interpretable.
            name = name.replace("&nbsp;", "\u00a0")
            single_path_closed = '//li[contains(@class ,"t closed") and span[text()="{}"]]'.format(name)
            single_path_opened = '//li[contains(@class ,"t opened") and span[text()="{}"]]'.format(name)
            parent_click = driver.find_elements_by_xpath(single_path_closed)
            if len(parent_click) == 1:
                parent_click = parent_click[0]
                parent_click.click()
            else:
                for item in parent_click:
                    if item.is_displayed():
                        item.click()
            increase_depth = driver.find_elements_by_xpath(single_path_opened + '/ul/li/span')
            if name in [e.get_attribute("innerHTML") for e in increase_depth]:
                # Difficulties arise if parent has child with same name parent_name.
                # The branch parent_name - parent_name has to be evaluated taking two steps.
                parent_click = driver.find_elements_by_xpath(single_path_closed)
                double_path = '//li[contains(@class ,"t closed") and span[text()="{}"]]/ul/li/span[text()="{}"]'.format(name, name)
                double_increase_depth = driver.find_elements_by_xpath(double_path + '/ul/li/span')
                tree_disolver([e.get_attribute("innerHTML") for e in double_increase_depth])
                if len(parent_click) == 1:
                    parent_click = parent_click[0]
                    parent_click.click()
                else:
                    for item in parent_click:
                        if item.isDisplayed():
                            item.click()
            else:
                tree_disolver([e.get_attribute("innerHTML") for e in increase_depth])

def download_clicker(download_section):
    '''
    -> Navigates through open tree sections to the download dialog window.
    
    -> Applies to all full data sets in the given download section. 
    
    ->The download_section has to be visible and all sublevels need to be unfolded.
    
    -> Use only after tree_disolver.
    '''
    ds_xpath = '//li[span[text() = "{}"]]//a[contains(@class ,"ds")]'.format(download_section)
    ds_elements = driver.find_elements_by_xpath(ds_xpath)
    for e_ds in ds_elements:
        e_ds.click()
        try:
            Export_Button = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.ID, 'export-icon')))
            Export_Button.click()
        except:
            print('Timeout while determining position of export button.')
        try:
            csv_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[span[@id='export-csv-icon']]")))
            csv_button.click()
            csv_button.click()
        except:
            print('Timeout while determining position of csv category.')
        try:
            iframe_choice = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//iframe[@id="DialogFrame"]')))
            driver.switch_to.frame(iframe_choice)
            download = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@id = "_ctl12_btnExportCSV"]')))
            ActionChains(driver).click(download).perform()
            driver.switch_to.default_content()
        except:
            print('Timeout while determining position of download button.')
        try:
            close = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//span[contains(@class,"ui-icon ui-icon-closethick")]')))
            close.click()
        except:
            print('Timeout while determining position of exit button.')
            
tree_disolver(['Labour', 'Globalisation'])
#download_clicker('Africapolis')

time.sleep(10)
driver.quit()