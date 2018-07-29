from selenium import webdriver
import pandas as pd

chrome=webdriver.Chrome()
chrome.get("https://www.adaptation-fund.org/apply-funding/designated-authorities/")

def find_index(value):
    return[i for i, x in enumerate(countries) if x==value]

def join_elements_country_data(indices,data_set):
    string=''
    for index in indices:
        string=string+", "+data_set[index]
    return string[2:]

def list2df(list):
    list = pd.DataFrame(list)
    list = pd.DataFrame.transpose(list)
    return (list)

def scrape_info_member(data_set):

    try:
        tel_index = [i for i, x in enumerate(data_set) if 'Tel' in x]
        telephone = data_set[tel_index[0]]
    except IndexError:
        telephone = 'NA'
        print(countries[ind] + ': telephone not found')

    try:
        fax_index = [i for i, x in enumerate(data_set) if 'Fax' in x]
        fax = data_set[fax_index[0]]
    except IndexError:
        fax = 'NA'
        print(countries[ind] + ': fax not found')

    try:
        email_index = [i for i, x in enumerate(data_set) if 'Email' in x]
        email = data_set[email_index[0]]
    except IndexError:
        email = 'NA'
        print(countries[ind] + ': email not found')

    if len(find_index(data_set[0]))>=1:
        country=data_set[0]
        name=data_set[1]

        try:
            designation = data_set[2]
        except (IndexError, ValueError):
            designation = 'NA'
            print(countries[ind] + ': designation not found')

        try:
            tel_index = [i for i, x in enumerate(data_set) if 'Tel' in x]
            address = join_elements_country_data(range(3, (tel_index[0])), data_set)
        except (IndexError, ValueError):
            address = 'NA'
            print(countries[ind] + ': address not found')

    else:
        country='NA'
        name=data_set[0]
        try:
            designation = data_set[1]
        except (IndexError, ValueError):
            designation = 'NA'
            print(countries[ind] + ': designation not found')

        try:
            tel_index = [i for i, x in enumerate(data_set) if 'Tel' in x]
            address = join_elements_country_data(range(2, (tel_index[0])), data_set)
        except (IndexError, ValueError):
            address = 'NA'
            print(countries[ind] + ': address not found')

    info = [country, name, designation, address, telephone, fax, email]
    return(info)

data=pd.DataFrame()

all_countries_data=chrome.find_elements_by_xpath("*//div[@class='post-content']/p")[7:]

countries_elements=chrome.find_elements_by_xpath("*//div[@class='post-content']/p/strong")
countries=[element.text for element in countries_elements]

for ind in range(0,len(all_countries_data)):
    country_data=all_countries_data[ind].text.split('\n')
    info=scrape_info_member(country_data)
    info_df=list2df(info)

    data=pd.concat([data,info_df])

data.columns=['Country','Name','Designation','Address','Telephone','Fax','Email']
data.to_csv('Adp_fund.csv',encoding='utf-8-sig',index= False)

data.to_csv('Adp_fund_py3.6.csv',index= False)