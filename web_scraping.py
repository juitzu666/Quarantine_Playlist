# -*- coding: utf-8 -*-
"""
@author: 
Group 4 - Padmil Khandelwal/ Pooja Puvvadi/ Jui Tzu Wang

This file contains the code for all of the web scraping

This module is imported by quarantine_playlist
"""


import pandas as pd
from bs4 import BeautifulSoup
import requests
import urllib.parse
from urllib.request import urlopen 
import requests
import json
import re
import statistics as s

#Add your API Key of last fm here : 
api_key="ed32d9c97313e194ffb67eca9973ff40"

# Uses Billboard Hot 100 chart to fetch the 100 songs
# Then uses Last fm api to fetch metadata of songs
def scrape_song_data():
    #meta data
    page = requests.get("https://www.billboard.com/charts/hot-100")
    URL = "http://ws.audioscrobbler.com/2.0"
    reqformat='json'
    
    bsyc = BeautifulSoup(page.content, 'html.parser')
    params={'method':"track.getInfo",'api_key':api_key,'format':reqformat,'autocorrect':1}
    params_2={'method':"album.getinfo",'api_key':api_key,'format':reqformat,'autocorrect':1}
    
    #Scrape Data using Beautiful Soap    
    chart_parent=bsyc.find(class_='chart-list__elements')
    chart_list=chart_parent.find_all('li')
    
    list_ranks=[]
    list_ranks_raw=[]
    album_data_list=[]
    list_metadata=[]
    album_raw_list=[]
    list_metadata_raw=[]
    not_found_count=0
    
    for song_rank in chart_list:
        doc={}
        doc_raw={}
        doc_raw['rank']=song_rank.find('span',class_='chart-element__rank__number').contents
        doc_raw['artist']=song_rank.find('span',class_='chart-element__information__artist text--truncate color--secondary').contents
        doc_raw['song_name']=song_rank.find('span',class_='chart-element__information__song text--truncate color--primary').contents
    #    doc_raw={song_rank.find('span',class_='chart-element__rank__number'),song_rank.find('span',class_='chart-element__information__artist text--truncate color--secondary'),song_rank.find('span',class_='chart-element__information__song text--truncate color--primary')}
        params_new=params
        doc['rank']=song_rank.find('span',class_='chart-element__rank__number').contents[0]
        doc['artist']=song_rank.find('span',class_='chart-element__information__artist text--truncate color--secondary').contents[0]
        doc['song_name']=song_rank.find('span',class_='chart-element__information__song text--truncate color--primary').contents[0]
    #    fout.writelines([doc['rank']+","+doc['artist']+","+doc['song_name'],'\n'])
        list_ranks.append(doc)
        list_ranks_raw.append(doc_raw)
        params_new['track']=doc['song_name'].lower()
        params_new['artist']=doc['artist'].lower()
        if('featuring' in  params_new['artist']):
             params_new['artist']='various artists'
        r = requests.get(url = URL, params = params_new) 
        song_data = r.json() 
        list_metadata_raw.append(song_data)
        if('error' in song_data.keys()):
            not_found_count+=1
        else:
            song_data=song_data['track']
            artist_lastfm=song_data['artist']['name']
            artist_billboard= params_new['artist']
            duration=song_data['duration']
            lastfm_url=song_data['url']
            if('album' in song_data.keys()):
                doc_meta={}
                album_res={}
                album=song_data['album']['title']
                doc_meta['album_title']=album
                doc_meta['duration']=duration
                doc_meta['lastfm_url']=lastfm_url
                params_album=params_2
                doc_meta['artist']=artist_lastfm
                params_album['album']=album
                params_album['artist']=artist_lastfm
                doc_meta['playcount']=song_data['playcount']
                doc_meta['genre_tags']='NA'
                if('tag' in song_data['toptags']):
                    if(len(song_data['toptags']['tag'])>0):
                        temp= [tag['name'] for tag in song_data['toptags']['tag']]
                        doc_meta['genre_tags']=", ".join(temp)
                res = requests.get(url = URL, params = params_album) 
                doc_meta['song_name']=doc['song_name']
                list_metadata.append(doc_meta)            
                album_data = res.json()
                album_raw_list.append(album_data)
                if('error' not in album_data ):
                    album_res['song_name']=doc['song_name']
                    album_res['name']=album_data['album']['name']
                    album_res['artist_album']=album_data['album']['artist']
                    album_res['artist_fm']=artist_lastfm
                    album_res['tracks']=album_data['album']['tracks']['track']
                    album_res['album_tracks']=len(album_data['album']['tracks']['track'])
                    album_data_list.append(album_res)
                    
    #Create dataframes 
    ranks=pd.DataFrame(data=list_ranks)
    meta_data=pd.DataFrame(data=list_metadata)
    album_df=pd.DataFrame(data=album_data_list)
    ranks_raw=pd.DataFrame(data=list_ranks_raw)
    meta_data_raw=pd.DataFrame(data=list_metadata)
    album_df_raw=pd.DataFrame(data=list_metadata_raw)
    
    # Create an Excel 
    meta_data_raw.to_excel('songs_lastfm_meta_data_raw.xlsx',index=False)
    album_df_raw.to_excel('songs_lastfm_album_raw.xlsx',index=False)
    ranks_raw.to_excel('songs_billboard_rankings_raw.xlsx',index=False)
    ranks.to_excel('songs_billboard_rankings_clean.xlsx',index=False);
    meta_data.to_excel('songs_lastfm_meta_data_clean.xlsx',index=False)
    album_df.to_excel('songs_lastfm_album_clean.xlsx',index=False)
        
    merged_df=pd.merge(meta_data,ranks, on=['song_name','artist'],how='left')
    merged_df_full=pd.merge(merged_df,album_df,left_on=['song_name','artist'],right_on=['song_name','artist_album'],how='left')
    merged_df_full.to_excel('songs_merged.xlsx')

    return True

