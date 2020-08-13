#This is how I got the Dataset prepared for producing the 
#line charts with Altair in order to pass these charts/visualizations as vega object to Marker tooltip in the folium maps.
#This data is without the Total Poisitive parameter


month = {7:'July',8:'August'}
url = 'C:/Users/Yash/Sublime files/Haryana Covid Project/Raw Data COVID19.xlsx'

#Getting the data for 'Deaths' cases
Df2 = pd.read_excel(url,sheet_name='10 July 2020')
Df2 = Df2[['Unnamed: 0','Deaths']].set_index('Unnamed: 0').T
for date in x:
    df = pd.read_excel(url,sheet_name=f"{date.day} {month[date.month]} 2020")
    df = df[['Unnamed: 0','Deaths']].set_index('Unnamed: 0').T
    Df2 = Df2.append(df)


#Getting Data for total active cases
Df3 = pd.read_excel(url,sheet_name='10 July 2020')
Df3 = Df3[['Unnamed: 0','Total Active']].set_index('Unnamed: 0').T
for date in x:
    df = pd.read_excel(url,sheet_name=f"{date.day} {month[date.month]} 2020")
    df = df[['Unnamed: 0','Total Active']].set_index('Unnamed: 0').T
    Df3 = Df3.append(df)


#Getting Data for Recovery rate
Df4 = pd.read_excel(url,sheet_name='10 July 2020')
Df4 = Df4[['Unnamed: 0','Recovery Rate']].set_index('Unnamed: 0').T
for date in x:
    df = pd.read_excel(url,sheet_name=f"{date.day} {month[date.month]} 2020")
    df = df[['Unnamed: 0','Recovery Rate']].set_index('Unnamed: 0').T
    Df4 = Df4.append(df)

#Stiching the collected data together
Df2 = Df2.append(Df3)
Df2 = Df2.append(Df4)

#Repairing some cracks
Df2.rename(axis=1,mapper={'Charkhi Dadri':'Dadri','Gurugram':'Gurgaon','Mahendergarh':'Mahendragarh','Yamunanagar':'Yamuna Nagar'},inplace=True)
y = pd.date_range(dt.date(2020,7,10),dt.date(2020,8,10),freq='D') 
z = pd.date_range(dt.date(2020,7,10),dt.date(2020,8,10),freq='D') 
y = y.append(y)
y = y.append(z)
Df2.reset_index(inplace = True)
Df2.set_index(y,inplace=True)
Df2.rename(axis=1,mapper={'index':'Variable'},inplace=True)
Df2.fillna(value=0,inplace=True)

#Converting the Recovery Rate values from percentages to a scale of 100 for plotting purposes
Df22 = Df2.iloc[64:,:].applymap(lambda x: x*100 if isinstance(x,float) else x)
Df2.drop(axis=0,labels=list(range(64,96)),inplace=True)   #Dropping the recovery rate data from the main data inorder to append new recovery rate data
Df2 = Df2.append(Df22)  #Appendind the new reovery rate data to the main data

#Since there are a lot of gaps in the data, plots produced with this data would be misleading,
#Therefore, defining a function to fill the average of the values (to flatten the data) in places of missing data
#Defining the function that will flatten out the Dataset
def avg_2(df):
    for col in range(df.shape[1]):
        block = 10
        for row in range(df.shape[0]):
            if (df.iloc[:,col].dtype=='float64') or (df.iloc[:,col].dtype=='int64'):
                if not all(df.iloc[row:row+block,col]==0): 
                    if (df.iloc[row,col]==0) and (row!=0 and row!=(df.shape[0]-1)):
                        df.iloc[row,col] = (df.iloc[row-1,col]+df.iloc[row+1,col])/2
                else:
                    block-=1
                    if block==0:
                        block = 10
                    df.iloc[row,col] =df.iloc[:,col].mean()

#breaking the dataset to apply the avg_2() function to only the 'Total Active' and 'Recovery Rate' parameters but
#not the 'Deaths' parameter as Deaths can fluctuate in any manner, hence flattening the 'Deaths' data is not required.
Df_mod = Df2.iloc[32:,:] #Now Df_mod contains the data tha needs to be flattened
Df2.drop(axis=0,labels=list(range(32,96)),inplace=True) # And Df2 is left out with the 'Deaths' data that is not to be altered at all.
avg_2(Df_mod) #Flattening the data
Df2 = Df2.append(Df_mod) #Appendind the altered data back to the 'Deaths' data set.


#Writing and saving data to an excel sheet
writer = pd.ExcelWriter('C:/Users/Yash/Sublime files/Haryana Covid Project/flattened_dataset.xlsx')
Df2.to_excel(writer)
writer.save()

#And we're DONE!!!!