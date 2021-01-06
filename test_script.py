from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import math
import numbers
import pandas as pd
import re

url = "https://www.immowelt.de/liste/berlin/wohnungen/mieten?sort=relevanz&cp="
start_page = 1
expose_links=[]
SCROLL_PAUSE_TIME = 1

def create_driver():
    options = Options()
    options.headless = False
    print("Driver created")
    return webdriver.Chrome(options=options, executable_path="C:\ChromeDriver\chromedriver.exe")

def expand_shadow_element(element):
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
    print("Shadow root expanded")
    return shadow_root

def close_shadow_root(driver):
    try:
        #shadow root container has built up time
        time.sleep(5)

        #find shadow root container
        root = driver.find_element_by_id('usercentrics-root')
        shadow_root = expand_shadow_element(root)

        #find and click"OK" button
        button = shadow_root.find_element_by_css_selector("button[data-testid='uc-accept-all-button']")
        button.click()
        print("Shadow root closed")
    except Exception as e:
        print("Exception in 'close_shadow_root': "+str(e))
        pass

def get_net_rent(driver):
    driver.get("https://www.immowelt.de/expose/2xx6s4s")

    re_net_rent = re.compile(r'Kaltmiete')
    re_add_cost = re.compile(r'Nebenkosten')
    re_heat_cost = re.compile(r'Heizkosten')

    #net_rent = driver.find_element_by_css_selector("#divPreise div.datarow:nth-child(1) > div.datacontent.iw_right > strong").text

    num_rows_pricetable = len(driver.find_elements_by_css_selector("#divPreise div.datarow"))

    for i in range(1, num_rows_pricetable+1):
        selector = "#divPreise div.datatable > div.datarow:nth-child("+ str(i) +") > div.datalabel"
        element_text = driver.find_element_by_css_selector(selector).text

        if re_net_rent.match(element_text):
            print("Kaltmiete in :" + str(i))

        if re_add_cost.match(element_text):
            print("Nebenkosten in :" + str(i))

        if re_heat_cost.match(element_text):
            print("Heizkosten in :" + str(i))
   
if __name__ == '__main__':
    driver = create_driver()
    driver.get(url+str(start_page))
    
    close_shadow_root(driver)

    get_net_rent(driver)

    driver.close()