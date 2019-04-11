#!/usr/bin/env python
# coding: utf-8

import mechanicalsoup
import json
import os
import getpass
import time
import pickle

browser = mechanicalsoup.StatefulBrowser()

#inputing handle and opening it's submission page

handle = input("Enter handle name:")
homeUrl = "https://codeforces.com/submissions/"+handle
browser.open(homeUrl)

first_time_flag = False
#changing the directory

path_to_download_directory = os.getcwd()+'/'+handle
if not os.path.exists(path_to_download_directory):
    os.makedirs(path_to_download_directory)
    first_time_flag = True
os.chdir(path_to_download_directory)

succesID=[] #holds successful submissions ID
links=[] #holds successful submissions links
end_search = False

if (first_time_flag == False):
    idFile = open('succesfulIdRecord','rb')
    savedID = pickle.load(idFile)
    idFile.close()

else:
    savedID=[]

#counting total number of pages

pageIndex = browser.get_current_page().select(".pagination")

pageNumberList=[]
for row in pageIndex:
    cells = row.find_all("span",attrs = {"class": "page-index"})
    for x in cells:
        pageNumberList.append(x['pageindex'])

totalNumberOfPages = int(max(pageNumberList))

pageBaseLink = 'https://codeforces.com/submissions/'+handle+'/page/'

for i in range(1,totalNumberOfPages):
    pageLink = pageBaseLink + str(i)
    browser.open(pageLink)

    # selecting table for getting successful submitted question list

    table = browser.get_current_page().select("table.status-frame-datatable")

    for row in table:
        if (end_search == True):
            break
        col = row.find_all("span",attrs = {"class": "submissionVerdictWrapper"})
        for x in col:
            subid=x['submissionid']
            if (subid in savedID):
                end_search = True 
                break
            verdict=x['submissionverdict']
            if(verdict=='OK'):
                succesID.append(subid)

    if(end_search==True):
        break
        
#print("Total succesful codes submitted:",len(succesID))  

    with open('succesfulIdRecord','wb') as idFile:
        pickle.dump(succesID,idFile)

# saving list of succesful questions link

    for row in table:
        col = row.find_all("a",attrs = {"class": "view-source"})
        for x in col:
            subid=x['submissionid']
                links.append(x['href'])

baseurl="https://codeforces.com"

# Generating link for getting solution

for link in links:
    time.sleep(0.4)
    
    finalurl = baseurl+link
    print(finalurl)

    browser.open(finalurl)

#saving code in a string

    codestr=''

    codebox = browser.get_current_page().select('#program-source-text')
    for x in codebox:
        codestr+=x.text

    datatable =browser.get_current_page().select(".datatable")

#getting name of Question number

    textlist=[]
    for row in datatable:
        anchors = row.find_all('a')
        for x in anchors:
            textlist.append(x.text)
    filename=textlist[1]
    filename+='.cpp'
    filename

#saving code with appropriate file name
    if(os.path.isfile('./'+filename)==False):
        f = open(filename, "w")
        f.write(codestr)
        f.close()
