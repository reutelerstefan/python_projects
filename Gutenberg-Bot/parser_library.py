import requests
import bs4
import urllib3
import os
import re
import json




#Check if/or Creates directory where .txt files get saved
# Depending on argument subdirectory is created instead
def get_all_books(path_local_archive):
    # highest book id on gutenberg -> can change -> idealy write parser
    max_book_id = 57122
    all_books_link = (["/ebooks/" + str(n)
        for n in range(3913,max_book_id)
        if n])

    for n in all_books_link:
        test = Books(n)
        test.get_book_data()
        test.print_metadata(True)
        test.download(path_local_archive)

def get_all(path_local_archive):
    #highest book_id 
    max_book_id = 57122
    all_books_link = (["/ebooks/" + str(n)
        for n in range(1,max_book_id)
        if n])
    
    book_database = []
    json_file_location = os.path.join(get_or_create_output_folder(),"library.json")
    
        
    print(json_file_location)
    
    with open(json_file_location, mode='w', encoding='utf-8') as f:
        json.dump([], f)
    for n in all_books_link[:100]:
        with open(json_file_location, mode='r', encoding='utf-8') as feedsjson:
            feeds = json.load(feedsjson)
        

        test = Books(n)
        test_data=test.get_book_data()
        print(test_data['language'])
        test.print_metadata(True)
        book_database.append(test_data)
        test.download(path_local_archive)
        with open(json_file_location, 'w', encoding='utf-8') as fp:
            feeds.append(test_data)
            json.dump(feeds,fp)


    for element in book_database:
        if "language" in element:
            print(element['title'])   
    
    print(get_or_create_output_folder() + '/library.json')
    


def get_or_create_output_folder(base_path = []):
    #Address to folder containing .py file
    if not base_path:
        base_folder = os.path.dirname(__file__)
        #Folder name of soundfont2-library
        folder = 'Gutenberg-Archive'
        full_path = os.path.join(base_folder,folder)
    else:
        full_path = base_path
    # Falls phad nicht existiert oder existiert ist aber kein ordner -> erstelle ordner
    if not os.path.exists(full_path) or not os.path.isdir(full_path):
        print('Creating new directory at {}'.format(full_path))
        os.mkdir(full_path)

    return full_path

# Using beautifulsoup gets text of html
def get_html_text(url):
    response = requests.get(url)
    if response.status_code:
        print('Connection to site {} sucessfull!'.format(url))
        return response.text
    else:
        print('Could not connect to {}'.format(url))


def get_titles_links(raw_html):
    soup = bs4.BeautifulSoup(raw_html, 'html.parser')
    book_titles = []
    book_links = []
    

    for a in soup.find_all('a', href=True):
        #if books
        if "/ebooks" in a['href']:
            if len(a['href']) > len('/ebooks/'):
                book_links.append(a['href'])
                book_titles.append(a.get_text())
            

    return book_titles,book_links


def remove_non_characters(raw_string):
    word1 = " ".join(re.findall("[a-zA-Z]+", raw_string))
    print(word1)
    return  word1


class Books:
    # Initizalization of array (not 100% sure about variables with default)
    def __init__(
            self, directory,title='', author='', txt_link = '',subjects = [], language= '' ):
        self.title = title
        self.author = author
        self.directory = directory
        self.text_link = []
        self.subjects = []
        self.language = []
    # Prints meta_data of books page,
    def print_metadata(self,debug = True):
        if debug:
            print()
            print('--------------------------------------------')
            print("Title: {}".format(self.title))
            print("Author: {}".format(self.author))
            print("Language: {}".format(self.language))
            print("Txt-File: {}".format(self.text_link))
            print("Subjects: {}".format(self.subjects))
            print("Directory: {}".format(self.directory))
            print('--------------------------------------------')
            print()
  
    def get_book_data(self):
        soup = self.get_rawHTML()
        #Get individual entry from bibliography-data        
        # If -Loop to stop crash if parser return 0
         #Author
        if soup.find(itemprop="headline"):
            self.title = soup.find(itemprop="headline").get_text().strip()     
        #Author
        if soup.find(itemprop="creator"):
            self.author = soup.find(itemprop="creator").get_text().strip()
        #Language
        if soup.find(itemprop="inLanguage"):
            data_language = soup.find(itemprop="inLanguage").get_text().split()[-1]
            self.language = data_language

        tags = ([a.get_text().strip()
            for a in soup.findAll(property="dcterms:subject")
                if soup.findAll(property="dcterms:subject")])
        # Get last entry in case there "language" inside the get_text
        
        self.subjects = tags

        txt_link = ([a['href'] 
        for a in soup.find_all('a', href=True)
            if ".txt" in a['href']
            ])
        
        for n in txt_link:
            n = n.split("/")
            hirarc_list = list(filter(None,n))
            n = "/".join(hirarc_list)
            print(n)
            if 'www.gutenberg.org' in n:
                self.text_link = 'http://' + n
            else:
                self.text_link = 'http://www.gutenberg.org/' + n
        
        number_id = self.directory.split("/")[-1]
        print("Number id: {}".format(number_id))        
        return {"directory":number_id ,"title" : self.title, "author" :self.author,"language" : self.language  ,"txt_link" : self.text_link ,"subjects" :self.subjects }
    # ,,self.text_link ,self.subjects, self.language 
       
        
        

    def construct_abs_link(self, debug = True):
        url = 'http://www.gutenberg.org' + self.directory
        if debug:
            print('Gutenberg Booksite at: {}'.format(url))
        return url


    def get_rawHTML(self):
        url = self.construct_abs_link()
        html = requests.get(url)
        html_raw = html.text
        soup = bs4.BeautifulSoup(html_raw, 'html.parser')
        return soup


    



    def download(self, text_dir ):
        # open in binary mode
        # Sanitize title_string -> max len 30 and remove non whitespace and char symbols
        sanitized_title = remove_non_characters(self.title)
        sanitized_author = remove_non_characters(self.author)
        file_name = sanitized_title 
        file_name = file_name.strip()
        file_name = file_name[:100]
        full_path = os.path.join(text_dir,sanitized_author)
        
        print(self.text_link)
        # Check if folder of authors exists or create it otherwise
        get_or_create_output_folder(full_path)
        
        full_path = os.path.join(full_path,file_name+ '.txt')
        print(full_path)
        if self.text_link:
            with open(full_path, "wb") as file:
                # get request
                response = requests.get(self.text_link)
                # write to file
                if response:
                    file.write(response.content)
        else:
            print('Textfile not found!')


    