#%%
import json
import requests
import pandas as pd
from dateutil import parser

address_df = pd.read_csv ("C:\\Users\\Nadz\\Documents\\UiPath\\Web Scraping with Randy\\excel\\Philadelphia Houses for Sale.csv")

google_apikey = open('GoogleApiKey.txt').read()
#%%



#iterating each row in address dataframe
for index, row in address_df.iterrows():
    print(row['House Address'])
    to_addr = '1400 JFK Boulevard, Philadelphia, PA 19107'
    from_addr = row['House Address']

    #establishing departure time
    dep_time = int(parser.parse("Aug 14 2020 04:30PM").timestamp())  
   
    #API URL
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={from_addr}&destination={to_addr}&departure_time={dep_time}&key={google_apikey}"
    #print (url)

    api_response = requests.get(url).json()
    #
    open("API.json", "w").write(json.dumps(api_response))
    
    routes = api_response["routes"]

    #record duration if a route exists
    if len(routes) > 0:
        j = routes[0]
        st_latitude = j["legs"][0]["start_location"]["lat"]
        st_longitude = j["legs"][0]["start_location"]["lng"]
        latitude = j["legs"][0]["end_location"]["lat"]
        longitude = j["legs"][0]["end_location"]["lng"]
        duration = j["legs"][0]["duration_in_traffic"]["value"]

        print('Driving duration is', duration/60, 'minutes')
        #creating new columns
        address_df.loc[index,'Travel Duration'] = duration/60
        address_df.loc[index,'Start Latitude'] = st_latitude
        address_df.loc[index,'Start Longitude'] = st_longitude
        address_df.loc[index,'Latitude'] = latitude
        address_df.loc[index,'Longitude'] = longitude
        

#%%
   address_df.to_csv('Philly_Commutes.csv')


    
    



#%%
address_df



# %%
