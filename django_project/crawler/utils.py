from bs4 import BeautifulSoup
import requests


class ScapingWrongUrlType(Exception):
	pass


def scrape_lyrics_tab4u(the_url):
    if the_url[0:35]!='https://www.tab4u.com/lyrics/songs/':
        raise ScapingWrongUrlType('"'+the_url+'" is not value a tab4u lyrics url')        
    source = requests.get(the_url).text
    soup = BeautifulSoup(source,'lxml')
    song=soup.find('div', class_="song_block")
    performer = song.find('div', class_="data_block_title_text").a.text
    title=song.find('h1').font.text.split('-')[1]
    need_to_connect_composer_and_songwriter=False
    try:
       aAndCArea=song.find('div', id="aAndcArea").a.text
       song_writer=aAndCArea
       composer=aAndCArea
       need_to_connect_composer_and_songwriter=False;
    except:
       need_to_connect_composer_and_songwriter=True
    if need_to_connect_composer_and_songwriter:
        for i in song.find('div', id="aAndcArea").text.split('\n'):
           if len(i) > 0:
               if (i.split(':')[0].strip()) == 'מחבר':
                   song_writer = i.split(':')[1].strip()
                   print(song_writer)
               elif (i.split(':')[0].strip()) == 'מלחין':
                   composer = i.split(':')[1].strip()
                   print(composer)
    lyrics=song.find('div', id="songContentTPL").text.replace('\n\n','\n').replace('\n\n\n','\n\n')
    href=song.find('div', class_="lItem woItem").find('a').get('href')
    clean_href=href.replace('../','')
    num_steps_back=(len(href)-len(clean_href))/3
    origin_url_to_keep=int(the_url.index('/')-num_steps_back)-1
    chords_url='/'.join(the_url.split('/')[:origin_url_to_keep])+'/'+clean_href
    song_dict={
        'song_writer' : song_writer,
        'composer' : composer,
        'performer' : performer,
        'title' : title,
        'lyrics': lyrics,
        'chords_url': chords_url}
    return(song_dict)

def scrape_chorld_tab4u(the_url):
    if the_url[0:33]!='https://www.tab4u.com/tabs/songs/':
        raise ScapingWrongUrlType('"'+the_url+'" is not a valid tab4u chords url')        
    source = requests.get(the_url).text
    soup = BeautifulSoup(source,'lxml')
    song=soup.find('div', class_="song_block")
    performer = song.find('div', class_="data_block_title_text").a.text
    title=song.find('h1').font.text.split('-')[1]
    need_to_connect_composer_and_songwriter=False
    try:
       aAndCArea=song.find('div', id="aAndcArea").a.text
       song_writer=aAndCArea
       composer=aAndCArea
       need_to_connect_composer_and_songwriter=False;
    except:
       need_to_connect_composer_and_songwriter=True
    if need_to_connect_composer_and_songwriter:
        for i in song.find('div', id="aAndcArea").text.split('\n'):
           if len(i) > 0:
               if (i.split(':')[0].strip()) == 'מחבר':
                   song_writer = i.split(':')[1].strip()
                   print(song_writer)
               elif (i.split(':')[0].strip()) == 'מלחין':
                   composer = i.split(':')[1].strip()
                   print(composer)
    song_chords=song.find('div', id="songContentTPL").text.replace('\n\n','\n').replace('\n\n\n','\n\n')
    href=song.find_all('div', class_="lItem npt cIS1")[1].find_all('a')[2].get('href')
    clean_href=href.replace('../','')
    num_steps_back=(len(href)-len(clean_href))/3
    origin_url_to_keep=int(the_url.index('/')-num_steps_back)-1
    lyrics_url='/'.join(the_url.split('/')[:origin_url_to_keep])+'/'+clean_href
    song_dict={
        'song_writer' : song_writer,
        'composer' : composer,
        'performer' : performer,
        'title' : title,
        'chords': song_chords,
        'lyrics_url':lyrics_url}
    return(song_dict)

def get_data_for_one_url(the_url):
    url_types={
        'https://www.tab4u.com/lyrics/songs/':['tab4u','lyrics','scrape_lyrics_tab4u','scrape_chorld_tab4u'],
        'https://www.tab4u.com/tabs/songs/':['tab4u','chords','scrape_chorld_tab4u','scrape_lyrics_tab4u']
    }
    for utk in url_types.keys():
       if utk==the_url[:len(utk)]:
          utl_site=url_types[utk][0]
          url_type=url_types[utk][1]
          print(url_type)
          if url_type=='lyrics':
            url_lyrics_function=eval(url_types[utk][2])
            url_chorld_function=eval(url_types[utk][3])
            song_lyrics_url=the_url
            lyrics_dict=url_lyrics_function(the_url)
            chords_dict=url_chorld_function(lyrics_dict['chords_url'])
          elif url_type=='chords':
            url_lyrics_function=eval(url_types[utk][3])
            url_chorld_function=eval(url_types[utk][2])
            song_chords_url=the_url
            chords_dict=url_chorld_function(the_url)
            lyrics_dict=url_lyrics_function(chords_dict['lyrics_url'])
    try:
    	return {'lyrics_dict':lyrics_dict,'chords_dict':chords_dict}
    except UnboundLocalError:
    	raise ScapingWrongUrlType({"message":'"'+the_url+'" is not a supported url type for scraping'})


# url_type format
# for lyrics tipe url - url_standard:[site,url_type,lyrics_scrape_function,chords_script_function]
# for chords tipe url - url_standard:[site,url_type,chords_scrape_function,lyrics_script_function]

url_types={
    'https://www.tab4u.com/lyrics/songs/':['tab4u','lyrics','scrape_lyrics_tab4u','scrape_chorld_tab4u'],
    'https://www.tab4u.com/tabs/songs/':['tab4u','chords','scrape_chorld_tab4u','scrape_lyrics_tab4u']
    }