# Get data on top TV shows
def scrape_tvshows_data():
    html = urlopen('https://www.telltalesonline.com/27957/popular-tv-series/')

    bsyc = BeautifulSoup(html.read(), "lxml")

    show_container = bsyc.find('div', class_ = 'entry-content clearfix')
    show_name = show_container.findAll('h2')
    show_name_list = []
    show_intro = show_container.findAll('p') #start from show_intro[2]
    show_name_list = []
    for i in range(10):
        show_name_list.append(show_name[i].text)
    p_intro = [2,4,6,8,10,12,14,16,18,20]
    p_other_info = [3,5,7,9,11,13,15,17,19,21]
    show_intro_list = []
    for i in p_intro:
        show_intro_list.append(show_intro[i].text)
        
    genre_list = []
    year_runnning = []
    IMDB_rating = []

    for i in p_other_info:
        temp = show_intro[i]
        # get genre
        temp_genre = temp.findAll('span', attrs={'class':'itemprop'})
        genre_for_this_show = [g.text for g in temp_genre]
        genre_list.append(genre_for_this_show)
        
        # get year running
        temp_strong = temp.find_all('strong')

        if i == 5:
            year_for_this_show = temp_strong[3].next_sibling #this parg forth strong tag is the Year Runnning tag
            year_runnning.append(year_for_this_show)
        else:
            year_for_this_show = temp_strong[1].next_sibling
            year_runnning.append(year_for_this_show)

        
        # get IMDB rating
        
        if i == 5:
            rate_for_this_show = temp_strong[5].next_sibling #this parg forth strong tag is the Year Runnning tag
            IMDB_rating.append(rate_for_this_show)
        else:
            rate_for_this_show = temp_strong[3].next_sibling
            IMDB_rating.append(rate_for_this_show)
            

    show_ranking = pd.DataFrame({'Show_Name': show_name_list, 
                                'Show_Genre': genre_list,
                                'Show_Year': year_runnning,
                                'Show_IMDB_Rating': IMDB_rating,
                                'Show_Intro': show_intro_list})

    # Export raw data to excel
    show_ranking.to_excel (r'export_raw_dataframe_show_ranking.xlsx', index = False, header=True)
    show_ranking_clean = show_ranking.copy()
    def get_name_only(ori_name):
        new_name = " ".join(re.findall("[a-zA-Z]+", ori_name))
        return new_name

    new_name_list = []
    for i in range(len(show_ranking_clean)):
        new_name_list.append(get_name_only(show_ranking_clean['Show_Name'][i]))


    def str_gen(original_list):
        string_gen = '; '.join(original_list) 
        return string_gen

    string_type_gen_list = []
    for i in range(len(show_ranking)):
                string_type_gen_list.append(str_gen(show_ranking['Show_Genre'][i]))


    def remove_reg_char(intro):
        intro=intro.replace("\xa0", " ")
        return intro

    show_ranking_clean['Show_Intro'] = show_ranking_clean['Show_Intro'].apply(remove_reg_char)

    # Data cleaning
    show_ranking_clean['Show_New_Name'] = new_name_list
    show_ranking_clean['Show_New_Genre'] = string_type_gen_list
    show_ranking_clean['Show_IMDB_Rating'] = show_ranking_clean['Show_IMDB_Rating'].str[:3]
    show_ranking_clean['Show_IMDB_Rating'] = show_ranking_clean['Show_IMDB_Rating'].astype(float)
    new_df_columns = ['Show_New_Name', 'Show_New_Genre', 'Show_Year', 'Show_IMDB_Rating',
        'Show_Intro']
    show_ranking_clean = show_ranking_clean[new_df_columns]
    # Export clean data to excel
    show_ranking_clean.to_excel (r'export_clean_dataframe_show_ranking.xlsx', index = False, header=True)

    #Source 2
    num_season = []
    num_episode = []
    show_to_search = ['https://en.wikipedia.org/wiki/Stranger_Things',
    'https://en.wikipedia.org/wiki/The_Walking_Dead_(TV_series)',
    'https://en.wikipedia.org/wiki/Game_of_Thrones',
    'https://en.wikipedia.org/wiki/American_Horror_Story',
    'https://en.wikipedia.org/wiki/Breaking_Bad',
    'https://en.wikipedia.org/wiki/Orange_Is_the_New_Black',
    'https://en.wikipedia.org/wiki/Friends',
    'https://en.wikipedia.org/wiki/Empire_(2015_TV_series)',
    'https://en.wikipedia.org/wiki/The_Vampire_Diaries',
    'https://en.wikipedia.org/wiki/The_Crown_(TV_series)',
    ]
    show_name = []
    num_season = []
    num_episode = []

    for s in range(len(show_to_search)):
        html_2 = urlopen(show_to_search[s])
        bsyc_2 = BeautifulSoup(html_2.read(), "lxml")
        tc_table_list = bsyc_2.findAll('table',
                        { "class" : "infobox vevent" } )
        tr_rows = []
        for row in tc_table_list[0].find_all('tr'):
            tr_rows.append(row)
    
        show_name.append(tr_rows[0].text)
        no_of_season = ''
        no_of_episodes = ''
        for i in range(len(tr_rows)):
            if(tr_rows[i].th is not None):
                if (tr_rows[i].th.text == 'No. of seasons'):
                    no_of_season = tr_rows[i].td.text
                    num_season.append(no_of_season)
                elif (tr_rows[i].th.text == 'No. of episodes'):
                    res = re.sub("\D", "", tr_rows[i].td.text) 
                    no_of_episodes = str(res)
                    num_episode.append(no_of_episodes)

    show_season_episode = pd.DataFrame({'Show_Name': show_name, 
                                'Number_of_Season': num_season,
                                'Number_of_Episode': num_episode})

    # Export raw data to excel
    show_season_episode.to_excel (r'export_raw_dataframe_show_season_episode.xlsx', index = False, header=True)

    # Data cleaning
    show_season_episode_clean = show_season_episode.copy()
    show_season_episode_clean['Number_of_Season'] = show_season_episode_clean['Number_of_Season'].astype(int)
    show_season_episode_clean['Number_of_Episode'] = show_season_episode_clean['Number_of_Episode'].astype(int)
    show_season_episode_clean['Total_hours_need_to_finish_all_episodes'] = show_season_episode_clean['Number_of_Episode']*42/60
    show_season_episode_clean['Average_hours_need_to_finish_a_season'] = show_season_episode_clean['Total_hours_need_to_finish_all_episodes']/show_season_episode_clean['Number_of_Season']

    # Export clean data to excel
    show_season_episode_clean.to_excel (r'export_clean_dataframe_show_season_episode.xlsx', index = False, header=True)

    # Merge 2 sources
    show_ranking_clean['Show_New_Name'] = show_ranking_clean['Show_New_Name'].str.upper()
    show_season_episode_clean['Show_Name'] = show_season_episode_clean['Show_Name'].str.upper()
    show_result_df = pd.merge(show_ranking_clean,show_season_episode_clean, left_on = 'Show_New_Name', right_on = 'Show_Name') 
    show_result_df['Ranking'] = (show_result_df.index)+1

    show_result_col = ['Ranking','Show_New_Name', 'Show_New_Genre', 'Show_Year', 'Number_of_Season', 'Number_of_Episode', 'Show_IMDB_Rating',
                    'Total_hours_need_to_finish_all_episodes','Average_hours_need_to_finish_a_season','Show_Intro']

    show_result_df_new = show_result_df[show_result_col]

    # Export merged data to excel
    show_result_df_new.to_excel (r'export_dataframe_show_merged.xlsx', index = False, header=True)

    return True

