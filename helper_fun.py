import os

def print_header():
    app_title = "First Python Bot"
    print(type(len(app_title)),len(app_title))

    #Construct title based on length of string and tile multiple
    tile_design_multiple = 3 
    print("*" * tile_design_multiple*len(app_title) + "\n" + 
    " " * int(tile_design_multiple*len(app_title)/2-len(app_title)/2) + app_title + "\n" 
    + "*" * tile_design_multiple*len(app_title))


#Check and create folder for files if nesssesarry
def get_or_create_output_folder():
    #Address to folder containing .py file
    base_folder = os.path.dirname(__file__)
    #Folder name of soundfont2-library
    folder = 'sf2-library'
    full_path = os.path.join(base_folder,folder)
    # Falls phad nicht existiert oder existiert ist aber kein ordner -> erstelle ordner
    if not os.path.exists(full_path) or not os.path.isdir(full_path):
        print('Creating new directory at {}'.format(full_path))
        os.mkdir(full_path)

    return full_path


#Get search input from user
def get_search_text_from_user():
    text = input('What are you searching for [Single Phrase only eg. keys]?')      
    return text.lower()
