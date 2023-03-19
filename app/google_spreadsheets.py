import base64
import os

import requests
from docx_parser import DocumentParser

SMM_TG = 0
SMM_OK = 1
SMM_VK = 2
SMM_DATE_POST = 3
SMM_TIME_POST = 4
SMM_DATE_ACTUAL_POST = 5
SMM_GOOGLE_DOC = 6
SMM_IMAGE_LINK = 7
SMM_TG_POST_ID = 8
SMM_VK_POST_ID = 9
SMM_OK_POST_ID = 10
SMM_DELETE_POST = 11
SMM_POSTS_PUBLISH = 12


def update_post_id(row, post_id, network):
    row[globals()[f"SMM_{network}"]].color = (0, 1, 0, 0)
    row[globals()[f"SMM_{network}_POST_ID"]].value = post_id
    row[globals()[f"SMM_{network}"]].value = True
    row[SMM_POSTS_PUBLISH].value = True


def get_parsed_file(path):
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
    os.remove(path)
    return ' '.join(text), filename


def get_file(link):
    file_id = link.split('/')[-2]
    url = f"https://docs.google.com/document/d/{file_id}/export?format=docx&id={file_id}"
    response = requests.get(url)
    file_name = 'post.docx'
    with open(file_name, 'wb') as f:
        f.write(response.content)
    return file_name


def get_rows_for_posts(all_table_rows):
    rows_for_post = []
    rows_for_delete = []
    for row in all_table_rows:
        if row[SMM_TG].value == 'TRUE' and row[SMM_TG_POST_ID].value == '':
            rows_for_post.append(row)
        elif row[SMM_OK].value == 'TRUE' and row[SMM_OK_POST_ID].value == '':
            rows_for_post.append(row)
        elif row[SMM_VK].value == 'TRUE' and row[SMM_VK_POST_ID].value == '':
            rows_for_post.append(row)
        elif row[SMM_DATE_ACTUAL_POST].value and row[SMM_DELETE_POST].value == 'FALSE' and (
                row[SMM_TG_POST_ID].value != '' or row[SMM_OK_POST_ID].value != '' or row[SMM_VK_POST_ID].value != ''):
            rows_for_delete.append(row)
    return rows_for_post, rows_for_delete
