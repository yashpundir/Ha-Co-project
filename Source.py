#importing libraries
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import folium
import branca
import altair as alt
import pandas as pd
import datetime
import webbrowser
import tkinter as tk
import tkcalendar as tkcal
import numpy as np


scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',
			"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/Yash/credentials.json',scope)    
client = gspread.authorize(creds)



#top-level root
root = tk.Tk(className='ViSuAlIzE')
root.geometry("907x625")

#top frame
top_frame = tk.Frame(master=root,height=300,width=750,bg='gray89',bd=3,relief='ridge',padx=100,pady=20)
top_frame.pack(side='top')

#bottom frame
bottom_frame = tk.Frame(master=root, height=250,width=750,bg='gray89',bd=3,relief='ridge')
bottom_frame.pack(side='bottom')

def save_map():
  download_map()
  har.save(f"{path_entry.get()}.html")
  #popup message upon saving
  win2 = tk.Toplevel(master=root,bg='snow2',bd=6,height=200,width=360,relief='groove')
  win2.title('Map Saved')
  msg = tk.Label(master=win2,text='Map Saved Successfully!')
  msg.pack()

#Toplevel window
def download_map_window():
  global path_entry
  win = tk.Toplevel(master=root,bg='snow2',bd=8,height=200,width=500,relief='groove')
  win.title('Download Map!')
  path_name = tk.Label(master=win, text='enter the path you want to save the map in:',anchor='w',font=40)
  path_name.pack(padx=0,pady=3,side='top')
  path_entry = tk.Entry(master=win,width=50,fg='black',borderwidth=5,relief='sunken')
  path_entry.pack(padx=5,pady=10)
  save_button = tk.Button(master=win, text='SAVE',command=save_map,fg='green',bg='light blue',
                            font=("Gabriola", 13, "bold"),activebackground='light green')
  save_button.pack(ipadx=20,ipady=1,fill='x',side='right')
             

#Main title
Title = tk.Label(master=top_frame,text="COVID19 Visualisation on Haryana",bg='light blue',font=("Gabriola", 22, "bold"))
Title.pack(padx=20,pady=5,side='top')

#Calendar widget
x = datetime.datetime.today()
y = x.day-1
tod = datetime.date(x.year,x.month,y) 
Cal = tkcal.Calendar(master=top_frame,firstweekday='monday',selectmode="day",cursor='hand1',borderwidth=5,
                    showothermonthdays=False,datepattern='dd-mm-y',year=2020,month=8,day=6,
                    selectforeground='green',mindate=datetime.date(2020,6,15),maxdate=tod,
                    font=('Jokerman',13,'normal'),showweeknumbers=False,selectbackground='lavender')
Cal.pack(padx=20,pady=8,side='left')

#Radio Button widget
options = ['Total Deaths','Total Active','Total Positive']
v = tk.StringVar(top_frame, "1")
for text in options:
    option = tk.Radiobutton(master=top_frame,text=text, value=text,variable=v,font =("Gabriola", 15, "bold italic"),
      bg='light blue',activebackground='light green',indicator=True,anchor='e',justify='left')
    option.pack(fill='x',ipady=5,pady=10,side='top')

def decorator(original_func):
  original_func()
  har.save('har_map.html')
  webbrowser.open_new_tab('har_map.html')

