import os
from asyncio import run

import pygsheets
import requests
import telegram
from dotenv import load_dotenv

from google_spreadsheets import get_rows_for_posts, get_download_file, get_parse_file, update_post_id, fetch_gif_image
from tg import send_post, send_animation_image


def fetch_gif_image(image_url):
    url = image_url
    filename = os.path.basename(image_url)
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)
    return filename


def main():
    # cell groups
    SMM_TG = 0
    SMM_OK = 1
    SMM_VK = 2
    SMM_DATE_POST = 3
    SMM_TIME_POST = 4
    SMM_DATE_ACTUAL_POST = 5
    SMM_GOOGLE_DOC = 6
    SMM_IMAGE_LINK = 7
    SMM_TELEGRAM_POST_ID = 8
    SMM_VKONTAKTE_POST_ID = 9
    SMM_ODNOKLASSNIKI_POST_ID = 10
    SMM_PUBLISH_POST = 11
    load_dotenv()
    service_file_spreadsheet = os.getenv('SERVICE_FILE_SPREADSHEET')
    spreadsheet_smm_key = os.getenv('SPREADSHEET_SMM_KEY')
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    gc = pygsheets.authorize(service_file=service_file_spreadsheet)
    spreadsheet_smm = gc.open_by_key(spreadsheet_smm_key)
    worksheet_smm = spreadsheet_smm.sheet1
    min_row = 21
    max_row = worksheet_smm.rows
    all_table_rows = worksheet_smm.range(f'{min_row}:{max_row}', returnas='cell')
    rows_for_post = get_rows_for_posts(all_table_rows)
    for row in rows_for_post:
        field_id = row[SMM_TELEGRAM_POST_ID].label
        file_link = ''
        image_link = ''
        if row[SMM_GOOGLE_DOC].value:
            file_link = row[SMM_GOOGLE_DOC].value
        else:
            image_link = row[SMM_IMAGE_LINK].value
        if file_link:
            downloaded_doc = get_download_file(file_link)
            text, image = get_parse_file(downloaded_doc)
            if row[SMM_TG].value:
                bot = telegram.Bot(token=telegram_token)
                post_id = run(send_post(telegram_chat_id, bot, text, image))
                update_post_id(worksheet_smm, field_id, post_id)
        elif image_link:
            image = fetch_gif_image(image_link)
            if row[SMM_TG].value:
                bot = telegram.Bot(token=telegram_token)
                post_id = run(send_animation_image(telegram_chat_id, bot, image))
                update_post_id(worksheet_smm, field_id, post_id)


if __name__ == '__main__':
    main()
