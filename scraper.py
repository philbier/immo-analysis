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

def scroll_to_end(driver):
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def get_last_page(driver):
    header = driver.find_element_by_css_selector("div.iw_content > h1")
    return math.ceil(int(header.text.split()[0])/20)

def get_net_rent(driver, expose_link):
    #net_rent = driver.find_element_by_css_selector("#divPreise div.datarow:nth-child(1) > div.datacontent.iw_right > strong").text
    net_rent = driver.find_element_by_css_selector("#divPreise > div > div > div.section_wrapper.iw_left > div:nth-child(2) > div.section_content.iw_right > div > div:nth-child(1) > div.datalabel.iw_left").text
    print(net_rent)
    
    return net_rent

def get_expose_data(driver, expose_link):
    driver.get(expose_link)
    title = driver.find_element_by_css_selector("div.quickfacts > h1").text
    location = driver.find_element_by_css_selector("div.quickfacts > .location > span").text

    net_rent = get_net_rent(driver, expose_link)
    
    full_rent = driver.find_element_by_css_selector("div.section.preise div.datarow:last-child div.datacontent").text
    full_rent = clean_point(full_rent)

    space = driver.find_element_by_css_selector("div.quickfacts > div.hardfacts > div.hardfact:nth-child(2)").text
    space = get_first_element(space)

    rooms = driver.find_element_by_css_selector("div.quickfacts > div.hardfacts > div.hardfact.rooms").text
    rooms = clean_rooms(rooms)
    return [title, location, net_rent, full_rent, space, rooms]

def delete_projects(lst):
    regex = re.compile(r'https://www.immowelt.de/projekte/')
    return [x for x in lst if not regex.match(x)]

def clean_point(lst):
    lst = get_first_element(lst)
    return ''.join(s for s in lst if s != "." )

def get_first_element(lst):
    lst = [s for s in lst.split()][0]
    return lst
    
def clean_rooms(lst):
    lst = [s for s in lst.split("\n")][0]
    return lst
    
if __name__ == '__main__':
    driver = create_driver()
    #preload first page to get last page
    driver.get(url+str(start_page))

    try:
        for i in range(start_page, 1+1):
            print("Processing page: " + str(i))
            if i == start_page:
                close_shadow_root(driver)
            else:
                #open url with pagenumber i
                driver.get(url+str(i))
            scroll_to_end(driver)
            
            #get every exposé-Link on current page
            exposes = driver.find_elements_by_css_selector("div.listitem > a")
            for element in exposes:
                expose_links.append(element.get_attribute('href'))
    except Exception as e:
        print("Exception while processing (pages): " + str(e))
        pass

    #delete projects from list
    expose_links = delete_projects(expose_links)

    try:
        columns = ['title', 'location', 'net_rent', 'full_rent', 'space', 'rooms', 'link']
        df = pd.DataFrame([], columns=columns)
        for index, link in enumerate(expose_links):
            print("Processing expose: " + link)
            expose_data = get_expose_data(driver, link)
            expose_data.append(link)
            df_tmp = pd.DataFrame([expose_data], columns=columns)
            df = df.append(df_tmp, ignore_index = True)
            if index == 1:
                break
    except Exception as e:
        print("Exception while processing (exposes): " + str(e))
        pass



    print(df)

    #driver.close()
