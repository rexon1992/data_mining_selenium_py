from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

chrome=webdriver.Chrome()
chrome.get('https://www.greenclimate.fund/countries')
country_elements=chrome.find_elements_by_xpath("*//div[@class='country-directory']")
countries=country_elements[0].text.split('\n')

chrome.get("https://www.greenclimate.fund/countries/-/country-profiles/afghanistan")

data=pd.DataFrame()

def list2df(list):
    list = pd.DataFrame(list)
    list = pd.DataFrame.transpose(list)
    return (list)

def scrape_info():
    try:
        country_name = chrome.find_element_by_xpath("*//span[@class='name']").text
    except NoSuchElementException:
        try:
            country_name = chrome.find_element_by_xpath("*//span[@class='name long']").text
        except NoSuchElementException:
            country_name='NA'
            print(country + ': country name not Found')

    try:
        country_section_title = chrome.find_element_by_xpath("*//div[@class='country__section-title']/h2").text
    except NoSuchElementException:
        country_section_title='NA'
        print(country+': country_section_title not Found')

    try:
        organization = chrome.find_element_by_xpath("*//div[@class='contact__title']").text
    except NoSuchElementException:
        organization='NA'
        print(country + ': organization not Found')

    try:
        name = chrome.find_element_by_xpath("*//div[@class='contact__strong']").text
    except NoSuchElementException:
        name='NA'
        print(country + ': name not Found')

    try:
        designation = chrome.find_element_by_xpath("*//div[@class='contact__item']").text
    except NoSuchElementException:
        designation='NA'
        print(country + ': designation not Found')

    try:
        email = chrome.find_element_by_xpath("//*[name()='canvas']").get_attribute('data-egmraeieln') + "@" + chrome.find_element_by_xpath("//*[name()='canvas']").get_attribute('data-dfoumnadifnu')
    except NoSuchElementException:
        email='NA'
        print(country + ': email not Found')

    try:
        telephone = chrome.find_element_by_xpath("*//span[@class='contact__item']").text
    except NoSuchElementException:
        telephone='NA'
        print(country + ': telephone not Found')

    try:
        address = ', '.join(chrome.find_element_by_xpath("*//span[@class='contact__item span8']").text.split('\n'))
    except NoSuchElementException:
        address='NA'
        print(country + ': address not Found')

    info=[country_name,country_section_title,organization,name,designation,email,telephone,address]

    return info

for country in countries:
    if(len(country)>1):
        WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='selectize-input items full has-options has-items']"))).click()
        WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='selectize-input items full has-options has-items focus input-active dropdown-active']/input[@type='text']"))).send_keys(u'\ue003')
        WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='selectize-input items has-options focus input-active dropdown-active not-full']/input[@type='text']"))).send_keys(country)
        WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='selectize-dropdown single select-selectize']"))).click()
        info = scrape_info()
        info_df = list2df(info)
        data = pd.concat([data, info_df])

data.columns=['Country','Country Section', 'Ministry_OR_Agency','Name','Designation','Email','Telephone','Address']
data.to_csv('GCF_focal_points.csv',encoding='utf-8-sig',index=False)






