# Get data on top books       
def scrape_books_data():
    
    nytbsl = urlopen('https://www.nytimes.com/books/best-sellers/')

    bs_gen = BeautifulSoup(nytbsl.read(), "lxml")


    # Get links to each genre list
    weekly_BSL = bs_gen.findAll('div',
                        { "class" : "css-nl1pro" } )

    links = []
    genre = []

    for div in weekly_BSL[0].children:
        if div.name == 'div':
            for sub in div:
                if sub.name == "ul":
                    for x in sub.children:
                        for wname in x.children:
                            links.append(wname['href'])
                            genre.append(wname.contents[0])
                            
                            
    monthly_BSL = bs_gen.findAll('div',
                        { "class" : "css-30wn1p" } )

    for div in monthly_BSL[0].children:
        for mname in div:
            links.append(mname['href'])
            genre.append(mname.contents[0])
                    

    links_to_genre = dict(zip(genre.copy(), links.copy()))


    # Get isbns of each book in each genre

    gen_books = {}
    gen_isbn = {}

    column_names = ["link", "genre", "isbn"]
    raw_links_isbn = pd.DataFrame(columns = column_names)

    clean_links_isbn = pd.DataFrame(columns = ["Genre", "ISBN List"])

    for link in links_to_genre:
        gen_link = 'https://www.nytimes.com' + links_to_genre[link]
        gen_link_list = urlopen(gen_link)
        
        bs_books = BeautifulSoup(gen_link_list.read(), "lxml")

        isbn_list = bs_books.findAll('meta',
                                    {"itemprop" : "isbn"})
        
        
        isbn = []
        for x in isbn_list:
            try:
                isbn.append(x["content"])
            except:
                isbn.append(0)
        
        raw_links_isbn = raw_links_isbn.append({"link": gen_link, "genre" : link , "isbn" : isbn }, ignore_index=True)
        raw_links_isbn.to_excel (r'link_data.xlsx', index = False, header = True)
        
        isbn = isbn[1::2]
        gen_isbn[link] = isbn
        
        clean_links_isbn = clean_links_isbn.append({"Genre" : link , "ISBN List" : isbn }, ignore_index=True)
        clean_links_isbn.to_excel (r'clean_link_data.xlsx', index = False, header = True)

    # get book metadata
    gen_json = {}

    for gen in gen_isbn:
        isbns = []
        isbns = gen_isbn[gen]
        
        json_list = []
        for isbn in isbns:
            isbnurl = 'ISBN:' + str(isbn)
            url = 'https://openlibrary.org/api/books?bibkeys=' + isbnurl + '&jscmd=data&format=json'
            
            try: 
                response = requests.get(url)
                json_list.append(response.json())
            except:
                json_list.append({})
        
        gen_json[gen] = json_list

    book_file = open('books.txt', 'wt',
            encoding='utf-8')

    book_file.write(json.dumps(gen_json))

    book_file.close()

    format_books_data()
    
    return True
 
