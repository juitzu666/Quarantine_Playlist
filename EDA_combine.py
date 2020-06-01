#!/usr/bin/env python
# coding: utf-8
"""
@author: 
Group 4 - Padmil Khandelwal/ Pooja Puvvadi/ Jui Tzu Wang

This file outputs EDA of all the media categories

This module is imported by quarantine_playlist
This module takes in the excel files of show data, book data, and music data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager
# WordCloud
# ref: https://www.datacamp.com/community/tutorials/wordcloud-python
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator



# Creates graphs based for individual media categories
def EDA_across_all_categories():
## Below are EDA for TV Show category:

    df_data_show=pd.read_excel("export_dataframe_show_merged.xlsx")
    df_data_book=pd.read_excel("Merged_Book_Data.xlsx")
    df_data_song=pd.read_excel("songs_merged.xlsx")
    ## What are the most common genre of the top 10 TV Shows?
    genre_list = df_data_show['Show_New_Genre'].str.split(';')

    g_full_list = []
    for i in df_data_show['Show_New_Genre'].str.split(';'):
        for g in i:
            g_full_list.append(g.strip())

    (unique, counts) = np.unique(g_full_list, return_counts=True)
    frequencies = np.asarray((unique, counts)).T


    gen_count_dict = {k:v for k,v in frequencies}

    g_df = pd.DataFrame(gen_count_dict.items(), columns = ['Genre','Count'])
    g_df['Count'] = g_df['Count'].astype(int)

    fig, ax = plt.subplots(figsize = (12,6))


    sns.barplot('Genre', 'Count', data=g_df, label = 'count_by_genre', ax = ax)

    ax.set_title("Top_10_TV_Shows_Count_By_Genre")
    ax.set_ylabel("Count_appears_in_top_10_TV_Shows")
    ax.set_ylim(ymin = min(g_df['Count']) -1, ymax = (max(g_df['Count']))+1)
    ax.set_xlabel("TV Show Genre Type")
    ax.set_xticklabels(g_df['Genre'], rotation=45)


    ## Correlation table
    corr = (df_data_show.corr())
    #ref:https://seaborn.pydata.org/generated/seaborn.heatmap.html
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(10, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=.3, square=True, cmap="YlGnBu")
        plt.title("Correlation Between every column in TV Show Data")
        plt.show()
        


    ## WordCloud
    text = " ".join(info for info in df_data_show['Show_Intro'])
    print ("There are {} words in the combination of all show intro.".format(len(text)))

    # Create stopword list:
    stopwords = set(STOPWORDS)
    # Based on observing of the data, additional stop words are added.
    stopwords.update(["movie","show","TV","will","one","series","shows","watch","episode","year","years","scene","scenes","re","sometimes"])

    # Generate a word cloud image
    wordcloud = WordCloud(stopwords=stopwords, background_color="white", width = 1500, height = 1000).generate(text)

    # Display the generated image:
    # the matplotlib way:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title("WordCloud for TV Show information")
    plt.show()

    ## EDA for book category
    gen_mean = df_data_book.groupby('Genre')['Time'].mean()

    # Plot genre vs. time it takes to read each genre
    plot_gen_time = gen_mean.plot.bar(x = 'Genre', y = 'Time', rot = 90)
    plt.title("Average Time It Takes to Read Each Genre")
    plt.show()

    auth_count = df_data_book['Author'].value_counts().nlargest(15)

    index = auth_count.index[1:]
    vals = auth_count.values[1:]

    df = pd.DataFrame({'Author':index, 'Count':vals})
    # Plot most popular authors
    plot_auth_count =  df.plot.bar(x='Author', y='Count', rot=90)
    plt.title("Book Count by Author")
    plt.show()


    ## Below are EDA for song category:
    del df_data_song['Unnamed: 0']

    #Covert Duration to Minutes

    df_data_song['duration']= df_data_song['duration']/(60*1000)

    # Plot average duration of songs
    sns.boxplot(x=df_data_song["duration"])
    plt.title("Box Plot for Duration ( in minutes )")
    plt.show()


    # plot playcount vs. rank of song
    sns.scatterplot(x=df_data_song['playcount'], y=df_data_song['rank'])
    plt.title("Scatter Plot Playcount vs Rank")
    plt.show()
    
    print("Correlation between every column")
    pearsoncorr = df_data_song.corr(method='pearson')

    plt.subplots(figsize=(10,10))      
    sns.heatmap(pearsoncorr, 
                square=True,
                cmap='RdBu_r',
                annot=True)  
    plt.show()



    artis_value_counts=df_data_song['artist'].value_counts()[df_data_song['artist'].value_counts()>1]
    artist_songs=pd.DataFrame(artis_value_counts)
    artist_songs=artist_songs.reset_index()
    artist_songs.columns=['artist','count']
    sns.barplot(x="count", y="artist",data=artist_songs)
    plt.ylabel("Artist Name")
    plt.title("Artist that appear more than once in Hot 100")
    plt.show()





