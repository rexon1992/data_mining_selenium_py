from selenium import webdriver
import pandas as pd

chrome=webdriver.Chrome()
chrome.get("https://www.thegef.org/focal_points_list")

def find_index(value):
    return[i for i, x in enumerate(list_all_elements) if x==value]

def match(list_1,list_2):
    return[i for i, x in enumerate(list_1) if x in list_2]

def join_elements_country_data(indices,data_set):
    string=''
    for index in indices:
        string=string+", "+data_set[index]
    return string[2:]


def scrape_info(data_set):
    country = data_set[0]
    name = data_set[1]

    fp_index = [i for i, x in enumerate(data_set) if 'Focal Point' in x]
    status = join_elements_country_data(fp_index,data_set)

    designation = data_set[max(fp_index) + 1]

    tel_index = [i for i, x in enumerate(data_set) if 'Tel' in x]
    telephone = data_set[tel_index[0]]
    try:
        fax_index = [i for i, x in enumerate(data_set) if 'Fax' in x]
        fax = data_set[fax_index[0]]
    except IndexError:
        fax = 'NA'
    email_index = [i for i, x in enumerate(data_set) if 'Email' in x]
    email = data_set[email_index[0]]
    address = join_elements_country_data(range((max(fp_index) + 2), (tel_index[0])),data_set)
    info = [country, name, status, designation, address, telephone, fax, email]
    return(info)

def scrape_info_multiple(data_set):
    name = data_set[0]

    try:
        fp_index = [i for i, x in enumerate(data_set) if 'Focal Point' in x]
        status = join_elements_country_data(fp_index, data_set)
    except IndexError:
        status='NA'
        print(list_countries[c]+': status not found')

    try:
        fp_index = [i for i, x in enumerate(data_set) if 'Focal Point' in x]
        designation = data_set[max(fp_index) + 1]
    except (IndexError, ValueError):
        designation = 'NA'
        print(list_countries[c] + ': designation not found')

    try:
        tel_index = [i for i, x in enumerate(data_set) if 'Tel' in x]
        telephone = data_set[tel_index[0]]
    except IndexError:
        telephone = 'NA'
        print(list_countries[c] + ': telephone not found')

    try:
        fax_index = [i for i, x in enumerate(data_set) if 'Fax' in x]
        fax = data_set[fax_index[0]]
    except IndexError:
        fax = 'NA'
        print(list_countries[c] + ': fax not found')
    try:
        email_index = [i for i, x in enumerate(data_set) if 'Email' in x]
        email = data_set[email_index[0]]
    except IndexError:
        email = 'NA'
        print(list_countries[c] + ': email not found')

    try:
        fp_index = [i for i, x in enumerate(data_set) if 'Focal Point' in x]
        tel_index = [i for i, x in enumerate(data_set) if 'Tel' in x]
        address = join_elements_country_data(range((max(fp_index) + 2), (tel_index[0])), data_set)
    except (IndexError, ValueError):
        address = 'NA'
        print(list_countries[c] + ': address not found')

    info = [list_countries[c], name, status, designation, address, telephone, fax, email]
    return(info)

def list2df(list):
    list = pd.DataFrame(list)
    list = pd.DataFrame.transpose(list)
    return (list)

data=pd.DataFrame()
countries_elements=chrome.find_elements_by_xpath("*//h2")
names_elements=chrome.find_elements_by_xpath("*//h4")
all_elements=chrome.find_element_by_class_name("focal-point-country-wrapper")


list_countries=[element.text for element in countries_elements]
list_names=[element.text for element in names_elements]
list_all_elements=all_elements.text.split("\n")


for c in range(0,len(list_countries)):

    if c<len(list_countries)-1:
        country_data = list_all_elements[min(find_index(list_countries[c])):min(find_index(list_countries[c + 1]))]
    if c==len(list_countries)-1:
        country_data=list_all_elements[min(find_index(list_countries[c])):]

    number_of_contacts=len(match(country_data,list_names))

    if number_of_contacts==1:
        info=scrape_info(country_data)
        info=list2df(info)
        data=pd.concat([data,info])
    else:
        index_of_names=match(country_data,list_names)

        for i in range(0,len(index_of_names)):
            if i<len(index_of_names)-1:
                country_data_person = country_data[index_of_names[i]:index_of_names[i + 1]]

                info = scrape_info_multiple(country_data_person)
                info = list2df(info)
                data = pd.concat([data, info])


            if i==len(index_of_names)-1:
                country_data_person = country_data[index_of_names[i]:]

                info = scrape_info_multiple(country_data_person)
                info = list2df(info)
                data = pd.concat([data, info])

data.columns=['Country','Name','Status','Designation','Address','Telephone','Fax','Email']
data.to_csv("GEF_Focal_Points.csv", encoding='utf-8-sig',index= False)

