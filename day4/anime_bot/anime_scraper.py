# Gogoanime scraper
import os.path
import helper

from requests import get
from json import dumps, load
from re import sub
from bs4 import BeautifulSoup

# Refactor for dotenv
URL = "https://gogoanime.ai/" 
URL_PAGE = URL + '?page=1'  
CATEGORY = 'category/'
SEARCH_URL = URL + 'search.html?keyword='
ANIME_FILE = os.getenv("ANIME_DIRECTORY") + "/file/anime_list.json"
SUBSCRIPTION=True
#https://gogoanime.ai//search.html?keyword=boku%20no%20hero


# Get Page and create Soup
# Returns BeautifulSoup page
def get_soup_page(url):
    try:
        page = page = get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup
    except:
        print("Website not avaiable...", flush=True)
    

# Base scraping
# Returns list 
def get_anime_entries(url):
    soup = get_soup_page(url)
    try:
        list_entries = soup.find('ul', class_='items')
        anime_entries = list_entries.find_all('li')
        return anime_entries
    except:
        print("Something went wrong in scraping..", flush=True)

# Scraping page 1 of site
# Returns dict "anime" : episode
def extract_anime_list(url):
    anime_entries = get_anime_entries(url)

    extracted_anime = {}
    if(anime_entries):
        for anime_entry in anime_entries:
            anime_title = helper.clean_text(
                            anime_entry
                            .find('p', class_='name')
                            .find('a')['title']
                            ).capitalize()
            episode_no = anime_entry.find('p', class_='episode').text.lower().strip('episode ')
            extracted_anime[anime_title] = int(episode_no)

    return extracted_anime

# Scraping page of search results
# Returns dict "anime" : episode
def extract_search_list(url):
    anime_entries = get_anime_entries(url)

    extracted_anime = {}
    if(anime_entries):
        for anime_entry in anime_entries:
            anime_title = helper.clean_text(
                            anime_entry
                            .find('p', class_='name')
                            .find('a')['title']
                            ).capitalize()
            release_date = anime_entry.find('p', class_='released').text
            extracted_anime[anime_title] = release_date.strip()

    return extracted_anime

# Reads anime file list on server
# Returns dict "anime" : episode
def read_anime_list_file():
    # Checks if anime file is present
    if(os.path.isfile(ANIME_FILE)):
        with open(ANIME_FILE) as infile:
            return load(infile)
    else:
        print("No current anime list...Creating one", flush=True)
        return {}

# Checks if scraped anime is the same or updated
# is_subscribe flag True - compares scraped to existing file
# is_subscribe flag False - Adds new anime upon checking regardless of file
# Returns dict "anime" : episode
def compare_anime_lists(old_anime_list, new_anime_list, is_subscribed):
    updated_list = {}
    if(new_anime_list):
        for key in new_anime_list:
            if(key in old_anime_list):
                if(new_anime_list[key] > old_anime_list[key]):
                    updated_list[key] = new_anime_list[key]
            else:
                if(not is_subscribed):
                    updated_list[key] = new_anime_list[key]
    return updated_list

# Consolidates new anime and updated anime to a dict
# Returns dict "anime" : episode
def consolidate_anime_list(old_list, updated_list):
    for key in updated_list:
        old_list[key] = updated_list[key]
    return old_list

# Writes to anime list file
def update_anime_list_file(updated_anime_list):
    json_obj = dumps(updated_anime_list, indent=4)

    with open(ANIME_FILE, "w") as outfile:
        outfile.write(json_obj)

# Create a dict of string of links
# Replaced all space with '-'
# {URL}{anime}{episode}{episode#} 
# Returns dict "anime" : "link"
def create_links(anime_list):
    anime_links = {}
    for key in anime_list:
        if(anime_list[key]):
            link = "%s %s %s" % (key, 'episode', str(anime_list[key]))
            link = helper.remove_colon(link)
            link = helper.replace_space_with_minus(link)
            link = URL + link.lower()
        else:
            link = "%s%s" % (CATEGORY, key)
            link = helper.remove_colon(link)
            link = helper.replace_space_with_minus(link)
            link = URL + link.lower()
        anime_links[key] = link
    return anime_links


# Calls number of scraper methods for anime bot
def call_scraper():
    final_list = {}
    old_list = read_anime_list_file()
    new_list = extract_anime_list(URL_PAGE)
    updated_list = compare_anime_lists(old_list, new_list, SUBSCRIPTION)
    if(updated_list):
        final_list = consolidate_anime_list(old_list, updated_list)
        update_anime_list_file(final_list)
    return updated_list


#Parked search function
#Pending logic is, get anime title and released date. add to file with 0 episode to update next time
def call_search_scraper(query):
    search_query = helper.replace_space_with_urlspace(query).lower()
    search_url = SEARCH_URL + search_query
    extracted_search_list = extract_search_list(search_url)
    return extracted_search_list

def create_anime_page_link(url):
    anime_title = helper.better_strip(url, URL)
    anime_title = helper.better_strip(anime_title, '-episode-\d+')
    return "%s%s%s" % (URL, CATEGORY, anime_title)

def strip_content(content):
    anime = {}
    link = helper.better_strip(content, f'^!addanime ')
    if(link.find('episode') != -1):
        link = create_anime_page_link(link)
    episode = int(check_current_episode(link))
    link = helper.better_strip(link, URL + CATEGORY)
    title = helper.replace_minus_with_space(link).capitalize()
    anime[title] = episode
    return anime

def check_current_episode(url):
    page = get_soup_page(url)
    episode_page = page.find('ul', id='episode_page').find('a')
    return episode_page['ep_end']


def add_anime(content):
    to_add_list = strip_content(content)
    old_list = read_anime_list_file()
    updated_list = compare_anime_lists(old_list, to_add_list, False)
    if(updated_list):
        final_list = consolidate_anime_list(old_list, updated_list)
        update_anime_list_file(final_list)
    return create_links(updated_list)

def link_checker(content):
    message = sub('^!addanime ', '', content)
    if(message.startswith(URL)):
        soup = get_soup_page(message)
        try:
            status = soup.find('h1', class_='entry-title').text
        except AttributeError:
            return True
        return status != '404'
    return False

def get_watchlist():
    anime_list = read_anime_list_file()
    anime_links = create_links(anime_list)
    list_with_episodes = {}
    for entry in anime_list:
        list_with_episodes[entry + f" - Episode {anime_list[entry]}"] = anime_links[entry]
    return list_with_episodes

#print(add_anime('!addanime https://gogoanime.ai/category/boku-no-hero-academia-5th-season'))
#print(add_anime('!addanime https://gogoanime.ai/category/otome-game-no-hametsu-flag-shika-nai-akuyaku-reijou-ni-tensei-shiteshimatta-x'))
#print(add_anime('!addanime https://gogoanime.ai/boku-no-hero-academia-5th-season-episode-1'))
#test_message = "!addanime https://gogoanime.ai/boku-no-hero-academia-5th-season-episode-1"
#print(strip_content(test_message))
#print(strip_message(test_message))
#print(call_search_scraper("working"))
#print(dumps(call_scraper(), indent=4))
#print(add_anime('!addanime https://gogoanime.ai/digimon-adventure-2020-episode-42'))