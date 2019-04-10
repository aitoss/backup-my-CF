#!/usr/bin/env python
# coding: utf-8

import mechanicalsoup
import json
import os
import getpass
import time

browser = mechanicalsoup.StatefulBrowser()

browser.open("https://codeforces.com/enter")

browser.select_form("#enterForm")

def user_auth():
    username=input('Enter Handle or Email:-')
    password=getpass.getpass('Enter password:-')
    creds={'username':username,
            'password':password
            }
    with open('cred.json','w') as outfile:
        json.dump(creds,outfile)

#if using for first time
if(os.path.isfile('./cred.json')==False):
    print("It's your first time....")
    user_auth()


#loading information from JSON file 

with open('cred.json') as json_file:
    creds = json.load(json_file)
    browser['handleOrEmail']=creds['username']
    browser['password']=creds['password']

browser.submit_selected()

succesID=[] #list for storing successful Question IDs

links=[]

browser.follow_link("submissions")


#counting total number of pages

pageIndex = browser.get_current_page().select(".pagination")

pageNumberList=[]
for row in pageIndex:
    cells = row.find_all("span",attrs = {"class": "page-index"})
    for x in cells:
        pageNumberList.append(x['pageindex'])

totalNumberOfPages = int(max(pageNumberList))

pageBaseLink = 'https://codeforces.com/submissions/shellkore/page/'

for i in range(1,totalNumberOfPages):
    pageLink = pageBaseLink + str(i)
    browser.open(pageLink)

    # selecting table for getting successful submitted question list

    table = browser.get_current_page().select("table.status-frame-datatable")

    for row in table:
        col = row.find_all("span",attrs = {"class": "submissionVerdictWrapper"})
        for x in col:
            subid=x['submissionid']
            verdict=x['submissionverdict']
            if(verdict=='OK'):
                succesID.append(subid)
        
    
# saving list of succesful questions link

    for row in table:
        col = row.find_all("a",attrs = {"class": "view-source"})
        for x in col:
            subid=x['submissionid']
            if(subid in succesID):
                links.append(x['href'])

summaryFile = open('summary.txt','w')

for ids in succesID:
    summaryFile.write(ids+'\n')


summaryFile.close()

#print(os.getcwd())
path_to_download_directory = os.getenv("HOME")+"/Downloads/Codeforces-solution"
if not os.path.exists(path_to_download_directory):
    os.makedirs(path_to_download_directory)
os.chdir(path_to_download_directory)
#print(os.getcwd())

baseurl="https://codeforces.com"

# Generating link for getting solution

for link in links:
    time.sleep(1)
    
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

    f = open(filename, "w")
    f.write(codestr)
    f.close()
