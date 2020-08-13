#This is how I got the Dataset prepared for producing the 
#line charts with Altair in order to pass these charts/visualizations as vega object to Marker tooltip in the folium maps.

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import datetime as dt

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/Yash/credentials.json',scope)    
client = gspread.authorize(creds)

x = pd.date_range(dt.date(2020,7,11),dt.date(2020,8,10),freq='D')
month = {7:'July',8:'August'}

#Getting the whole sheet and using API - //approach\\

#Getting Data for total positive cases
# sheet = client.open('Data COVID19').worksheet('10 July 2020')
# month = {7:'July',8:'August'}
# Df = pd.DataFrame(sheet.get_all_records())
# Df = Df[['','Total Positive']].set_index('').T
# for date in x:
#     sheet = client.open('Data COVID19').worksheet(f"{date.day} {month[date.month]} 2020")
#     df = pd.DataFrame(sheet.get_all_records())
#     df = df[['','Total Positive']].set_index('').T
#     Df = Df.append(df)


#Getting Data for total deaths
sheet = client.open('Data COVID19').worksheet('10 July 2020')
Df2 = pd.DataFrame(sheet.get_all_records())
Df2 = Df2[['','Deaths']].set_index('').T
for date in x:
    sheet = client.open('Data COVID19').worksheet(f"{date.day} {month[date.month]} 2020")
    df = pd.DataFrame(sheet.get_all_records())
    df = df[['','Deaths']].set_index('').T
    Df2 = Df2.append(df)


#Getting Data for total active cases
sheet = client.open('Data COVID19').worksheet('10 July 2020')
Df3 = pd.DataFrame(sheet.get_all_records())
Df3 = Df3[['','Total Active']].set_index('').T
for date in x:
    sheet = client.open('Data COVID19').worksheet(f"{date.day} {month[date.month]} 2020")
    df = pd.DataFrame(sheet.get_all_records())
    df = df[['','Deaths']].set_index('').T
    Df3 = Df3.append(df)


#Getting Data for Recovery rate
sheet = client.open('Data COVID19').worksheet('10 July 2020')
Df4 = pd.DataFrame(sheet.get_all_records())
Df4 = Df4[['','Recovery Rate']].set_index('').T
for date in x:
    sheet = client.open('Data COVID19').worksheet(f"{date.day} {month[date.month]} 2020")
    df = pd.DataFrame(sheet.get_all_records())
    df = df[['','Recovery Rate']].set_index('').T
    Df4 = Df4.append(df)

#Appendind all the datasets into one dataset namely Df
# Df = Df.append(Df2)
Df2 = Df2.append(Df3)
Df2 = Df2.append(Df4)

#repairing some minor cracks
Df2.rename(axis=1,mapper={'Charkhi Dadri':'Dadri','Gurugram':'Gurgaon','Mahendergarh':'Mahendragarh','Yamunanagar':'Yamuna Nagar'},inplace=True)
y = pd.date_range(dt.date(2020,7,10),dt.date(2020,8,10),freq='D') 
z = pd.date_range(dt.date(2020,7,10),dt.date(2020,8,10),freq='D') 
y = y.append(y)
y = y.append(z)
Df2.reset_index(inplace = True)
Df2.set_index(y,inplace=True)
Df2.rename(axis=1,mapper={'index':'Variable'},inplace=True)
Df2 = Df2.applymap(lambda x:0 if x=='' else x)


#Writing the data into xlsx file
writer = pd.ExcelWriter('C:/Users/Yash/Sublime files/Haryana Covid Project/haryana dataset.xlsx')
Df2.to_excel(writer)
writer.save()

#AND WE'RE DONE!!!