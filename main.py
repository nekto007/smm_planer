import os
from asyncio import run

import pygsheets
import telegram
from dotenv import load_dotenv

from globals import *
from google_spreadsheets import get_rows_for_posts, get_download_file, get_parse_file, update_post_id
from tg import post_telegram


def main():
    load_dotenv()
    service_file_spreadsheet = os.getenv('SERVICE_FILE_SPREADSHEET')
    spreadsheet_smm_key = os.getenv('SPREADSHEET_SMM_KEY')
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    gc = pygsheets.authorize(service_file=service_file_spreadsheet)
    spreadsheet_smm = gc.open_by_key(spreadsheet_smm_key)
    worksheet_smm = spreadsheet_smm.sheet1
    min_row = 20
    max_row = worksheet_smm.rows
    all_table_rows = worksheet_smm.range(f'{min_row}:{max_row}', returnas='cell')
    rows_for_post = get_rows_for_posts(all_table_rows)
    for row in rows_for_post:
        file_link = row[SMM_GOOGLE_DOC].value
        if file_link:
            downloaded_doc = get_download_file(file_link)
            text, image = get_parse_file(downloaded_doc)
            if row[SMM_TG].value:
                field_id = row[SMM_TELEGRAM_POST_ID].label
                bot = telegram.Bot(token=telegram_token)
                post_id = run(post_telegram(telegram_chat_id, bot, text, image))
                update_post_id(worksheet_smm, field_id, post_id)


if __name__ == '__main__':
    main()
