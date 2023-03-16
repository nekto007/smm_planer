import base64

import requests
from docx_parser import DocumentParser

from globals import *


def update_post_id(worksheet_smm, field_id, post_id):
    worksheet_smm.update_value(str(field_id), post_id)


def get_parse_file(path):
    doc = DocumentParser(path)
    text = []
    filename = None
    for _type, item in doc.parse():
        if _type == 'paragraph':
            text.append(item['text'])
        elif _type == 'multipart':
            img_data = item[1]['image'].split(',')[1]
            filename = item[1]['filename']
            recovered = base64.b64decode(img_data)
            with open(filename, 'wb') as file:
                file.write(recovered)
    return ' '.join(text), filename


def get_download_file(link):
    file_id = link.split('/')[-2]
    url = f"https://docs.google.com/document/d/{file_id}/export?format=docx&id={file_id}"
    response = requests.get(url)
    file_name = 'post.docx'
    with open(file_name, 'wb') as f:
        f.write(response.content)
    return file_name


def get_rows_for_posts(all_table_rows):
    rows_for_post = []
    for row in all_table_rows:
        if row[SMM_TG].value != 'FALSE' or row[SMM_OK].value != 'FALSE' or row[SMM_VK].value != 'FALSE':
            rows_for_post.append(row)
        else:
            break
    return rows_for_post
