from selenium import webdriver
import pandas as pd

chrome=webdriver.Chrome()
chrome.get("http://www.thegef.org/council_members_alternates")

def join_elements_country_data(indices,data_set):
    string=''
    for index in indices:
        string=string+", "+data_set[index]
    return string[2:]

def list2df(list):
    list = pd.DataFrame(list)
    list = pd.DataFrame.transpose(list)
    return (list)

def scrape_info_member(data_set,type):
    name = data_set[0]

    try:
        designation = data_set[1]
    except (IndexError, ValueError):
        designation = 'NA'
        print(constituency_elements[ind].text + ': designation not found')

    try:
        tel_index = [i for i, x in enumerate(data_set) if 'Tel' in x]
        telephone = data_set[tel_index[0]]
    except IndexError:
        telephone = 'NA'
        print(constituency_elements[ind].text + ': telephone not found')

    try:
        fax_index = [i for i, x in enumerate(data_set) if 'Fax' in x]
        fax = data_set[fax_index[0]]
    except IndexError:
        fax = 'NA'
        print(constituency_elements[ind].text + ': fax not found')
    try:
        email_index = [i for i, x in enumerate(data_set) if 'Email' in x]
        email = data_set[email_index[0]]
    except IndexError:
        email = 'NA'
        print(constituency_elements[ind].text + ': email not found')
    try:
        tel_index = [i for i, x in enumerate(data_set) if 'Tel' in x]
        address = join_elements_country_data(range(2, (tel_index[0])), data_set)
    except (IndexError, ValueError):
        address = 'NA'
        print(constituency_elements[ind].text + ': address not found')
    try:
        app_index = [i for i, x in enumerate(data_set) if 'Appointment' in x]
        app = data_set[app_index[0]]
    except IndexError:
        app = 'NA'
        print(constituency_elements[ind].text + ': do_app not found')

    info = [constituency,type,name, designation, address, telephone, fax, email,app]
    return(info)

data=pd.DataFrame()

constituency_elements=chrome.find_elements_by_xpath("*//tbody/tr/td[@data-th='Constituency']")
council_member_elements=chrome.find_elements_by_xpath("*//tbody/tr/td[@data-th='Council Member']")
alternate_elements=chrome.find_elements_by_xpath("*//tbody/tr/td[@data-th='Alternate']")

for ind in range(0,len(constituency_elements)):
    constituency=constituency_elements[ind].text

    council_member_data=council_member_elements[ind].text.split('\n')
    council_member_info=scrape_info_member(council_member_data,'Council Member')
    cm_info=list2df(council_member_info)
    data=pd.concat([data,cm_info])

    alternate_data=alternate_elements[ind].text.split('\n')
    alternate_member_info=scrape_info_member(alternate_data,'Alternate Contact')
    alt_info=list2df(alternate_member_info)
    data=pd.concat([data,alt_info])

data.columns=['Constituency','Type of Contact','Name','Designation','Address','Telephone','Fax','Email','Date of Appointment']

data.to_csv('GEF_council.csv',encoding='utf-8-sig',index= False)