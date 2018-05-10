import parser_library

def main():
   
        
    #   Checks working directory 
    #   and creates it if not available if argument is given,
    #   subdirectory is created
    path_local_archive = parser_library.get_or_create_output_folder()
    
    # gets all books through counting from 1 to max 
    # parser_library.get_all_books(path_local_archive)
    #Get metadata
    parser_library.get_all(path_local_archive)


if __name__ == "__main__":
    main()