# Clean book data   
def format_books_data():

    book_file = open('books.txt', 'rt',
            encoding='utf-8')

    books_dict = json.loads(book_file.read())

    book_file.close()

    column_names = ["Title", "Genre", "Author", "Publish Date", "Pages", "Time"]

    books_df = pd.DataFrame(columns = column_names)

    raw_books_df = pd.DataFrame(columns = ["ISBN", "JSON"])

    column_names2 = ["Title", "Genre", "Author", "Publish Date", "Pages", "Time", "ISBN"]
    merge_data = pd.DataFrame(columns = column_names2)

    for gen in books_dict.copy():
        for i in books_dict[gen]:
            for b_json in i:
                raw_books_df = raw_books_df.append({"ISBN" : b_json, "JSON" : i[b_json] }, ignore_index=True)
    
    raw_books_df.to_excel (r'raw_book_data.xlsx', index = False, header = True)
            
    for gen in books_dict:
        for i in books_dict[gen]:
            for b_json in i:
                if int(b_json[5:]) != 0:
                    title = i[b_json]["title"]
                    genre = gen
                    
                    try:
                        author = i[b_json]["authors"][0]["name"]
                    except:
                        author = ""
                    
                    try:
                        pub_date = i[b_json]["publish_date"]
                    except:
                        publish_date = ""
                
                    try:
                        pages = i[b_json]["number_of_pages"]
                    except:
                        pages = 350  
                    
                    time = round(((pages * 2) / 60), 2)
                    
                    
                    books_df = books_df.append({"Title" : title, "Genre" : genre, "Author" : author, "Publish Date" : pub_date, "Pages" : pages, "Time" : time}, ignore_index=True)
                    merge_data = merge_data.append({"Title" : title, "Genre" : genre, "Author" : author, "Publish Date" : pub_date, "Pages" : pages, "Time" : time, "ISBN" : b_json[5:]}, ignore_index=True)

    # create excel files
    books_df.to_excel (r'book_data.xlsx', index = False, header = True)
    # merged, clean excel file
    merge_data.to_excel (r'Merged_Book_Data.xlsx', index = False, header = True)


# Output to show user what is being scraped
def scrape_all_data():
    print("Starting Scraping for Songs")
    if(scrape_song_data()):
        print("..... Completed scraping for Songs")
        
    print("Starting Scraping for TV Shows")
    
    if(scrape_tvshows_data()):
        print(".....  Completed scraping for TV Shows")
    
    print("Starting Scraping for Books ")
    
    if(scrape_books_data()):
        print(".....  Completed scraping for Books")
        
    return True
        
