# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 14:43:05 2021

@author: Andreu
"""

#%% Load in the necessary lybraries

import requests
from bs4 import BeautifulSoup as bs
import urllib.request

# Load the webpage content
r = requests.get("https://keithgalli.github.io/web-scraping/example.html")

# Convert to a beautiful soup object
soup = bs(r.content , features="lxml")

# Print out our html
print(soup.prettify())

#%% Start using Beautiful Soup to Scrape

# find and find_all

first_header = soup.find("h2")
#print(first_header)

header = soup.find_all("h2")
#print(header)

# Pass in a list of elements to look for

first_header = soup.find(["h1" , "h2"])
#print(first_header)

header = soup.find_all(["h1" , "h2"])
#print(header)

# You can pass in attributes to the find/find_all function

paragraph = soup.find_all("p" , attrs = {"id":"paragraph-id"})
#print(paragraph)

# You can nest find/find_all calls

body = soup.find("body")
div = body.find("div")
header = div.find("h1")
#print(header)

# We can search specific strings in our find/find_all calls
import re
paragraphs = soup.find_all("p" , string = re.compile("Some"))
#print(paragraphs)

headers = soup.find_all("h2" , string = re.compile("(H|h)eader"))
#print(headers)

# select (CSS selector)

content = soup.select("p")
#print(content)

content = soup.select("div p")
#print(content)

paragraphs = soup.select("h2 ~ p")
#print(paragraphs)

bold_text = soup.select("p#paragraph-id b")
#print(bold_text)

paragraphs = soup.select("body > p")
#print(paragraphs)

for paragraph in paragraphs:
    print(paragraph.select("i"))


#%% Get different properties of the HTML

header = soup.find("h2")
#print(header.string)

div = soup.find("div")
#print(div.prettify())
#print(div.get_text())

# Get a specific property from an element
link = soup.find("a")
#print(link["href"])

paragraphs = soup.select("p#paragraph-id")
#print(paragraphs[0]["id"])


#%% Code navigation

# Path syntax

#print(soup.body.div.h1.string)

# Know the terms: Parent, Sibling and Child

#print(soup.body.find("div").find_next_siblings())

#%% EXERCISES

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import re

# Go to https://keithgalli.github.io/web-scraping/webpage.html

# Load the webpage content
r = requests.get("https://keithgalli.github.io/web-scraping/webpage.html")

# Convert to a beautiful soup object
webpage = bs(r.content , features="lxml")

#%% 1 Grab all of the social links from the webpage (do it in 3 different ways)

sociallist = []

body = webpage.find("body")
paragraphs = body.find_all("a")
link1 = body.find("a" , string = re.compile("youtube"))
link2 = body.find("a" , string = re.compile("instagram"))
link3 = body.find("a" , string = re.compile("twitter"))
link4 = body.find("a" , string = re.compile("linkedin"))
link5 = body.find("a" , string = re.compile("tiktok"))

print(paragraphs)
print(link1["href"])
print(link2["href"])
print(link3["href"])
print(link4["href"])
print(link5["href"])

sociallist.append(link1["href"])
sociallist.append(link2["href"])
sociallist.append(link3["href"])
sociallist.append(link4["href"])
sociallist.append(link5["href"])

answer1 = sociallist

#%% 2 Scrape an HTML table into Pandas Dataframe

tablehead = webpage.find("thead")
tablehead = [text for text in tablehead.stripped_strings]

df = pd.DataFrame(columns = tablehead)

tablebody = webpage.find("tbody")

row1 = tablebody.find("tr")
row1list = [text for text in row1.stripped_strings]

filtered1 = []
for x in row1list:
    if x != "|":
        filtered1.append(x)

rowlist = []
filtered1 = []
row1 = tablebody.find("tr")
row1list = [text for text in row1.stripped_strings]
for x in row1list:
    if x != "|":
        filtered1.append(x)
rowlist.append(filtered1)
row = row1


while not row == None:
    row = row.find_next_sibling()
    if row == None:
        pass
    else:
        row1list = [text for text in row.stripped_strings]
        filtered1 = []
        for x in row1list:
            if x != "|":
                filtered1.append(x)
        rowlist.append(filtered1)

for i in range(len(rowlist)):
    while len(rowlist[i]) < len(tablehead):
        rowlist[i].append(" ")


for i in range(len(rowlist)):
    zz = pd.Series(rowlist[i] , index = df.columns)
    df = df.append(zz , ignore_index = True)

answer2 = df

#%% 3 Grab all fun facts that contain the word "is"

factlist = []
funfacts = webpage.find("ul" , attrs = {"class":"fun-facts"})
fact1 = funfacts.find("li" , string = re.compile("is"))
factlist.append(fact1.get_text())
fact = fact1

while not fact == None:
    fact = fact.find_next_sibling("li")
    if fact == None:
        pass
    else:
        if "is" in fact.get_text():
            factlist.append(fact.get_text())
        else:
            pass

#%% 4 Use beautiful soup to help download an image from a webpage

image = webpage.find("img" , attrs = {"alt":"Riomaggiore, Cinque de Terre"})
halflink2 = image["src"] 
halflink1 = "https://keithgalli.github.io/web-scraping/"

link = halflink1 + halflink2

urllib.request.urlretrieve(link , "C:/Users/Andreu/OneDrive/PYTHON/Project_machine_learning/riomaggiore.jpg")


#%% 5 Solve the mystery challenge

block1 = webpage.find("div" , attrs = {"class":"block"})

filelist = []

file = block1.find("a")
filelist.append(halflink1 + file["href"])

while not file == None:
    try:
        file = file.find_parent().find_next_sibling().find("a")
        if file == None:
            pass
        else:
            filelist.append(halflink1 + file["href"])
    except:
        file = None

block2 = block1.find_next_sibling()

file = block2.find("a")
filelist.append(halflink1 + file["href"])

while not file == None:
    try:
        file = file.find_parent().find_next_sibling().find("a")
        if file == None:
            pass
        else:
            filelist.append(halflink1 + file["href"])
    except:
        file = None

wordlist = []

for link in filelist:
    r = requests.get(link)
    file = bs(r.content , features="lxml")
    
    word = file.find_all("p" , attrs = {"id":"secret-word"})
    
    for el in word:
        wordlist.append(el.get_text())
    
print('The secret message is: "' + " ".join(wordlist) + '"')

























