'''
Getting access to current ALAC tutors
'''
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 09:50:52 2021

@author: shahva
"""

import bs4
import requests
from bs4 import BeautifulSoup as bs
import json

def get_html():
    url = "https://info.rpi.edu/advising-learning-assistance/learning-assistance"
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    page = requests.get(url, headers=agent)
    soup = bs(page.content, 'html.parser')
    ALAC = soup.body.find(id="page").find(id='section-content').find(id="zone-content-wrapper").find(id ="zone-content")\
    .find(id="region-content").find(class_="region-inner region-content-inner").find(id="block-system-main")\
    .find(class_ ="block-inner clearfix").find(class_="content clearfix").find(id="node-page-34379")\
    .find(class_="content clearfix").find(class_="field-collection-container clearfix").find(class_="field field-name-field-building-block field-type-field-collection field-label-hidden")\
    .find(class_="field-items").find(class_="field-item even").find(class_="field-collection-view clearfix view-mode-full")\
    .find(class_="content").find(class_="field field-name-field-text field-type-text-long field-label-hidden")\
    .find(class_="field-item even").find(class_="Table")
    return ALAC

def get_ALAC_tutor():
    ALAC = get_html()
    dictionary = dict()
    for tutor in ALAC.findAll('tr'):
        info = tutor.findAll("td")
        if isinstance(info[0].p, bs4.element.Tag):
            info[0].p.decompose()
        data = info[0].text.strip().split(" ")
        class_name = ' '.join(data[2:])
        link = "N/A"
        try:
            copy = info[1].p.text.strip()
            info[1].p.decompose()
            tutor = info[1].text.strip().split('-')[0]
            # print(info[1].text.split('-'))
        except AttributeError:
            tutor = info[1].text.split('-')[0].strip()
            link = info[1].text.split('-')[1].strip()
        if tutor[0:5] != "Small":
            link = copy
        tutor = tutor.replace(u'\xa0', u' ')
        level = ' '.join(data[0:2])
        # print(class_name) 
        # print(data[0:2])  
        # print(tutor)  
        # if(info[1].text.strip()[0:5] != "Small"):
        #     tutor = info[1].text.strip()
        #     webex = info[1].find("a").get('href')
        if class_name in dictionary.keys():
            dictionary[class_name]["Tutors"].append({"Name": tutor, "Access":link})
        else:
            found = False
            for k, v in dictionary.items():
                if(v['Level'] == level):
                    dictionary[k]["Tutors"].append({"Name": tutor, "Access":link})
                    found = True
                    break
            if (found == False): 
                dictionary[class_name] = {"Level": level, "Tutors": [{"Name": tutor, "Access":link}]}
    # print(dictionary.values().keys())
    # for k, v in dictionary.items():
    #             print(v['Level'])
    #             break
    with open("RPI_ALAC.json", "w") as outfile:
        outfile.write(json.dumps(dictionary, indent=4))

    
if __name__ == "__main__":
    get_ALAC_tutor()
        
