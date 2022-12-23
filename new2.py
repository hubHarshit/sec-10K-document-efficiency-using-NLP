# Import requests to retrive Web Urls example HTML. TXT 
import requests

# Import BeautifulSoup
from bs4 import BeautifulSoup

# import re module for REGEXes
import re

# import pandas
import pandas as pd
import os
import glob
import new as script
#open document


list_data=[]
error_list=[]
for filename in os.listdir(r'.\forms2016\QTR3'): 
    if filename.endswith('.txt'):
        
        
        with open(os.path.join(r'.\forms2016\QTR3', filename)) as f:
            print(filename)
            
            raw_10k = f.read()
            company=raw_10k[raw_10k.find('COMPANY DATA:')+len('COMPANY DATA:'):raw_10k.find('FILING VALUES')]
            print(company)

            # regex to find company details
            filed_index=raw_10k.find('FILED AS OF DATE:')
            date_of_change_index=raw_10k.find('DATE AS OF CHANGE:')
            filed_date=raw_10k[filed_index+len('FILED AS OF DATE:'):date_of_change_index].strip()
            company_name=raw_10k[raw_10k.find('COMPANY CONFORMED NAME:')+len('COMPANY CONFORMED NAME:'):raw_10k.find('CENTRAL INDEX KEY:')].strip()
            if('STANDARD INDUSTRIAL CLASSIFICATION' in company):
                cik=raw_10k[raw_10k.find('CENTRAL INDEX KEY:')+len('CENTRAL INDEX KEY:'):raw_10k.find('STANDARD INDUSTRIAL CLASSIFICATION:')].strip()
            else:
                cik=raw_10k[raw_10k.find('CENTRAL INDEX KEY:')+len('CENTRAL INDEX KEY:'):raw_10k.find('IRS NUMBER:')].strip()
            
            # Regex to find <DOCUMENT> tags
            doc_start_pattern = re.compile(r'<DOCUMENT>')
            doc_end_pattern = re.compile(r'</DOCUMENT>')
            # Regex to find <TYPE> tag prceeding any characters, terminating at new line
            type_pattern = re.compile(r'<TYPE>[^\n]+')
            # Create 3 lists with the span idices for each regex

            ### There are many <Document> Tags in this text file, each as specific exhibit like 10-K, EX-10.17 etc
            ### First filter will give us document tag start <end> and document tag end's <start> 
            ### We will use this to later grab content in between these tags
            doc_start_is = [x.end() for x in doc_start_pattern.finditer(raw_10k)]
            doc_end_is = [x.start() for x in doc_end_pattern.finditer(raw_10k)]

            ### Type filter is interesting, it looks for <TYPE> with Not flag as new line, ie terminare there, with + sign
            ### to look for any char afterwards until new line \n. This will give us <TYPE> followed Section Name like '10-K'
            ### Once we have have this, it returns String Array, below line will with find content after <TYPE> ie, '10-K' 
            ### as section names
            doc_types = [x[len('<TYPE>'):] for x in type_pattern.findall(raw_10k)]
            document = {}

            # Create a loop to go through each section type and save only the 10-K section in the dictionary
            for doc_type, doc_start, doc_end in zip(doc_types, doc_start_is, doc_end_is):
                if doc_type == '10-K':
                    document[doc_type] = raw_10k[doc_start:doc_end]
            # display excerpt the document
            # print(document['10-K'][0:500])
            # Write the regex
            regex = re.compile(r'(>Item(\s|&#160;|&nbsp;)(7A|7|8|9)\.{0,1})|(ITEM\s(7A|7|8|9))')

            # Use finditer to math the regex
            matches = regex.finditer(document['10-K'])

            # Write a for loop to print the matches
            # for match in matches:
            #     print(match)
            # Matches
            matches = regex.finditer(document['10-K'])
            
            # Create the dataframe
            test_df = pd.DataFrame([(x.group(), x.start(), x.end()) for x in matches])
            df_error=pd.DataFrame(columns=['Company Name','CIK','Filed Date','FileName'],index=[''])
            
            try:
                test_df.columns = ['item', 'start', 'end']
                test_df['item'] = test_df.item.str.lower()
                test_df['item'] = test_df.item.str.replace("\n","")
            except ValueError as ve:
                df_error['Company Name']=company_name
                df_error['CIK']=cik
                df_error['Filed Date']=filed_date
                df_error['FileName']=filename
                error_list.append(df_error)
                continue
            
            
            # Display the dataframe
            # Get rid of unnesesary charcters from the dataframe
            test_df.replace('&#160;',' ',regex=True,inplace=True)
            test_df.replace('&nbsp;',' ',regex=True,inplace=True)
            test_df.replace(' ','',regex=True,inplace=True)
            test_df.replace('\.','',regex=True,inplace=True)
            test_df.replace('>','',regex=True,inplace=True)
            # print(test_df)
            # Drop duplicates
            pos_dat = test_df.sort_values('start', ascending=True).drop_duplicates(subset=['item'], keep='last')
            print(pos_dat)
            df=pd.DataFrame(columns=['Trillion Dollars','Million Dollars','Billion Dollars','Thousand Dollars','Hundred and Decimal Dollars',
            'Company Name','CIK','Filed Date'])
            df = pd.DataFrame(index=[''])
            # Set item as the dataframe index
            pos_dat.set_index('item', inplace=True)
            # print(pos_dat)
            df['Company Name']=company_name
            df['CIK']=cik
            df['Filed Date']=filed_date
            # print(df)
            
            
            # print(df)
            # Get Item 7
            if('item7' in pos_dat.index and 'item8' in pos_dat.index):  #need to handle missing item 8 case
                item_7_raw = document['10-K'][pos_dat['start'].loc['item7']:pos_dat['start'].loc['item8']]
                # item_7_content=re.sub(r'<TABLE>(.*?)</TABLE>','',item_7_raw)
                # item_7_content=re.sub(r'<table>(.*?)</table>','',item_7_content)
                item_7_content = BeautifulSoup(item_7_raw, 'lxml')
                # print(item_7_content)
                # print(item_7_raw)
                data_7=script.text_extractor_7(item_7_content.get_text(),company_name,cik,filed_date)
                # # print(data_7[3])
                # a=pd.DataFrame({'Trillion Dollars':data_7[0]})
                # b=pd.DataFrame({'Billion Dollars':data_7[1]})
                # c=pd.DataFrame({'Million Dollars':data_7[2]})
                # d=pd.DataFrame({'Thousand Dollars':data_7[3]})
                # e=pd.DataFrame({'Hundred and Decimal Dollars':data_7[4]})
                # df=pd.concat([a,b,c,d,e], axis=1)
                df['Trillion Dollars']=data_7[1]
                df['Billion Dollars']=data_7[0]
                df['Million Dollars']=data_7[2]
                df['Thousand Dollars']=data_7[3]
                df['Hundred and Decimal Dollars']=data_7[4]
                # # print(df)
                # df.to_excel('company_data/{}.xlsx'.format(company_name))
                list_data.append(df)
# print(error_list)
data=pd.concat(list_data)                
data.to_excel('master.xlsx')
data_error=pd.concat(error_list)
data_error.to_excel('error.xlsx')

            

            #Get Item 8
            # item_8_raw = document['10-K'][pos_dat['start'].loc['item8']:pos_dat['start'].loc['item9']]

            ### First convert the raw text we have to exrtacted to BeautifulSoup object 
            

            ### First convert the raw text we have to exrtacted to BeautifulSoup object 
            # item_8_content = BeautifulSoup(item_8_raw, 'lxml')

            ### First convert the raw text we have to exrtacted to BeautifulSoup object 
            # print(item_7_content.get_text())
            
            
            
            