#

import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

from car_data import url_cars, columns_ordered

def populate(soup, content):
    """populates the content with values from soup
    Args:
        soup = BeautifulSoup parsed
        content = dict()
    Return:
        content = dict() populated with soup content
    """
    divTag = soup.find_all("div", {"class": "css-1ajawdl e2zahha0"})
    title = soup.title.text
    content[title] = dict()
    for _div in divTag:
        div_sub = _div.findAll('div')
        if div_sub:
            category = div_sub[0].text
            value = div_sub[1].text
            if category in content:
                print("!!! category: ", category, " is present")
            content[title][category] = value
        else:
            pass
    return content

def iterate_urls():
    """
    Args:
        None
    Return:
        dict()
    """
    content = dict()
    for url in url_cars[:1]:
        print("reading: ", url)
        with urlopen(url) as reponse:
            html = reponse.read()
        soup = BeautifulSoup(html, 'html.parser')
        content = populate(soup, content)
    return content


def save_2tab(content, path2save):
    """saves to csv file using pandas
    Args:
        content = dict() with data
        path2save = abspath to file
    Return:
        saves tabular file
    """
    df = pd.DataFrame.from_dict(content,
                                orient = 'columns')
    df = df.T
    columns_order = [i for i in columns_ordered if i in df.columns]
    feats_unordered = [a for a in df.columns if a not in columns_order]
    # try:
    #     df = df[[columns_order + feats_unordered]]
    # except Exception as e:
    #     print(e)
    df.to_csv(path2save)


if __name__ == "__main__":
    file_name = "caranddrive_compare_20220528.csv"
    dir_2save = os.getcwd()
    path2save = os.path.join(dir_2save,
                             file_name)

    content = iterate_urls()
    save_2tab(content, path2save)
