import os, shutil, re
from markdown import Markdown
from json import loads, dumps
from pathlib import Path


md_path = Path(__file__).parent/"Md_Articles"/"Article_description"
json_path = Path(__file__).parent/"article_path.json"

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


#print(_convert_md_to_html(_get_files(md_path)))

def article_description_to_json(json_file):
    msg_list = _convert_md_to_html(_get_files(md_path))
    msg_path = _get_files(md_path)
    html_name = []

    for filepath in msg_path:

        #get file name
        name_pattern = rf'{re.escape(str(md_path))}/([^/]+)\.md$'
        match = re.search(name_pattern, filepath)
        
        #Add file name to a list
        html_name.append(str(match.group(1)))

    print(html_name)


    #TODO: json file must according to latest modification time

article_description_to_json(json_path)

