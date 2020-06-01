#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
THE QUARNTINE PLAYLIST

Created on Wed Apr 29 15:02:24 2020

Group 4 - Padmil Khandelwal/ Pooja Puvvadi/ Jui Tzu Wang

This is the main file to be run by the user.

This file imports the web_scraping, EDA_combine, tv_show_recs, songs_recs,
and books_recs modules.
"""

import pandas as pd
import books_recs as bm #load book recommendations module
import songs_recs as sr #load songs recommendations module
import tv_show_recs as tvsr #load TV Show recommendations module
import matplotlib.pyplot as plt
import EDA_combine #load EDA module
import web_scraping #load web scraping module
import warnings
warnings.filterwarnings("ignore")

scrapeData=False #can set to True if you want to web scrape


# Scrape Data from Web Scraping 
if(scrapeData):
    #Scrapes data for all three categories
    web_scraping.scrape_all_data()    


EDA_combine.EDA_across_all_categories()

# Get user name:
user_name = input ("Enter your name:") 
print(user_name) 

print("Hi",user_name," answer a few questions to create a customised Quarantine Playlist for you ")

# Get hours of playlist to be created:
negative_hours = True

while negative_hours:
    try:
        (hours_to_spend) = input("Enter hours you want to create for the playlist: ") 
        if(float(hours_to_spend)) <= 0:
            print("Please enter a number more than 0.")
        else:
            print(float(hours_to_spend))
            negative_hours = False
    except ValueError:
        print("Not valid float. Please try again.")

# Get propotion of preference - only ask for tv show, and deduct from 100(%) to get book's propotion
invalid_input_percentage = True
while invalid_input_percentage:
    try:
        prop_to_spend_tvshow = input("Enter percentage (0-100) of playlist time you want to spend on TV shows: ") 
        if (float(prop_to_spend_tvshow)) > 100 or (float(prop_to_spend_tvshow)) <0 :
            print("input out of bound - select again!")
        else:
            hours_to_spend_tvshow = round(float(hours_to_spend)*float(prop_to_spend_tvshow)/100)
            print(float(prop_to_spend_tvshow), '%') 
            print("You choose to spend ",hours_to_spend_tvshow, " hours on TV Shows")

            prop_to_spend_book = 100 - float(prop_to_spend_tvshow)
            hours_to_spend_book = round(float(hours_to_spend)*prop_to_spend_book/100)
            print(prop_to_spend_book, '%') 
            print("You choose to spend ",hours_to_spend_book, " hours on books")
            invalid_input_percentage = False
    except ValueError:
        print("Not valid float. Please try again.")


# Get Show Genre:

df_data=pd.read_excel("export_dataframe_show_merged.xlsx")
show_gen_list = []
show_gen_list_unique = []
for i in df_data['Show_New_Genre'].str.split(';'):
    for g in i:
        show_gen_list.append(g.strip())
        
show_gen_list_unique = list(set(show_gen_list))

show_dic = {k:v for k,v in zip(range(1,len(show_gen_list_unique)+1),show_gen_list_unique)}


def show_gen(i):
    switcher = show_dic
    show_gen_switch.append(switcher.get(i, "Invalid selection"))
    return switcher.get(i, "Invalid selection")

#show user what each number represent:
print("Below is the options for show genre:")
for k,v in show_dic.items():
    print("option:", k, "= genre: ", v)

show_gen_switch = []


# First choice:
show_gen_wrong = True
while (show_gen_wrong):
    try:
        show_gen_selection_first = input("Enter 1 to 8 to select the show genre your first choice of show genre: ")
        if(int(show_gen_selection_first) not in range(1,len(show_gen_list_unique)+1)):
            print("input out of bound - select again!")
        else:
            show_gen(int(show_gen_selection_first))
            show_gen_wrong = False
    except ValueError:
        print("Not valid integer. Please try again.")
        
# Second choice:
show_gen_wrong = True
while (show_gen_wrong):
    try:
        show_gen_selection_second = input("Enter 1 to 8 to select show_gen_list_unique show genre your second choice of show genre: ")
        if(int(show_gen_selection_second) not in range(1,len(show_gen_list_unique)+1)):
            print("input out of bound - select again!")
        else:
            show_gen(int(show_gen_selection_second))
            show_gen_wrong = False
    except ValueError:
        print("Not valid integer. Please try again.")
print(show_gen_switch)

# Get book genre:

df_data=pd.read_excel("Merged_Book_Data.xlsx")
book_gen_list = list(set(df_data['Genre']))
book_dic = {k:v for k,v in zip(range(1,len(book_gen_list)+1),book_gen_list)}

def book_gen(i):
    switcher = book_dic
    book_gen_switch.append(switcher.get(i, "Invalid selection"))
    return switcher.get(i, "Invalid selection")

#show user what each number represent:
print("Below is the options for book genre:")
for k,v in book_dic.items():
    print("option:", k, "= genre: ", v)
book_gen_switch = []


# First choice:
book_gen_wrong = True
while (book_gen_wrong):
    try:
        book_gen_switch_first = input("Enter 1 to 18 to select the show genre your first choice of book genre: ")
        if(int(book_gen_switch_first) not in range(1,len(book_gen_list)+1)):
            print("input out of bound - select again!")
        else:
            book_gen(int(book_gen_switch_first))
            book_gen_wrong = False
    except ValueError:
        print("Not valid integer. Please try again.")
        
# Second choice:
book_gen_wrong = True
while (book_gen_wrong):
    try:
        book_gen_switch_second = input("Enter 1 to 18 to select the show genre your second choice of book genre: ")
        if(int(book_gen_switch_second) not in range(1,len(book_gen_list)+1)):
            print("input out of bound - select again!")
        else:
            book_gen(int(book_gen_switch_second))
            book_gen_wrong = False
    except ValueError:
        print("Not valid integer. Please try again.")

print(book_gen_switch)

# Get music genre:
song_gen_list = ['Hip-Hop', 'Pop', 'RnB', 'Country', 'Dance', 'Disco', 'Other']  #to be used in the dropdown menu
song_dic = {k:v for k,v in zip(range(1,len(song_gen_list)+1),song_gen_list)}


def song_gen(i):
    switcher = song_dic
    song_gen_switch.append(switcher.get(i, "Invalid selection"))
    return switcher.get(i, "Invalid selection")

#show user what each number represent:
print("Below is the options for song genre:")
for k,v in song_dic.items():
    print("option:", k, "= genre: ", v)

song_gen_switch = []

# First choice:
song_gen_wrong = True
while (song_gen_wrong):
    try:
        song_gen_switch_first = input("Enter 1 to 7 to select the show genre your first choice of song genre: ")
        if(int(song_gen_switch_first) not in range(1,len(song_gen_list)+1)):
            print("input out of bound - select again!")
        else:
            song_gen(int(song_gen_switch_first))
            song_gen_wrong = False
    except ValueError:
        print("Not valid integer. Please try again.")

# Second choice:
song_gen_wrong = True
while (song_gen_wrong):
    try:
        song_gen_switch_second = input("Enter 1 to 7 to select the show genre your second choice of song genre: ")
        if(int(song_gen_switch_second) not in range(1,len(song_gen_list)+1)):
            print("input out of bound - select again!")
        else:
            song_gen(int(song_gen_switch_second))
            song_gen_wrong = False
    except ValueError:
        print("Not valid integer. Please try again.")

print(song_gen_switch)

# Print summary of what user has chosen
print('---Summary---')
print("User Name: ", user_name)
print("Total hours of the playlist to be created: ", hours_to_spend)
print("You choose to spend ",hours_to_spend_tvshow, " hours on TV Shows")
print("You choose to spend ",hours_to_spend_book, " hours on books")
print("Your top 2 choices of TV Show genres are: ") 
for i in show_gen_switch:
    print(i)
print("Your top 2 choices of book genres are: ") 
for i in book_gen_switch:
    print(i)
print("Your top 2 choices of song genres are: ") 
for i in song_gen_switch:
    print(i)

# Get recommendations from all recommendation modules
tv_recs, tv_min_left = tvsr.show_recom((hours_to_spend_tvshow * 60),show_gen_switch)
tv_recs_df=pd.DataFrame(tv_recs)

book_recs, b_hours_left = bm.generate_recommedations((hours_to_spend_book * 60),book_gen_switch)
book_recs_df=pd.DataFrame(book_recs)

songs_min = (b_hours_left * 60) + tv_min_left
song_recs_df = pd.DataFrame(sr.generate_recommedations(songs_min,song_gen_switch))

#Concatinate all recommendations in one
all_recommendations=pd.concat([tv_recs,book_recs_df,song_recs_df],ignore_index=True)

print()
print("***********************************************************")
print("                           TV Shows")
print("************************************************************")
for i,j in tv_recs_df.iterrows():
    #print("-------------------------------------------------------")
    print(i+1,". ",j['output_message'])
    print("-------------------------------------------------------")

print()
print("***********************************************************")
print("                           Books")
print("***********************************************************")
for i,j in book_recs_df.iterrows():
    #print("-------------------------------------------------------")
    print(i+1,". ",j['output_message'])
    print("-------------------------------------------------------")
    
print()    
print("***********************************************************")
print("                           Songs")
print("***********************************************************")
for i,j in song_recs_df.iterrows():
    #print("-------------------------------------------------------")
    print(i+1,". ",j['output_message'])
    print("-------------------------------------------------------")


# Show graphs to user based on recommendations given

# Graph of how many of each type of media
df_media_count = pd.DataFrame({'Media':['TV Shows', 'Books', 'Songs'], 
                   'Count':[len(tv_recs_df.index), len(book_recs_df.index), len(song_recs_df.index)]})
plot_media_count =  df_media_count.plot.bar(x='Media', y='Count', rot=90, color = ['b', 'r', 'g'])
plt.title("Count of each category recommeneded ")
plt.show()


# Graph of time spent on each type of media
df_time_spent = pd.DataFrame({'Media':['TV Shows', 'Books', 'Songs'], 
                   'Hours':[(hours_to_spend_tvshow - (tv_min_left / 60)), 
                            (hours_to_spend_book - b_hours_left), (((b_hours_left * 60) + tv_min_left) / 60)]})
plot_time_spent =  df_time_spent.plot.bar(x='Media', y='Hours', rot=90, color = ['b', 'r', 'g'])
plt.title("Hours of each category recommeneded ")
plt.show()