#Plot map function
def download_map():    
    #getting the selected date
    date = Cal.selection_get()
    
    #Accessing a worksheet
    months = {6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
    sheet = client.open('Data COVID19').worksheet(f"{date.day} {months[date.month]} {date.year}")

    #Data Wrangling
    df = pd.DataFrame(sheet.get_all_records())
    df.rename(axis=1,mapper={'':'Districts','Deaths':'Total Deaths'},inplace=True)
    df.columns = [str(col) for col in df.columns]
    df = df.iloc[:,[0,1,3,4]]
    df = df.applymap(lambda x:0 if x=='' else x)
    df.iloc[2,0],df.iloc[5,0],df.iloc[12,0],df.iloc[21,0] = 'Dadri','Gurgaon','Mahendragarh','Yamuna Nagar'

    #Creating the Choropleth
    global har
    har = folium.Map(location=[29.0588,76.0856],zoom_start=8)
    # folium.LatLngPopup().add_to(har)
    folium.Choropleth(geo_data='C:/Users/Yash/jupyter notebooks/json files/haryana.geojson',
                      data=df,
                      columns=['Districts',v.get()],
                      key_on='feature.properties.Dist_Name',
                      fill_color='YlOrRd',
                      bins = 8,
                      fill_opacity=0.7,
                      legend_name=v.get(),
                      name='haryana geojson',
                      highlight=True).add_to(har)
    har.fit_bounds([[27.8244,74.6082],[30.8106,78.2556]])
    
    #Plotting Markers
    coordinates = [[30.3752,76.7821],[28.7975,76.1322],[28.5921,76.2653],[28.4089,77.3178],[29.5132,75.4510],
                [28.4595,77.0266],[29.1492,75.7217],[28.6055,76.6538],[29.3255,76.2998],[29.8043,76.4039],
                [29.6857,76.9905],[29.9695,76.8783],[28.2734,76.1401],[28.1024,76.9931],[28.1473,77.3260],
                [30.6942,76.8606],[29.3909,76.9635],[28.1920,76.6191],[28.8955,76.6066],[29.5321,75.0318],
                [28.9931,77.0151],[30.1290,77.2674]]

    #For icons            
    rang = max(df[v.get()]) - min(df[v.get()])
    step = rang/8
    binss = np.arange(min(df[v.get()]),max(df[v.get()]),step,dtype=np.float)  
    df.set_index('Districts',drop=True,inplace=True)          

    #Opening data for plotting line charts
    Df = pd.read_excel('C:/Users/Yash/SUblime files/Haryana Covid Project/flattened_dataset.xlsx')
    Df.drop(columns='Unnamed: 0',inplace=True)

    #Plotting the markers
    for (coor,dist,value) in zip(coordinates,df.index,df[v.get()]):
      if df.loc[dist,v.get()] <= binss[2]:
        ico_color ='green'
      elif binss[2]<df.loc[dist,v.get()]<=binss[5]:
        ico_color ='orange'
      else:
        ico_color ='red'
      #Creating the line charts for various districts
      c = alt.Chart(Df[['Dates','Variable',dist]]).mark_line().encode(
        x='Dates',
        y=alt.Y(dist,axis=alt.Axis(title='Count / Percentage')),
        color=alt.Color('Variable',legend=alt.Legend(title='July/August')))

      html = c.to_html()
      iframe = branca.element.IFrame(html=html, width=700, height=370)
      pop = folium.Popup(iframe, max_width=550)

      folium.Marker(location=coor,tooltip=f"<b>{dist}</b> {v.get()[6:]} : {value}",
        icon=folium.Icon(icon='info',icon_color='white',prefix='fa',color=ico_color),popup=pop).add_to(har)

#BUTTONS
    
#select date button
img1 = tk.PhotoImage(file='C:/Users/Yash/Sublime files/Haryana Covid Project/Icons/calendar final 1.png')
sel_date_button = tk.Button(master=bottom_frame,image=img1,text='Select Date',compound='left',bd=4,bg='white',width=150,height=80,
                        font=("Gabriola", 20, "bold"),activebackground='light green',cursor='hand2')
sel_date_button.pack(ipadx=42,ipady=0,padx=31,pady=20,side='left',expand=True)

#plot map button
img2 = tk.PhotoImage(file= 'C:/Users/Yash/Sublime files/Haryana Covid Project/Icons/play 2.png')
plot_button = tk.Button(master=bottom_frame,image=img2,text='Plot Map',compound='left',bd=4,bg='white',width=150,height=80,
  font=("Gabriola", 20, "bold"),activebackground='light green',command=lambda : decorator(download_map),cursor='hand2')
plot_button.pack(ipadx=42,ipady=0,padx=23,pady=20,side='left',expand=True)

#save map button
img3 = tk.PhotoImage(file='C:/Users/Yash/Sublime files/Haryana Covid Project/Icons/download red final.png')
save_map_button = tk.Button(master=bottom_frame,image=img3,text='Download',font=("Gabriola", 20, "bold"),bg='white',width=150,height=80,
                              compound='left',command=download_map_window,activebackground='light green',bd=4,cursor='hand2')
save_map_button.pack(ipadx=42,ipady=0,padx=25,pady=20,side='left',expand=True)

root.mainloop()

