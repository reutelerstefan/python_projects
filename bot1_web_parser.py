import requests
import re
import bs4
from tqdm import tqdm
import requests

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from google_drive_downloader import GoogleDriveDownloader as gdd

import collections

SearchResult = collections.namedtuple('SearchResult','filename, g_id, a_ref')



def get_gdrive_filelist(url):
    html_text = get_html_from_url(url)
    a_refs, link_name = parse_html_for_file_links(html_text)
    # print(a_refs, link_name)
    # gdrive_a_refs_only= find_gdrive_links(all_a_refs)
    gdrive_id_list = find_gdrive_id_list(a_refs)
    # print(gdrive_id_list)
    report = SearchResult(filename=link_name, g_id=gdrive_id_list, a_ref=a_refs)
    return report


def get_html_from_url(url):
    response = requests.get(url)
    if response.status_code:
        print('Connection to site {} sucessfull!'.format(url))
        return response.text
    else:
        print('Could not connect to {}'.format(url))
    
    # print(response.status_code)
    # print(response.text[0:250]) 

def parse_html_for_file_links(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    matches = []
    file_names = []
    
    for a in soup.find_all('a', href=True):
        if "https://drive.google.com/file/d/" in a['href']:
            matches.append(a['href'])
            file_names.append(a.get_text())

    print(matches,file_names)   
    return matches, file_names



def find_gdrive_id_list(gdrive_link_kist):
    gdrive_id_list = ([
        g_id[len('https://drive.google.com/file/d/'):-len('/view?usp=sharing')]  # projection or items
        for g_id in gdrive_link_kist  # the set to process     
    ]
    )
    return gdrive_id_list

def get_Files_from_google_id(single_gid, single_aref, file_directory):
    gdrive_link_id = single_gid
    html_links = single_aref
    
    raw_HTML_item=get_html_from_url(html_links)
    
           
    file_name = get_filename_from_html(raw_HTML_item)

    
    gdd.download_file_from_google_drive(file_id=gdrive_link_id,
                                    dest_path='./sf2/{}'.format(file_name),
                                    unzip=False)
 
    
    return 


def get_filename_from_html(url):
    raw_html =  get_html_from_url(url)
    soup = bs4.BeautifulSoup(raw_html, 'html.parser')
    file_name = soup.find(class_='uc-name-size').get_text()
    file_name = file_name.split()[0]
    print(file_name)
    return file_name

    
    
 



