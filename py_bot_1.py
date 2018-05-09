
import collections
import helper_fun
import bot1_web_parser
import requests

def main():
   
    #Test site
    url = 'https://sites.google.com/site/soundfonts4u/'

    helper_fun.print_header()
    search_key = helper_fun.get_search_text_from_user()
    file_directory= helper_fun.get_or_create_output_folder()
    searchreport = bot1_web_parser.get_gdrive_filelist(url)

    for n in range(0,len(searchreport[0])):
        print(searchreport.filename[n])
    print(searchreport.g_id[0])
    bot1_web_parser.get_Files_from_google_id(searchreport.g_id[0],searchreport.a_ref[0], file_directory)
    



if __name__ == "__main__":
    main()
    