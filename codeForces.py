#!/usr/bin/env python
# coding: utf-8

# In[1]:


import mechanicalsoup
import json


# In[2]:


browser = mechanicalsoup.StatefulBrowser()


# In[3]:


browser.open("https://codeforces.com/enter")


# In[4]:


browser.select_form("#enterForm")


# In[5]:


with open('cred.json') as json_file:
    creds = json.load(json_file)
    browser['handleOrEmail']=creds['username']
    browser['password']=creds['password']


# In[6]:


browser.submit_selected()


# In[7]:


browser.follow_link("submissions")


# In[8]:


table = browser.get_current_page().select("table.status-frame-datatable")


# In[9]:


succesID=[]
for row in table:
    col = row.find_all("span",attrs = {"class": "submissionVerdictWrapper"})
    for x in col:
        subid=x['submissionid']
        verdict=x['submissionverdict']
        if(verdict=='OK'):
            succesID.append(subid)
        
    


# In[11]:


links=[]
for row in table:
    col = row.find_all("a",attrs = {"class": "view-source"})
    for x in col:
        subid=x['submissionid']
        if(subid in succesID):
            links.append(x['href'])


# In[12]:


baseurl="https://codeforces.com"


# In[13]:


link='/contest/1132/submission/51841587'
finalurl = baseurl+link
print(finalurl)


# In[14]:


browser.open(finalurl)


# In[15]:


codebox = browser.get_current_page().select('#program-source-text')
codestr=codebox[0].text


# In[16]:


datatable =browser.get_current_page().select(".datatable")


# In[17]:


textlist=[]
for row in datatable:
    anchors = row.find_all('a')
    for x in anchors:
        textlist.append(x.text)
filename=textlist[1]
filename+='.cpp'
filename


# In[18]:


f = open(filename, "w")
f.write(codestr)
f.close()


# In[ ]:




