import parser_library

def main():
    # Most downloadad books url
    url = "http://www.gutenberg.org/browse/scores/top"
    # Get html.text from url
    raw_html = parser_library.get_html_text(url)
    #All books on top 100 page 
    titles, links = parser_library.get_titles_links(raw_html)
    #   Checks working directory 
    #   and creates it if not available if argument is given,
    #   subdirectory is created
    path_local_archive = parser_library.get_or_create_output_folder()
    
    # gets all books through counting from 1 to max 
    # parser_library.get_all_books(path_local_archive)
    #Get metadata
    parser_library.get_all(path_local_archive)


    # print(titles,links)
    # for n in enumerate(titles):
        
    #     test = parser_library.Books(links[n[0]])
    #     test.get_book_data()
    #     test.print_metadata(False)
    #     test.download(path_local_archive)
       

    #     # if n[0]>=3:
    #     #     break

if __name__ == "__main__":
    main()