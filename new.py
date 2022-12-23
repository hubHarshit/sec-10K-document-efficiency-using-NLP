from cgitb import text
from pyexpat import features
import sec_edgar_downloader
import glob
import os
import nltk   
from urllib.request import urlopen 
from bs4 import BeautifulSoup   
import re

# print(sec_edgar_downloader.__version__)
from sec_edgar_downloader import Downloader



###########################################################################################
# from sec_api import QueryApi
# queryApi = QueryApi(api_key="6ecda7bc37b447a93abb908e99ac24392d689337ada5f0db9838e564841f9af4")
from sec_api import ExtractorApi
import pandas as pd
import numpy as np
from openpyxl import load_workbook
# df=pd.DataFrame(index=[8])
def text_extractor_7(section_html,company_name,cik,filed_date):
    
    
   
    df=pd.DataFrame(columns=['Trillion Dollars','Million Dollars','Billion Dollars','Thousand Dollars','Decimal Dollars','Company Name','CIK','Filed Date'])
    df = pd.DataFrame(index=[cik])
    print('million dollars section 7')
    
    countMilliondollars=[]
    for i in re.findall("(\$\d+(,\d+)*(\.\d+)?) million",section_html):
        countMilliondollars.append(i[0])
    df['Million Dollars']=len(countMilliondollars)
    for i in re.findall("(\$\d+(,\d+)*(\.\d+)?)",section_html):
        k=re.sub(",","",i[0])
        # print(k)
        if(8<=len(k.split(".")[0])<=10):
            countMilliondollars.append(i[0]) 
    print(countMilliondollars)

    print('billion dollars section 7')
    countBilliondollars= []
    for i in re.findall('\$\d+(?:\.\d+)? billion',section_html):
        countBilliondollars.append(i[0])
    df['Billion Dollars']=len(countBilliondollars)
    print(countBilliondollars)


    print('thousand dollars section 7')
    countThousandDollars=[]
    countHundredDollars=[]
    temp=[]
    
    
    for i in re.finditer('(\$\d+(,\d+)*(\.\d+)?)',section_html):
        # if i[0]+' billion' not in countBilliondollars and i[0]+' million' not in countMilliondollars:
        if(section_html[i.end(0)+1: i.end(0)+8].strip()!="million" and section_html[i.end(0)+1: i.end(0)+8].strip()!="billion" and section_html[i.end(0)+1: i.end(0)+9].strip()!="trillion" and section_html[i.end(0)+1:i.end(0)+11].strip()!="per share"):
            temp.append(section_html[int(i.start(0)):int(i.end(0))])
        
    # print('temp here')
    # print(temp)
    for j in temp:
        k=re.sub(",","",j)
    # print(k)
        if(5<=len(k.split(".")[0])<=7):
            countThousandDollars.append(j) 
        if(2<=len(k.split(".")[0])<=4):
            countHundredDollars.append(j)
    
                
    df['Thousand Dollars']=len(countThousandDollars)
    print(countThousandDollars)

    print('trillion dollars section 7')
    countTrilliondollars= []
    for i in re.findall('\$\d+(?:\.\d+)? trillion',section_html):
        countTrilliondollars.append(i[0])
    df['Trillion Dollars']=len(countTrilliondollars)
    # df['Trillion Dollars']=pd.Series(countTrilliondollars).size if(pd.Series(countTrilliondollars).size!=0) else 0
    # print(countTrilliondollars)
    # print(df['Trillion Dollars'])
    

    print('Hundred dollars section 7')
    # dollars=re.findall('(\$\d+( \w+|[\d,.]+))',section_html)
    # countDecimaldollars=[]
    # for i in dollars:
    #     if i not in countBilliondollars and countMilliondollars:
    #         countDecimaldollars.append(i[0])
    df['Hundred Dollars']=len(countHundredDollars)
    print(countHundredDollars)
    # print(df['Million Dollars'].head(10))
    # print(countDecimaldollars)



    

    df['Company Name']=company_name
    df['CIK']=cik
    df['Filed Date']=filed_date
    print(df['Company Name'])
    # print(df['Billion Dollars'])
    return len(countBilliondollars),len(countTrilliondollars),len(countMilliondollars),len(countThousandDollars),len(countHundredDollars)

    
    # book=load_workbook('master.xlsx')
    # writer.book = book
    # writer.sheets='2010'

    # print(df)


    ###########################################section 8
    # filing_url_10k = "https://www.sec.gov/Archives/edgar/data/320193/000032019318000145/a10-k20189292018.htm"
    # section_html1 = extractorApi.get_section(filing_url_10k, "8", "text")
    # countMilliondollars=[]
    # countBilliondollars=[]
    # countDecimaldollars=[]
    # countDollars_comma=[]
    # countMilliondollars= re.findall('\$\d+(?:\.\d+)? million',section_html1)
    # for i in re.findall('\$\d+(?:\,\d+)? million',section_html1):
    #     countMilliondollars.append(i)
    # print('million dollars section 8')
    # print(countMilliondollars)
    # countBilliondollars= re.findall('\$\d+(?:\.\d+)? billion',section_html1)
    # for i in re.findall('\$\d+(?:\,\d+)? billion',section_html1):
    #     countBilliondollars.append(i)
    # print('billion dollars section 8')
    # print(countBilliondollars)
    # countDollars_comma= re.findall('\$\d+\,\d+',section_html1)
    # print('comma dollars section 8')
    # print(countDollars_comma)
    # dollars=re.findall('\$\d+\.\d+',section_html1)
    # countDecimaldollars=[]
    # print('decimal dollars section 8')
    # for i in dollars:
    #     if i not in countBilliondollars and countMilliondollars:
    #         countDecimaldollars.append(i)

    # print(countDecimaldollars)

