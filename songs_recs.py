# -*- coding: utf-8 -*-
"""
@author: 
Group 4 - Padmil Khandelwal/ Pooja Puvvadi/ Jui Tzu Wang

This file returns song recommendations based on input of how much time
is left over from creating recommendations of books and tv shows

This module is imported by quarantine_playlist
This module takes in the song data excel file
"""


import pandas as pd
#import web_scraping
 


#web_scraping.scrape_song_data()




# songs max = 199 minutes
genres=['pop','rnb'];
doc={
     "category":"songs",
     "item_name":"songs_artist",
     "genre":"x",
     "minutes":67,
     "info":"url",
     "output_message":"see here"}

# Creates output message
def create_output_message (data,output):
    message=" "
    if isinstance(data, pd.DataFrame):
        message+=str(data['song_name'].values[0].title())+" "
        message+="by "+str(data['artist'].values[0].title())+" "
        message+="of genres "+str(data['genre_tags'].values[0])+" "
        message+="available at "+str(data['lastfm_url'].values[0])+" "
    else:
        message+=str(data['song_name'].title())+" "
        message+="by "+str(data['artist'].title())+" "
        message+="of genre "+str(output['genre'])+" "
        message+="available at "+str(output['info'])+" "
    return message
        
        
        
# Get song recommendations based on user input

def generate_recommedations(mins,genres):
    df_data=pd.read_excel("songs_merged.xlsx")

    del df_data['Unnamed: 0']
    
    df_data['duration']= df_data['duration']/(60*1000)
    
    df_data.sort_values(by=['rank'],inplace=True)
    
    sum_minutes=df_data['duration'].sum()

    total_hours=sum_minutes/60
    rows=[]
    song_list=[]
    mins_left=mins
    for i,j in df_data.iterrows():
        if mins_left>0 and mins_left>=j['duration']:
            output={}
            for genre in genres:
                if(genre.lower() in str(j['genre_tags']).lower().split(", ")):
                    output['category']="songs"
                    output['item_name']=j['song_name']
                    output['genre']=genre
                    output['minutes']=j['duration']
                    output['info']=j['lastfm_url']
                    output['output_message']=create_output_message(j,output)
                    mins_left-=j['duration']
                    rows.append(output)
                    song_list.append(j['song_name'])
                    break
                
    #if genre condition is not enough for minutes required 
    if(mins_left>3.3):
        for i,j in df_data.iterrows():
            if mins_left>0 and mins_left>=j['duration'] and (j['song_name'] not in song_list) :
                output={}
                output['category']="songs"
                output['item_name']=j['song_name']
                output['genre']=j['genre_tags']
                output['minutes']=j['duration']
                output['info']=j['lastfm_url']
                output['output_message']=create_output_message(j,output)
                mins_left-=j['duration']
                song_list.append(j['song_name'])
                rows.append(output)
                
    #add the minimum duration song if duration of that song is within mins left + 10% of total time left
    elif mins_left>0 and len(rows)<2:
        j=df_data[df_data['duration']==df_data['duration'].min()]
        if(j['duration'].values[0]<(mins_left+(0.1*mins))): 
            output={}
            output['category']="songs"
            output['item_name']=j['song_name'].values[0]
            output['genre']=j['genre_tags'].values[0]
            output['minutes']=j['duration'].values[0]
            output['info']=j['lastfm_url'].values[0]
            output['output_message']=create_output_message(j,output)
            mins_left=0
#            print("%",output)
            rows.append(output)
            song_list.append(j['song_name'])
    #print("Minutes Left ",mins_left)
    return rows   


        
