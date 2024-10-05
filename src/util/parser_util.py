import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def _get_ep_content_from_link(url:str):
    """
    Get the content of a given episode link

    Parameters
    ----------
    url : str
        The link to the episode. The link can be from either wikipedia or fandom.

    Returns
    -------
    str
        The content of the episode as a string.

    Notes
    -----
    The function will then parse the content of the episode. If the link is from
    fandom, the function will remove all the text in the sections of "Gallery",
    "References", and "External Links". If the link is from wikipedia, the function
    will remove all the text in the sections after the section of "Production".
    """
    if not url:
        return ""
    
    response = None
    while not response:
        try:
            response = requests.get(url)
        except Exception:
            time.sleep(5)
            response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    main_content = soup.find('div', class_='mw-parser-output')

    article_text = ""
    if "fandom" in url:
        for element in main_content.find_all(['p', 'li', 'h2', 'h3']):
            if element.name == 'h2' and ('Gallery' in element.get_text() or 'References' in element.get_text() or 'External Links' in element.get_text()):
                continue
            article_text += element.get_text(separator=' ', strip=True) + ' '

    elif "wikipedia" in url:
        for element in main_content.find_all(['p', 'h2', 'h3']):
            if element.name == 'h2' and 'Production' in element.get_text():
                break
            article_text += element.get_text(separator=' ', strip=True) + ' '

    article_text = article_text.replace('\xa0', ' ')
    article_text = article_text.replace('\u200b', '')
    citation_pattern = r'\[\s*\d+\s*\]'
    clean_text = re.sub(citation_pattern, '', article_text)
    return clean_text


def get_all_episodes_df(url:str):
    """
    Get all the episodes data from a given url as a pandas DataFrame.

    Parameters
    ----------
    url : str
        The url to the webpage containing the episodes. The url can be from either
        wikipedia or fandom.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame containing the episodes.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    episode_list = []

    if "fandom" in url:
        seasons = soup.find_all('div', class_='mw-parser-output')[0].find_all('h3')
        for season in seasons:
            episodes = season.find_next("tbody").find_all('tr')[1:]
            for episode in episodes:
                episode_elem = episode.find_next("a")
                title = episode_elem.text.strip()
                episode_url = 'https://how-i-met-your-mother.fandom.com' + episode_elem['href']
                episode_list.append({
                    'title': title,
                    'link': episode_url
                })

    elif "wikipedia" in url:
        episode_tables = soup.find_all('table', class_='wikitable plainrowheaders wikiepisodetable')
        for season, table in tqdm(enumerate(episode_tables, 1), "Extracting each season table"):
            rows = table.find_all('tr')[1:]
            for row in rows:
                try:
                    title = row.find('td', class_='summary').get_text(strip=True)
                    link_tag = row.find('td', class_='summary').find('a')
                    href = f"https://en.wikipedia.org{link_tag['href']}" if link_tag else None

                    airdate = row.find_all('td')[4].get_text(strip=True)
                    date_pattern = r'\(([^)]+)\)'
                    match = re.search(date_pattern, airdate)
                    if match:
                        extracted_text = match.group(1)
                        airdate = extracted_text
                    viewership = row.find_all('td')[6].get_text(strip=True)
                    citation_pattern = r'\[\d+\]|\(\d+\)'
                    viewership = re.sub(citation_pattern, '', viewership)
                    episode_list.append({"season": season, "title": title, "link": href, "airdate": airdate, "viewership(mil)": viewership})
                except:
                    continue

    tqdm.pandas(desc="Extracting individual episode data from links")
    df = pd.DataFrame(episode_list)
    df["content"] = df["link"].progress_apply(_get_ep_content_from_link)
    df = df.drop("link", axis=1)
    df["episode_num"] = df.index + 1
    return df
