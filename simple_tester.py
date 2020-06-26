from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time


#options = Options()
#options.add_argument('--headless')

#driver = webdriver.Firefox(options = options)
profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2) # custom location
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', '/home/jens/Documents_Ubuntu/')
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

driver = webdriver.Firefox(profile)
driver.get("https://stats.oecd.org/")

begin = driver.find_element_by_id("browsethemes")
begin = begin.text.split('\n')


def tree_disolver(highest_level_names = begin):  
    if len(highest_level_names) != 0:
        for name in highest_level_names:
            name = name.replace("&nbsp;", "\u00a0")
            print('parent text {}'.format(name))
            parent_click = driver.find_elements_by_xpath('//li[contains(@class ,"t closed") and span[text()="{}"]]'.format(name))
            if len(parent_click) == 1:
                parent_click = parent_click[0]
                parent_click.click()
            else:
                for item in parent_click:
                    if item.is_displayed():
                        item.click()
            increase_depth = driver.find_elements_by_xpath('//li[contains(@class ,"t opened") and span[text()="{}"]]/ul/li/span'.format(name))
            if name in [e.get_attribute("innerHTML") for e in increase_depth]:
                double_increase_depth = driver.find_elements_by_xpath('//li[contains(@class ,"t opened") and span[text()="{}"]]/ul/li/span[text()="{}"]/ul/li/span'.format(name, name))
                tree_disolver([e.get_attribute("innerHTML") for e in double_increase_depth])
                parent_click = driver.find_elements_by_xpath('//li[contains(@class ,"t opened") and span[text()="{}"]]/ul/li/span[text()="{}"]'.format(name, name))
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
    ds_elements = driver.find_elements_by_xpath('//li[span[text() = "{}"]]//a[contains(@class ,"ds")]'.format(download_section))
#    q_elements = driver.find_elements_by_xpath('//li[span[text() = "{}"]]//a[contains(@class ,"q")]'.format(download_section))
    for e_ds in ds_elements:
        e_ds.click()
##            time.sleep(5)
#        except:
#            pass
#    for e_q in q_elements:
##        try:
#        e_q.click()
#            try:
        Export_Button = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.ID, 'export-icon')))
        Export_Button.click()
        print('first')
        csv_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[span[@id='export-csv-icon']]")))
        csv_button.click()
        csv_button.click()
        print('second')
        iframe_choice = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//iframe[@id="DialogFrame"]')))
        driver.switch_to.frame(iframe_choice)
        download = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@id = "_ctl12_btnExportCSV"]')))
        ActionChains(driver).click(download).perform()
        driver.switch_to.default_content()
        close = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//span[contains(@class,"ui-icon ui-icon-closethick")]')))
        close.click()
        print("Download!")
#            except:
#                print("Loading took too much time!")
#                time.sleep(5)    
#                driver.quit()
            
#        except:
#            pass
            
tree_disolver(['Environment'])
#download_clicker('LFS by sex and age')

#driver.quit()