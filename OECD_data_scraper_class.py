from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains


class OECD_data_scaper:

    def __init__(self, visible = False):
        self.visible = visible
        
        options = Options()
        if self.visible:
            options.add_argument('--headless')
        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.download.folderList', 2) # custom location
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.download.dir', '/home/jens/Documents_Ubuntu/')
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
        
        self.driver = webdriver.Firefox(firefox_profile=profile, options=options)
        self.driver.get("https://stats.oecd.org/")

        begin = self.driver.find_element_by_id("browsethemes")
        self.begin = begin.text.split('\n')
        self.dependence_tree = {}

    def tree_disolver(self, parent = 0, highest_level_names = -1):
        if highest_level_names == -1:
            highest_level_names = self.begin
        if len(highest_level_names) != 0:
            for name in highest_level_names:
                name = name.replace("&nbsp;", "\u00a0")
                parent_click = self.driver.find_elements_by_xpath('//li[contains(@class ,"t closed") and span[text()="{}"]]'.format(name))
                if len(parent_click) == 1:
                    parent_click = parent_click[0]
                    parent_click.click()
                else:
                    for item in parent_click:
                        if item.is_displayed():
                            item.click()
                increase_depth = self.driver.find_elements_by_xpath('//li[contains(@class ,"t opened") and span[text()="{}"]]/ul/li/span'.format(name))
                if name in [e.get_attribute("innerHTML") for e in increase_depth]:
                    double_increase_depth = self.driver.find_elements_by_xpath('//li[contains(@class ,"t opened") and span[text()="{}"]]/ul/li/span[text()="{}"]/ul/li/span'.format(name, name))
                    self.tree_disolver(name, [e.get_attribute("innerHTML") for e in double_increase_depth])
                    parent_click = self.driver.find_elements_by_xpath('//li[contains(@class ,"t opened") and span[text()="{}"]]/ul/li/span[text()="{}"]'.format(name, name))
                    if len(parent_click) == 1:
                        parent_click = parent_click[0]
                        parent_click.click()
                    else:
                        for item in parent_click:
                            if item.isDisplayed():
                                item.click()
                else:
                    self.tree_disolver(name, [e.get_attribute("innerHTML") for e in increase_depth])

    def download_clicker(self, download_section):
        ds_elements = self.driver.find_elements_by_xpath('//li[span[text() = "{}"]]//a[contains(@class ,"ds")]'.format(download_section))
        for e_ds in ds_elements:
            e_ds.click()
            try:
                Export_Button = WebDriverWait(self.driver, 40).until(EC.element_to_be_clickable((By.ID, 'export-icon')))
                Export_Button.click()
            except:
                print('Timeout while determining position of export button.')
            try:
                csv_button = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[span[@id='export-csv-icon']]")))
                csv_button.click()
                csv_button.click()
            except:
                print('Timeout while determining position of csv category.')
            try:
                iframe_choice = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//iframe[@id="DialogFrame"]')))
                self.driver.switch_to.frame(iframe_choice)
                download = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@id = "_ctl12_btnExportCSV"]')))
                ActionChains(self.driver).click(download).perform()
                self.driver.switch_to.default_content()
            except:
                print('Timeout while determining position of download button.')
            try:
                close = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//span[contains(@class,"ui-icon ui-icon-closethick")]')))
                close.click()
            except:
                print('Timeout while determining position of exit button.')