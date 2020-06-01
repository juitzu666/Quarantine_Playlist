#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 
Group 4 - Padmil Khandelwal/ Pooja Puvvadi/ Jui Tzu Wang

This file returns book recommendations and the number of left over minutes
based on input of how much time to spend reading and book genre preferences

This module is imported by quarantine_playlist
This module takes in the book data excel file
"""

import pandas as pd 


#genres =["Combined Print & E-Book Fiction"];

#Format Messages
def create_output_message (data,output):
    message=" "
    if isinstance(data, pd.DataFrame):
        message+=str(data['Title'].values[0].title())+" "
        if (str(data['Author']) == ""):
            message+="by unknown "
        else:
            message+="by "+str(data['Author'])+" "
        message+="of genre "+str(data['Genre'].values[0])+" "
    else:
        message+=str(data['Title'].title())+" "
        if (str(data['Author']) == ""):
            message+="by unknown "
        else:
            message+="by "+str(data['Author'])+" "
        message+="of genre "+str(data['Genre'])+" "
    return message
        
        
#generate book recommendations     
def generate_recommedations(mins,genres):
    
    df_data=pd.read_excel("Merged_Book_Data.xlsx")
    
    # del df_data['Unnamed: 0']
    
    df_data['Time'] = df_data['Time'] * 60
    
    # df_data.sort_values(by=['rank'],inplace=True)
    
    sum_minutes = (df_data['Time'] * 60).sum()
    
    total_hours = sum_minutes/60
    rows=[]
    mins_left=mins
    for i,j in df_data.sample(frac=1).iterrows():
        if mins_left>0 and mins_left>=j['Time']:
            output={}
            for genre in genres:
                if(genre ==j['Genre']):
                    output['category']="books"
                    output['item_name']=j['Title']
                    output['genre']=genre
                    output['minutes']=(j['Time'])
                    output['output_message']=create_output_message(j,output)
                    mins_left -= (j['Time'])
#                    print("!",output)
                    rows.append(output)
                    break
                
    #if genre condition is not enough for minutes required 
    if(mins_left>=48):
        for i,j in df_data.sample(frac=1).iterrows():
            if mins_left>0 and mins_left>=j['Time']:
                output={}
                output['category']="books"
                output['item_name']=j['Title']
                output['genre']=j['Genre']
                output['minutes']=(j['Time'])
                output['output_message']=create_output_message(j,output)
                mins_left-=(j['Time'])
                rows.append(output)
    #print("Minutes Left ",mins_left)
    return rows, (mins_left / 60)




