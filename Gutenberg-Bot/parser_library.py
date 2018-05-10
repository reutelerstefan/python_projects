import requests
import bs4
import urllib3
import os
import re
import json
def get_book(gutenberg_id):
    pass

# Get_all metadata
def get_all(path_local_archive):
    #highest book_id 
    # in the future should check code
    max_book_id = 57122
    # constructs website link base on gutenberg id
    all_books_link = (["/ebooks/" + str(n)
        for n in range(1,max_book_id)
        if n])
    
    book_database = []
    # Constructs full_path for json file inside - Gutenberg-Archive File
    json_file_location = os.path.join(get_or_create_output_folder(),"library.json")
    # In each iteration json file gets read, appended, writen
    with open(json_file_location, mode='w', encoding='utf-8') as f:
        json.dump([], f)
    # Iterates over all book_links in ascending order
    # Note Slicing
    for n in all_books_link[:100]:
        with open(json_file_location, mode='r', encoding='utf-8') as feedsjson:
            feeds = json.load(feedsjson)
        # Creates instance of books class for book id using directory
        test = Books(n)
        #Using beautifull soup gets 
        # metadata, file link 
        test_data=test.get_book_data()
        # If argument == True -> prints meta_data
        test.print_metadata(True)
        # adds dictonary from book.get_book_data to list
        # Results in List with all Books
        book_database.append(test_data)
        # and downloads file in 
        # folder based on author
        test.download(path_local_archive)
        #  Writes list(dict_book1,dict_book2....) after
        # each iteration to json file
        with open(json_file_location, 'w', encoding='utf-8') as fp:
            # appends most recent book to imported data
            feeds.append(test_data)
            # Writes json file
            json.dump(feeds,fp)

    # Test to access meta_data
    for element in book_database:
        if "language" in element:
            print(element['title'])   
    #  Prints full path of json library at the end of execution
    print(get_or_create_output_folder() + '/library.json')
    
    
# Folder managment
def get_or_create_output_folder(base_path = []):
    #If no argument is provided checks/created archive directory
    # IF an argument (string) is provided creates subdirectory in archive folder
    if not base_path:
        # Get directory of main loop python script
        base_folder = os.path.dirname(__file__)

        #Folder name of gutenberg library
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
    #Gets data from url 
    # If connection sucessfull -> return text part of data
    response = requests.get(url)
    if response.status_code:
        print('Connection to site {} sucessfull!'.format(url))
        return response.text
    else:
        print('Could not connect to {}'.format(url))


# Crawls gutenberg site for books -> returns title and links
# Fast part of algorithm
def get_titles_links(raw_html):
    soup = bs4.BeautifulSoup(raw_html, 'html.parser')
    book_titles = []
    book_links = []
    for a in soup.find_all('a', href=True):
        #if books
        if "/ebooks" in a['href']:
            if len(a['href']) > len('/ebooks/'):
                # Gets actual link to book
                book_links.append(a['href'])
                # Returns caption of links which should be title
                # This title is different to the title from get_all_method
                # less reliable
                book_titles.append(a.get_text())    
    return book_titles,book_links


# Using regex removes all keysymbols except chars, and joints them together
# using whitespace
# Aim: to sanitize data for writing files
def remove_non_characters(raw_string):
    word1 = " ".join(re.findall("[a-zA-Z]+", raw_string))
    print(word1)
    return word1

# Book class that gathers data based on gutenberg id
# .get_meta
# .print_metadata()
# .download(self, text_dir ):
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
  
    # Gets meta_data from beautifulsoup
    # Very slow   
    def get_book_data(self,comment_Id = False):
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
        # Tags or subjects as lists -> can be multiple
        tags = ([a.get_text().strip()
            for a in soup.findAll(property="dcterms:subject")
                if soup.findAll(property="dcterms:subject")])
        # Get last entry in case there "language" inside the get_text
        self.subjects = tags
        # Generator that gets link to text files
        txt_link = ([a['href'] 
        for a in soup.find_all('a', href=True)
            if ".txt" in a['href']
            ])
        # Constructs absolute link from /books/id/..../*.txt
        for n in txt_link:
            # Work-Around to filter out empty data/or wiered formating
            n = n.split("/")
            hirarc_list = list(filter(None,n))
            n = "/".join(hirarc_list)
            print(n)
            if 'www.gutenberg.org' in n:
                self.text_link = 'http://' + n
            else:
                self.text_link = 'http://www.gutenberg.org/' + n
        #Gets number id from full linmk
        number_id = self.directory.split("/")[-1]
        if comment_Id:
            print("Number id: {}".format(number_id))
        # !!!! Discrepancy between  return value: id only and input books /books/id
        return {"directory":number_id ,"title" : self.title, "author" :self.author,"language" : self.language  ,"txt_link" : self.text_link ,"subjects" :self.subjects }
    
    # Fetches soup file from link
    def get_rawHTML(self,debug=False):
        # Checks input if prefix 'http://www.gutenberg.org' is present
        if not 'http://www.gutenberg.org' in self.directory:
            url = 'http://www.gutenberg.org' + self.directory
            if debug:
                print('Gutenberg Booksite at: {}'.format(url))
        else: 
            url= self.directory
        # Gets data from url
        html = requests.get(url)
        html_raw = html.text
        soup = bs4.BeautifulSoup(html_raw, 'html.parser')
        return soup

    # Download file based on self.text_link
    # 
    def download(self, text_dir, debug = False ):
        # open in binary mode
        # Sanitize title_string -> max len 30 and remove non whitespace and char symbols
        # Requires get_book_data to be run in advance
        # connection .json <-> .txt
        # excerption handling
        # removes bad characters
        sanitized_title = remove_non_characters(self.title)
        sanitized_author = remove_non_characters(self.author)
        file_name = sanitized_title 
        file_name = file_name.strip()
        # max_file length 100 characters
        file_name = file_name[:100]
        full_path = os.path.join(text_dir,sanitized_author)
        
        
        # Check if folder of authors exists or create it otherwise
        get_or_create_output_folder(full_path)
        
        full_path = os.path.join(full_path,file_name+ '.txt')
        if debug:
            print("This is the self.text data: {}".format(self.text_link))
            print("This is the fullpath: {}".format(full_path))


        if self.text_link:
            with open(full_path, "wb") as file:
                # get request
                response = requests.get(self.text_link)
                # write to file
                if response:
                    file.write(response.content)
        else:
            print('Textfile not found!')


    