from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import xml.etree.cElementTree as ET

driver = webdriver.Chrome()
driver.get("https://www.climatechangecommunication.org/climate-change-opinion-map/")

# switch to iframe
WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@src = 'https://environment.yale.edu/ycom/factsheets/MapPage/2017Rev/?est=happening&type=value&geo=county']")))

# select options and download data

congressional_dist=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='cd']")))
congressional_dist.click()

state_string=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='stateSelect']")))
state=state_string.text.split("\n")

#select states


for s in range(1,len(state)):
    select_state = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='stateSelect']/option[text()='"+state[s]+"']")))
    select_state.click()
    cd_string=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='cdSelect']")))
    cd=cd_string.text.split("\n")

    #select counties
    for c in range (1,len(cd)):
        select_cd=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='cdSelect']/option[text()='"+cd[c]+"']")))
        select_cd.click()

        #scrape data
        raw_data = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='document']/div[*]//*[name()='svg']")))



        print(raw_data [1].text)

# switch back to default content
driver.switch_to.default_content()

USA=ET.Element("USA")
state=ET.SubElement(USA, "State")
county=ET.SubElement(state,"county")
question=ET.SubElement(county,"Q1")

ET.SubElement(question,"Global warming is happening",name="Yes").text="50"
ET.SubElement(question,"Global warming is happening",name="No").text="5"

tree=ET.ElementTree(USA)
tree.write("sample.xml")