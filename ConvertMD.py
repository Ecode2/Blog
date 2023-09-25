import os, re
from markdown import Markdown
import json
from pathlib import Path


json_path = Path(__file__).parent/"article_path.json"

description_md_path = Path(__file__).parent/"Md_Articles"/"Article_description"
description_path = Path(__file__).parent/"static"/"docs"/"Article_description_html"

article_md_path = Path(__file__).parent/"Md_Articles"/"Articles" 
article_path = Path(__file__).parent/"static"/"docs"/"Article_html"

def _get_files(folder_dir):
    files = []

    for file in os.listdir(folder_dir):
        if not os.path.exists(folder_dir):
            raise OSError(f"{folder_dir} folder does not exists")

        if not os.path.isfile(f"{folder_dir}/{file}"):
            raise OSError(f"contents of {folder_dir} is not a file")

        files.append(f"{folder_dir}/{file}")

    #Sorts file path by the latest modified
    latest_mod_file = sorted(files, key=lambda x: os.path.getmtime(x), reverse=True)

    return latest_mod_file


def _convert_md_to_html(md_files):
    html_msg = []

    for msg_file in md_files:
        if not os.path.exists(msg_file):
            raise OSError(f"{msg_file} folder does not exists")

        if not os.path.isfile(msg_file):
            raise OSError(f"contents of {msg_file} is not a file")

        if not msg_file.endswith(".md"):
            continue

        #opens the markdown file
        with open(msg_file, "r") as msg_text:
            
            #Change markdown to html
            md_obj = Markdown(extensions= ["fenced_code"], output_format="html", tab_length=4)
            converted_message = md_obj.convert(msg_text.read())
        
            #Adding the converted html string to a list
            html_msg.append(converted_message)
    
    return html_msg



def article_description_to_json(json_file, html_path_list):
    
    
    html_list = []
    for index, item in enumerate(html_path_list):

        #Regular experssion pattern to get correct file path
        pattern = r'(/static/docs/Article_description_html/.*)'
        match = re.search(pattern, item)
        short_path = match.group(1)

        html_list.append(short_path)


    #adding the file path to json
    try: #ensure that the json exists and is not empty
        # Load the existing JSON file
        with open(json_file, 'r') as json_file_path:
            json_data = json.load(json_file_path)
    
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is empty, initialize json_data as an empty dictionary
        json_data = {}

    new_list =[]
    #Adds the paths that are not in json to a new list
    for item in html_list:

        if item not in json_data.get('files', []):
            new_list.append(item)


    # Add the new content to the top of the existing list
    json_data['files'] = new_list + json_data.get('files', [])

    # Write the updated JSON data back to the file
    with open(json_file, 'w') as json_file_path:
        json.dump(json_data, json_file_path, indent=4)


def article_to_html(article_folder, article_storage_folder):

    article_list = _convert_md_to_html(_get_files(article_folder))
    article_name_path = _get_files(article_folder)
    article_name = []
    article_path = []

    #gets markdown file names
    for filepath in article_name_path:

        #get file name
        name_pattern = rf'{re.escape(str(article_folder))}/([^/]+)\.md$'
        match = re.search(name_pattern, filepath)

        #Add file name to a list
        article_name.append(str(match.group(1)))


    #adds article file name to article path
    for name in article_name:                                                       
        storage_folder = f"{article_storage_folder}/{name}.html"
        article_path.append(storage_folder)                               
    
    #save markdown to html string to html file
    num = 0
    for article in article_list:

        #creates and saves the html file
        with open(article_path[num], 'w') as article_file:
            article_file.write(article)
            
            num += 1


    return article_path

article_list = article_to_html(description_md_path, description_path)

article_description_to_json(json_path, article_list)
if __name__ == "__main__":

    #Convert articles from markdown to  html files
    article_to_html(article_md_path, article_path)

    #Convert article description snippet from markdown to html
    description_list = article_to_html(description_md_path, description_path)

    #Add html description path to json file
    article_description_to_json(json_path, description_list)
