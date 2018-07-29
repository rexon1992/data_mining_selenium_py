from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import itertools as it

driver = webdriver.Chrome()
driver.get("https://www.climatechangecommunication.org/climate-change-opinion-map/")

# switch to iframe
WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@src = 'https://environment.yale.edu/ycom/factsheets/MapPage/2017Rev/?est=happening&type=value&geo=county']")))

def alt_apend(old_list):
    list_1=old_list[2:len(old_list):5]
    list_2=old_list[4:len(old_list):5]
    new_list=[None]*(len(list_1)+len(list_2))
    new_list[::2]=list_1
    new_list[1::2]=list_2
    return(new_list)

# select options and download data

congressional_dist=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='cd']")))
congressional_dist.click()

names=WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='document']/div[*]//*[@class='name']")))
labels=WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='document']/div[*]//*[@class='label']")))

columns=[]

for n in range(1,len(names)):
    no=(names[n].text+"_"+labels[(n*2)].text)
    yes=(names[n].text+"_"+labels[(n*2)+1].text)
    columns.append(no)
    columns.append(yes)

loc=['State']+['CD']+columns
data=pd.DataFrame()

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

        list_data_beliefs=raw_data[2].text.split("\n")
        list_data_risk=raw_data[3].text.split("\n")
        list_data_policy=raw_data[4].text.split("\n")
        list_data_behavior=raw_data[5].text.split("\n")

        beliefs=alt_apend(list_data_beliefs)
        risk=alt_apend(list_data_risk)
        policy=alt_apend(list_data_policy)
        behavior=alt_apend(list_data_behavior)

        region=[state[s],cd[c]]
        temp=list(it.chain(region, beliefs,risk,policy,behavior))
        temp=pd.DataFrame(temp)
        temp=pd.DataFrame.transpose(temp)
        data=pd.concat([data,temp])

        print(list_data_behavior)

data.columns=loc[0:len(loc)-1]
data.to_csv("map_data.csv")


# switch back to default content
driver.switch_to.default_content()