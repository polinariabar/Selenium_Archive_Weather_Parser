import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains


class GoogleChromeDriver:

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.file_download_driver = webdriver.Chrome(ChromeDriverManager().install())

    def fill_in_station(self, station_id):
        self.driver.get(url="https://rp5.ru/Weather_archive_in_Gorki_Leninskiye")
        station = self.driver.find_element_by_id("wmo_id")
        js_str = "arguments[0].setAttribute('value','" + str(station_id) + "');"
        self.driver.execute_script(js_str, station)
        action_chains = ActionChains(self.driver)
        action_chains.double_click(station).perform()
        action_chains.double_click(station).perform()

    def choose_station(self):
        self.driver.find_element_by_class_name('ac_results').get_attribute('innerHTML')
        list_vars = self.driver.find_element_by_class_name('ac_results')
        variant = list_vars.find_element_by_class_name('ac_even')
        variant.click()

    def change_start_date(self, str_date):
        date = self.driver.find_element_by_id("calender_dload")
        self.change_date(date, str_date)

    def change_end_date(self, str_date):
        date = self.driver.find_element_by_id("calender_dload2")
        self.change_date(date, str_date)

    def change_date(self, date, str_date):
        js_str = "arguments[0].setAttribute('value','" + str_date + "');"
        self.driver.execute_script(js_str, date)
        self.driver.execute_script("arguments[0].setAttribute('onChange','');", date)
        time.sleep(1)

    def create_archive(self):
        row = self.driver.find_element_by_class_name('menu-row2')
        elem = row.find_element_by_class_name('archButton')
        self.driver.execute_script("arguments[0].click();", elem)

    def download_archive(self):
        dwnld_href = self.driver.find_element_by_id("f_result").find_element_by_tag_name("a").get_attribute('href')
        self.file_download_driver.get(dwnld_href)
        return dwnld_href.split('/')[-1]
