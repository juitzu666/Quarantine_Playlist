#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 
Group 4 - Padmil Khandelwal/ Pooja Puvvadi/ Jui Tzu Wang

This file returns tv show recommendations and the number of left over minutes
based on input of how much time to spend watching and tv show genre preferences

This module is imported by quarantine_playlist
This module takes in the tv show data excel file
"""

import pandas as pd
#import web_scraping
 


#web_scraping.scrape_tvshows_data()



# mins = 360
#genres = ['Crime','Comedy']

def get_master_recomm(mins,genre,df):
    rows = []
    for i,j in df.iterrows():
            output = {}
            for gen in genre:
                if(gen in j['Show_New_Genre'].split('; ')):
                    output['category'] = 'TV_SHOW'
                    output['item_name'] = j['Show_New_Name']
                    output['genre'] = gen
                    output['minutes'] = j['Total_minutes_need_to_finish_all_episodes']
                    output['info'] = j['Show_Intro']
                    output['output_message'] =output['item_name']+" IMDB Rating of "+ str(j['Show_IMDB_Rating'])
                    rows.append(output)
                    break
    #master recommendation list
    
    recommendation_df=pd.DataFrame(rows)
    return recommendation_df

#Get recommendations based on user preferences
#to return: show_name, no. of episodes to watch, duration time, other msg (imdb rating/intro)
def show_recom(mins,genres):
    show_result_df_new=pd.read_excel("export_dataframe_show_merged.xlsx")


    col_need_for_recom = ['Ranking', 'Show_New_Name', 'Show_New_Genre','Number_of_Season', 'Number_of_Episode', 'Show_IMDB_Rating',
           'Total_hours_need_to_finish_all_episodes','Show_Intro']
    
    show_result_df_new_recom = show_result_df_new[col_need_for_recom]
    show_result_df_new_recom['Total_minutes_need_to_finish_all_episodes'] = show_result_df_new_recom['Total_hours_need_to_finish_all_episodes']*60
    show_result_df_new_recom.sort_values(by=['Ranking'])

    recommendation_df=get_master_recomm(mins,genres,show_result_df_new_recom)
 
    sum_time_recommend=recommendation_df['minutes'].sum()
    recommend_min_time=recommendation_df[recommendation_df['minutes']==recommendation_df['minutes'].min()]
    
    final_list=[]
    min_left = mins
    actual_min=0   
    added=[]   
    if min_left<=sum_time_recommend:
        for i,j in recommendation_df.iterrows(): 
            if min_left>0 and min_left>recommend_min_time['minutes'].values[0] : 
                #if full season fits
                if(min_left>j['minutes'] and j['item_name'] not in added):
                    output={}
                    output['category'] = 'TV_SHOW'
                    output['item_name'] = j['item_name']
                    output['genre'] =  j['genre']
                    output['minutes'] =  j['minutes']
                    output['info'] =  j['info']
                    output['output_message'] =j['output_message'];       
                    final_list.append(output)
                    actual_min+=float(j['minutes'])
                    added.append(j['item_name'])
                    min_left-=float(j['minutes'])

                #divide into episodes
                elif(j['item_name'] not in added):
                    output={}
                    print("outside",min_left,j['minutes'])
                    temp=show_result_df_new_recom[show_result_df_new_recom['Show_New_Name']==j['item_name']]
                    num_of_episodes=temp['Number_of_Episode'].values[0]
                    season_mins=temp['Total_minutes_need_to_finish_all_episodes'].values[0]
                    mins_per_episode=season_mins/num_of_episodes
                    no_episodes=min_left//mins_per_episode
                    output['Category'] = 'TV_SHOW'
                    output['item_name'] = j['item_name']
                    output['genre'] =  j['genre']
                    output['minutes'] = (no_episodes)*mins_per_episode
                    output['info'] =  j['info']
                    output['output_message'] =str(j['output_message'])+" Number of Episodes :"+str(no_episodes);       
                    final_list.append(output)
                    added.append(j['item_name'])
                    actual_min+=(no_episodes)*mins_per_episode
                    min_left=0
        
        #ADD LOWEST     
        if min_left>0 and min_left<recommend_min_time['minutes'].values[0] and recommend_min_time['item_name'].values[0] not in added :
            temp_output=recommend_min_time
            temp=show_result_df_new_recom[show_result_df_new_recom['Show_New_Name']==recommend_min_time['item_name'].values[0]]
            num_of_episodes=temp['Number_of_Episode'].values[0]
            season_mins=temp['Total_minutes_need_to_finish_all_episodes'].values[0]
            mins_per_episode=season_mins/num_of_episodes
            no_episodes=min_left//mins_per_episode
            output={}    
            output['category'] = 'TV_SHOW'
            output['item_name'] = temp_output['item_name'].values[0]
            output['genre'] =  temp_output['genre'].values[0]
            output['minutes'] = (no_episodes)*mins_per_episode
            output['info'] =  temp_output['info'].values[0]
            output['output_message'] =str(temp_output['output_message'].values[0])+" Number of Episodes :"+str(no_episodes)
            final_list.append(output)
            actual_min+=(no_episodes)*mins_per_episode
            min_left=0
        df_new=pd.DataFrame(final_list)
        #print("LEFT ",str(mins-actual_min)) 
        return df_new, float(mins-actual_min)
    else:    
        #Add recommendation_df in list
        apply_list=[recommendation_df]
        min_left-=sum_time_recommend
        actual_min+=sum_time_recommend
        added=list(recommendation_df['item_name'].unique())
        rows=[]
        for i,j in show_result_df_new_recom.iterrows():
            if(min_left>0 and j['Show_New_Name'] not in added):
                if(j['Total_minutes_need_to_finish_all_episodes']<min_left):
                    output={}
                    output['category'] = 'TV_SHOW'
                    output['item_name'] = j['Show_New_Name']
                    output['genre'] = j['Show_New_Genre']
                    output['minutes'] = j['Total_minutes_need_to_finish_all_episodes']
                    output['info'] = j['Show_Intro']
                    output['output_message'] =output['item_name']+" IMDB Rating of "+ str(j['Show_IMDB_Rating'])
                    rows.append(output)
                    added.append(output['item_name'])
                    actual_min+= output['minutes']
                    min_left-= output['minutes']
                #BREAK THE SEASON
                else:
                    output={}
                    temp=j
                    num_of_episodes=temp['Number_of_Episode']
                    season_mins=temp['Total_minutes_need_to_finish_all_episodes']
                    mins_per_episode=season_mins/num_of_episodes
                    no_episodes=min_left//mins_per_episode
                    output['category'] = 'TV_SHOW'
                    output['item_name'] = j['Show_New_Name']
                    output['genre'] = j['Show_New_Genre']
                    output['minutes'] = j['Total_minutes_need_to_finish_all_episodes']
                    output['info'] = j['Show_Intro']
                    output['output_message'] =output['item_name']+" IMDB Rating of "+ str(j['Show_IMDB_Rating'])+" Number of Episodes :"+str(no_episodes)
                    actual_min+=(no_episodes)*mins_per_episode
                    rows.append(output)
                    added.append(output['item_name'])
                    min_left=0
        apply_list.append(pd.DataFrame(rows))            
        df_new=pd.concat(apply_list)
        #print("LEFT ",str(mins-actual_min)) 
        return df_new, float(mins-actual_min)
   
   
  
# output, left_min =show_recom(35000,genres)
# output=output.reset_index(drop=True)
# display(output,left_min )
# output.sum()


